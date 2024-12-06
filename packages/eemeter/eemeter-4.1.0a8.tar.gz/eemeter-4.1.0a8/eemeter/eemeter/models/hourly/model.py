#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

   Copyright 2014-2024 OpenEEmeter contributors

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

"""

from __future__ import annotations

import os
os.environ['OMP_NUM_THREADS'] = "1"
os.environ['MKL_NUM_THREADS'] = "1"
os.environ['OPENBLAS_NUM_THREADS'] = "1"

from pydantic import BaseModel

import numpy as np
import pandas as pd

import sklearn
sklearn.set_config(assume_finite=True, skip_parameter_validation=True) # Faster, we do checking

from scipy.spatial.distance import cdist

from sklearn.linear_model import ElasticNet
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.decomposition import PCA, KernelPCA

import pywt

from timeit import default_timer as timer

import json

from eemeter.eemeter.models.hourly import settings as _settings
from eemeter.eemeter.models.hourly import HourlyBaselineData, HourlyReportingData
from eemeter.common.clustering import (
    bisect_k_means as _bisect_k_means,
    scoring as _scoring,
)
from eemeter.common.metrics import BaselineMetrics, BaselineMetricsFromDict


# TODO: need to make explicit solar/nonsolar versions and set settings requirements/defaults appropriately
class HourlyModel:
    # set priority columns for sorting
    # this is critical for ensuring predict column order matches fit column order
    _priority_cols = {
        "ts": ["temporal_cluster", "temp_bin", "temperature", "ghi"],
        "cat": ["temporal_cluster", "temp_bin"],
    }

    """Note:
        Despite the temporal clusters, we can view all models created as a subset of the same full model.
        The temporal clusters would simply have the same coefficients within the same days/month combinations.
    """

    def __init__(
        self,
        settings: (
            _settings.HourlyNonSolarSettings | _settings.HourlySolarSettings | None
        ) = None,
    ):
        """ """

        # Initialize settings
        if settings is None:
            self.settings = _settings.HourlyNonSolarSettings()
        else:
            self.settings = settings

        # Initialize model
        if self.settings.SCALING_METHOD == _settings.ScalingChoice.STANDARDSCALER:
            self._feature_scaler = StandardScaler()
            self._y_scaler = StandardScaler()
        elif self.settings.SCALING_METHOD == _settings.ScalingChoice.ROBUSTSCALER:
            self._feature_scaler = RobustScaler(unit_variance=True)
            self._y_scaler = RobustScaler(unit_variance=True)

        self._T_edge_bin_coeffs = None    # TODO: this needs to be exported in serialization

        self._model = ElasticNet(
            alpha=self.settings.ELASTICNET.ALPHA,
            l1_ratio=self.settings.ELASTICNET.L1_RATIO,
            fit_intercept=self.settings.ELASTICNET.FIT_INTERCEPT,
            precompute=self.settings.ELASTICNET.PRECOMPUTE,
            max_iter=self.settings.ELASTICNET.MAX_ITER,
            tol=self.settings.ELASTICNET.TOL,
            selection=self.settings.ELASTICNET.SELECTION,
            random_state=self.settings.ELASTICNET._SEED,
        )

        self._T_bin_edges = None
        self._T_edge_bin_rate = None
        self._df_temporal_clusters = None
        self._ts_features = self.settings._TRAIN_FEATURES.copy()
        self._categorical_features = None
        self._ts_feature_norm = None

        self.is_fit = False
        self.baseline_metrics = None

    def fit(self, baseline_data, ignore_disqualification=False):
        if not isinstance(baseline_data, HourlyBaselineData):
            raise TypeError("baseline_data must be a DailyBaselineData object")
        # TODO check DQ, log warnings
        self._fit(baseline_data)
        return self

    def _fit(self, meter_data):
        # Initialize dataframe
        self.is_fit = False

        # TODO: should we profile later to check if this copy is necessary?
        df_meter = meter_data.df.copy()

        # Prepare feature arrays/matrices
        X_fit, X_predict, y_fit = self._prepare_features(df_meter)

        # fit the model
        self._model.fit(X_fit, y_fit)
        self.is_fit = True

        # get number of model parameters
        num_parameters = np.count_nonzero(self._model.coef_) + np.count_nonzero(
            self._model.intercept_
        )

        # get model prediction of baseline
        df_meter = self._predict(meter_data, X=X_predict)

        # calculate baseline metrics on non-interpolated data
        cols = [col for col in df_meter.columns if col.startswith("interpolated_")]
        interpolated = df_meter[cols].any(axis=1)

        self.baseline_metrics = BaselineMetrics(
            df=df_meter.loc[~interpolated], num_model_params=num_parameters
        )

        return self

    def predict(
        self,
        reporting_data,
        ignore_disqualification=False,
    ):
        """Perform initial sufficiency and typechecks before passing to private predict"""
        if not self.is_fit:
            raise RuntimeError("Model must be fit before predictions can be made.")

        # TODO check DQ, log warnings

        if not isinstance(reporting_data, (HourlyBaselineData, HourlyReportingData)):
            raise TypeError(
                "reporting_data must be a DailyBaselineData or DailyReportingData object"
            )

        df_eval = self._predict(reporting_data)

        return df_eval

    def _predict(self, eval_data, X=None):
        """
        Makes model prediction on given temperature data.

        Parameters:
            df_eval (pandas.DataFrame): The evaluation dataframe.

        Returns:
            pandas.DataFrame: The evaluation dataframe with model predictions added.
        """
        # TODO: same as fit, is copy necessary?
        df_eval = eval_data.df.copy()
        dst_indices = _get_dst_indices(df_eval)
        datetime_original = eval_data.df.index
        # # get list of columns to keep in output
        columns = df_eval.columns.tolist()
        if "datetime" in columns:
            columns.remove("datetime")  # index in output, not column

        if X is None:
            _, X, _ = self._prepare_features(df_eval)

        y_predict_scaled = self._model.predict(X)
        y_predict = self._y_scaler.inverse_transform(y_predict_scaled)
        y_predict = y_predict.flatten()

        y_predict = _transform_dst(y_predict, dst_indices)

        df_eval["predicted"] = y_predict

        # # remove columns not in original columns and predicted
        df_eval = df_eval[[*columns, "predicted"]]

        # reindex to original datetime index
        df_eval = df_eval.reindex(datetime_original)

        return df_eval

    def _prepare_features(self, meter_data):
        """
        Initializes the meter data by performing the following operations:
        - Renames the 'model' column to 'model_old' if it exists
        - Converts the index to a DatetimeIndex if it is not already
        - Adds a 'season' column based on the month of the index using the settings.season dictionary
        - Adds a 'day_of_week' column based on the day of the week of the index
        - Removes any rows with NaN values in the 'temperature' or 'observed' columns
        - Sorts the data by the index
        - Reorders the columns to have 'season' and 'day_of_week' first, followed by the remaining columns

        Parameters:
        - meter_data: A pandas DataFrame containing the meter data

        Returns:
        - A pandas DataFrame containing the initialized meter data
        """
        dst_indices = _get_dst_indices(meter_data)
        initial_index = meter_data.index
        meter_data = self._add_categorical_features(meter_data)
        self._add_supplemental_features(meter_data)

        self._ts_features, self._categorical_features = self._sort_features(
            self._ts_features, 
            self._categorical_features
        )

        meter_data = self._daily_sufficiency(meter_data)
        meter_data = self._normalize_features(meter_data)
        meter_data = self._add_temperature_bin_masked_ts(meter_data)

        # save actual df used for later inspection
        self._ts_feature_norm, _ = self._sort_features(self._ts_feature_norm)
        selected_features = self._ts_feature_norm + self._categorical_features
        if "observed_norm" in meter_data.columns:
            selected_features += ["observed_norm"]
        self._processed_meter_data_full = meter_data
        self._processed_meter_data = self._processed_meter_data_full[selected_features]

        # get feature matrices
        X_predict, _ = self._get_feature_matrices(meter_data, dst_indices)

        if not self.is_fit:
            meter_data = meter_data.set_index(initial_index)
            # remove insufficient days from fit data
            meter_data = meter_data[meter_data["include_date"]]

            # recalculate DST indices with removed days
            dst_indices = _get_dst_indices(meter_data)

            # index shouldn't matter since it's being aggregated on date col inside _get_feature_matrices,
            # but just keeping the input consistent with initial call
            meter_data = meter_data.reset_index()

            X_fit, y_fit = self._get_feature_matrices(meter_data, dst_indices)

        else:
            X_fit, y_fit = None, None

        return X_fit, X_predict, y_fit

    def _add_temperature_bins(self, df):
        # TODO: do we need to do something about empty bins in prediction? I think not but maybe
        settings = self.settings.TEMPERATURE_BIN

        # add temperature bins based on temperature
        if not self.is_fit:
            if settings.METHOD == "equal_sample_count":
                T_bin_edges = pd.qcut(df["temperature"], q=settings.N_BINS, labels=False)

            elif settings.METHOD == "equal_bin_width":
                T_bin_edges = pd.cut(df["temperature"], bins=settings.N_BINS, labels=False)

            elif settings.METHOD == "set_bin_width":
                bin_width = settings.BIN_WIDTH

                min_temp = np.floor(df["temperature"].min())
                max_temp = np.ceil(df["temperature"].max())

                if not settings.INCLUDE_EDGE_BINS:
                    step_num = np.round((max_temp - min_temp) / bin_width).astype(int) + 1

                    # T_bin_edges = np.arange(min_temp, max_temp + bin_width, bin_width)
                    T_bin_edges = np.linspace(min_temp, max_temp, step_num)

                else:
                    set_edge_bin_width = False
                    if set_edge_bin_width:
                        edge_bin_width = bin_width*1/2

                        bin_range = [min_temp + edge_bin_width, max_temp - edge_bin_width]

                    else:
                        edge_bin_count = settings.EDGE_BIN_DAYS

                        # get 5th smallest and 5th largest temperatures
                        sorted_temp = np.sort(df["temperature"].unique())
                        min_temp_reg_bin = np.ceil(sorted_temp[edge_bin_count])
                        max_temp_reg_bin = np.floor(sorted_temp[-edge_bin_count])

                        bin_range = [min_temp_reg_bin, max_temp_reg_bin]

                    step_num = np.round((bin_range[1] - bin_range[0]) / bin_width).astype(int) + 1

                    # create bins with set width
                    T_bin_edges = np.array([min_temp, *np.linspace(*bin_range, step_num), max_temp])
                
            else:
                raise ValueError("Invalid temperature binning method")

            # set the first and last bin to -inf and inf
            T_bin_edges[0] = -np.inf
            T_bin_edges[-1] = np.inf

            # store bin edges for prediction
            self._T_bin_edges = T_bin_edges

        T_bins = pd.cut(df["temperature"], bins=self._T_bin_edges, labels=False)

        df["temp_bin"] = T_bins

        # Create dummy variables for temperature bins
        bin_dummies = pd.get_dummies(
            pd.Categorical(
                df["temp_bin"], categories=range(len(self._T_bin_edges) - 1)
            ),
            prefix="temp_bin",
        )
        bin_dummies.index = df.index

        col_names = bin_dummies.columns.tolist()
        df = pd.merge(df, bin_dummies, how="left", left_index=True, right_index=True)

        return df, col_names
    
    def _add_categorical_features(self, df):
        def set_initial_temporal_clusters(df):
            fit_df_grouped = (
                df.groupby(["month", "day_of_week", "hour_of_day"])["observed"]
                .mean()
                .reset_index()
            )
            fit_grouped = fit_df_grouped.groupby(["month", "day_of_week"])[
                "observed"
            ].apply(np.array)

            # convert fit_grouped to 2D numpy array
            X = np.stack(fit_grouped.values, axis=0)

            settings = self.settings.TEMPORAL_CLUSTER
            labels = cluster_temporal_features(
                X,
                settings.WAVELET_N_LEVELS,
                settings.WAVELET_NAME,
                settings.WAVELET_MODE, 
                settings.PCA_MIN_VARIANCE_RATIO_EXPLAINED, 
                settings.RECLUSTER_COUNT, 
                settings.N_CLUSTER_LOWER, 
                settings.N_CLUSTER_UPPER, 
                settings.SCORE_METRIC, 
                settings.DISTANCE_METRIC, 
                settings.MIN_CLUSTER_SIZE, 
                settings._SEED
            )

            df_temporal_clusters = pd.DataFrame(
                labels,
                columns=["temporal_cluster"],
                index=fit_grouped.index,
            )

            return df_temporal_clusters

        def correct_missing_temporal_clusters(df):
            # check and match any missing temporal combinations

            # get all unique combinations of month and day_of_week in df
            df_temporal = df[["month", "day_of_week"]].drop_duplicates()
            df_temporal = df_temporal.sort_values(["month", "day_of_week"])
            df_temporal_index = df_temporal.set_index(["month", "day_of_week"]).index

            # reindex self.df_temporal_clusters to df_temporal_index
            df_temporal_clusters = self._df_temporal_clusters.reindex(df_temporal_index)

            # get index of any nan values in df_temporal_clusters
            missing_combinations = df_temporal_clusters[
                df_temporal_clusters["temporal_cluster"].isna()
            ].index
            if not missing_combinations.empty:
                # TODO: this assumes that observed has values in df and not all null
                if "observed" in df.columns:
                    # filter df to only include missing combinations
                    df_missing = df[
                        df.set_index(["month", "day_of_week"]).index.isin(
                            missing_combinations
                        )
                    ]

                    df_missing_grouped = (
                        df_missing.groupby(["month", "day_of_week", "hour_of_day"])["observed"]
                        .mean()
                        .reset_index()
                    )
                    df_missing_grouped = df_missing_grouped.groupby(
                        ["month", "day_of_week"]
                    )["observed"].apply(np.array)

                    # convert fit_grouped to 2D numpy array
                    X = np.stack(df_missing_grouped.values, axis=0)

                    # calculate average observed for known clusters
                    # join df_temporal_clusters to df on month and day_of_week
                    df = pd.merge(
                        df,
                        df_temporal_clusters,
                        how="left",
                        left_on=["month", "day_of_week"],
                        right_index=True,
                    )

                    df_known = df[
                        ~df.set_index(["month", "day_of_week"]).index.isin(
                            missing_combinations
                        )
                    ]

                    df_known_groupby = df_known.groupby(
                        ["month", "day_of_week", "hour_of_day"]
                    )["observed"]
                    df_known_mean = df_known_groupby.mean().reset_index()
                    df_known_mean = df_known_mean.groupby(["month", "day_of_week"])[
                        "observed"
                    ].apply(np.array)

                    # get temporal clusters df_known
                    temporal_clusters = df_known.groupby(["month", "day_of_week"])[
                        "temporal_cluster"
                    ].first()
                    temporal_clusters = temporal_clusters.reindex(df_known_mean.index)

                    X_known = np.stack(df_known_mean.values, axis=0)

                    # get smallest distance between X and X_known
                    dist = cdist(X, X_known, metric="euclidean")
                    min_dist_idx = np.argmin(dist, axis=1)

                    # set labels to minimum distance of known clusters
                    labels = temporal_clusters.iloc[min_dist_idx].values
                    df_temporal_clusters.loc[
                        missing_combinations, "temporal_cluster"
                    ] = labels

                    self._df_temporal_clusters = df_temporal_clusters

                else:
                    # TODO: There's better ways of handling this
                    # unstack and fill missing days in each month
                    # assuming months more important than days
                    df_temporal_clusters = df_temporal_clusters.unstack()

                    # fill missing days in each month
                    df_temporal_clusters = df_temporal_clusters.ffill(axis=1)
                    df_temporal_clusters = df_temporal_clusters.bfill(axis=1)

                    # fill missing months if any remaining empty
                    df_temporal_clusters = df_temporal_clusters.ffill(axis=0)
                    df_temporal_clusters = df_temporal_clusters.bfill(axis=0)

                    df_temporal_clusters = df_temporal_clusters.stack()

            return df_temporal_clusters

        # assign basic temporal features
        df["date"] = df.index.date
        df["month"] = df.index.month
        df["day_of_week"] = df.index.dayofweek
        df["hour_of_day"] = df.index.hour

        # assign temporal clusters
        if not self.is_fit:
            self._df_temporal_clusters = set_initial_temporal_clusters(df)
        else:
            self._df_temporal_clusters = correct_missing_temporal_clusters(df)

        # join df_temporal_clusters to df
        df = pd.merge(
            df,
            self._df_temporal_clusters,
            how="left",
            left_on=["month", "day_of_week"],
            right_index=True,
        )
        n_clusters = self._df_temporal_clusters["temporal_cluster"].nunique()

        cluster_dummies = pd.get_dummies(
            pd.Categorical(df["temporal_cluster"], categories=range(n_clusters)),
            prefix="temporal_cluster",
        )
        cluster_dummies.index = df.index

        cluster_cat = [f"temporal_cluster_{i}" for i in range(n_clusters)]
        self._categorical_features = cluster_cat

        df = pd.merge(
            df, cluster_dummies, how="left", left_index=True, right_index=True
        )

        if self.settings.TEMPERATURE_BIN is not None:
            df, temp_bin_cols = self._add_temperature_bins(df)
            self._categorical_features.extend(temp_bin_cols)

        return df

    def _add_supplemental_features(self, df):
        # TODO: should either do upper or lower on all strs
        if self.settings.SUPPLEMENTAL_TIME_SERIES_COLUMNS is not None:
            for col in self.settings.SUPPLEMENTAL_TIME_SERIES_COLUMNS:
                if (col in df.columns) and (col not in self._ts_features):
                    self._ts_features.append(col)

        if self.settings.SUPPLEMENTAL_CATEGORICAL_COLUMNS is not None:
            for col in self.settings.SUPPLEMENTAL_CATEGORICAL_COLUMNS:
                if (
                    (col in df.columns)
                    and (col not in self._ts_features)
                    and (col not in self._categorical_features)
                ):
                    self._categorical_features.append(col)

    def _sort_features(self, ts_features=None, cat_features=None):
        features = {"ts": ts_features, "cat": cat_features}

        # sort features
        for _type in ["ts", "cat"]:
            feat = features[_type]

            if feat is not None:
                sorted_cols = []
                for col in self._priority_cols[_type]:
                    cat_cols = [c for c in feat if c.startswith(col)]
                    sorted_cols.extend(sorted(cat_cols))

                # get all columns in self._categorical_feature not in sorted_cat_cols
                leftover_cols = [c for c in feat if c not in sorted_cols]
                if leftover_cols:
                    sorted_cols.extend(sorted(leftover_cols))

                features[_type] = sorted_cols

        return features["ts"], features["cat"]

    # TODO rename to avoid confusion with data sufficiency
    def _daily_sufficiency(self, df):
        # remove days with insufficient data
        min_hours = self.settings.MIN_DAILY_TRAINING_HOURS

        if min_hours > 0:
            # find any rows with interpolated data
            cols = [col for col in df.columns if col.startswith("interpolated_")]
            df["interpolated"] = df[cols].any(axis=1)

            # if row contains any null values, set interpolated to True
            df["interpolated"] = df["interpolated"] | df.isnull().any(axis=1)

            # count number of non interpolated hours per day
            daily_hours = 24 - df.groupby("date")["interpolated"].sum()
            sufficient_days = daily_hours[daily_hours >= min_hours].index

            # set "include_day" column to True if day has sufficient hours
            df["include_date"] = df["date"].isin(sufficient_days)

        else:
            df["include_date"] = True

        return df

    def _normalize_features(self, df):
        """ """
        train_features = self._ts_features
        self._ts_feature_norm = [i + "_norm" for i in train_features]

        # need to set scaler if not fit
        if not self.is_fit:
            self._feature_scaler.fit(df[train_features])
            self._y_scaler.fit(df["observed"].values.reshape(-1, 1))

        data_transformed = self._feature_scaler.transform(df[train_features])
        normalized_df = pd.DataFrame(
            data_transformed, index=df.index, columns=self._ts_feature_norm
        )

        df = pd.concat([df, normalized_df], axis=1)

        if "observed" in df.columns:
            df["observed_norm"] = self._y_scaler.transform(
                df["observed"].values.reshape(-1, 1)
            )

        return df

    def _add_temperature_bin_masked_ts(self, df):
        settings = self.settings.TEMPERATURE_BIN

        def get_k(int_col, a, b):
            k = []
            for hour in range(24):
                df_hour = df[df["hour_of_day"] == hour]
                df_hour = df_hour.sort_values(by=int_col)
                
                x_data = a*df_hour[int_col].values + b
                y_data = df_hour["observed"].values
                
                # Fit the model using robust least squares
                try:
                    params = fit_exp_growth_decay(x_data, y_data, k_only=True, is_x_sorted=True)
                    # save k for each hour
                    k.append(params[2])
                except:
                    pass

            k = np.abs(np.array(k))
            k = np.mean(k[k < 5])

            return k

        # TODO: if this permanent then it should not create, erase, make anew
        self._ts_feature_norm.remove("temperature_norm")

        # get all the temp_bin columns
        # get list of columns beginning with "daily_temp_" and ending in a number
        for interaction_col in ["temp_bin_", "temporal_cluster_"]:
            cols = [col for col in df.columns if col.startswith(interaction_col) and col[-1].isdigit()]
            for col in cols:
                # splits temperature_norm into unique columns if that temp_bin column is True
                ts_col = f"{col}_ts"
                df[ts_col] = df["temperature_norm"] * df[col]

                self._ts_feature_norm.append(ts_col)

        # TODO: if this is permanent then it should be a function, not this mess
        if settings.INCLUDE_EDGE_BINS:
            if self._T_edge_bin_coeffs is None:
                self._T_edge_bin_coeffs = {}

            cols = [col for col in df.columns if col.startswith("temp_bin_") and col[-1].isdigit()]
            cols = [0, int(cols[-1].replace("temp_bin_", ""))]
            # maybe add nonlinear terms to second and second to last columns?
            # cols = [0, 1, last_temp_bin - 1, last_temp_bin]
            # cols = list(set(cols))
            # all columns?
            # cols = range(cols[0], cols[1] + 1)
            
            for n in cols:
                base_col = f"temp_bin_{n}"
                int_col = f"{base_col}_ts"
                T_col = f"{base_col}_T"

                # get k for exponential growth/decay
                if not self.is_fit:
                    # determine temperature conversion for bin
                    range_offset = settings.EDGE_BIN_TEMPERATURE_RANGE_OFFSET
                    T_range = [df[int_col].min() - range_offset, df[int_col].max() + range_offset]
                    new_range = [-4, 4]

                    T_a = (new_range[1] - new_range[0])/(T_range[1] - T_range[0])
                    T_b = new_range[1] - T_a*T_range[1]

                    # The best rate for exponential
                    if settings.EDGE_BIN_RATE == "heuristic":
                        k = get_k(int_col, T_a, T_b)
                    else:
                        k = settings.EDGE_BIN_RATE

                    # get A for exponential
                    A = 1/(np.exp(1/k*new_range[1]) - 1)

                    self._T_edge_bin_coeffs[n] = {
                        "T_a": T_a,
                        "T_b": T_b,
                        "k": k,
                        "A": A,
                    }

                T_a = self._T_edge_bin_coeffs[n]["T_a"]
                T_b = self._T_edge_bin_coeffs[n]["T_b"]
                k = self._T_edge_bin_coeffs[n]["k"]
                A = self._T_edge_bin_coeffs[n]["A"]

                df[T_col] = 0
                df.loc[df[base_col], T_col] = T_a*df[int_col] + T_b # doing this multiple times in get_k and here

                for pos_neg in ["pos", "neg"]:
                    # if first or last column, add additional column
                    # testing exp, previously squaring worked well

                    s = 1
                    if "neg" in pos_neg:
                        s = -1

                    # set rate exponential
                    ts_col = f"{base_col}_{pos_neg}_exp_ts"

                    df[ts_col] = 0
                    df.loc[df[base_col], ts_col] = A*np.exp(s/k*df[T_col]) - A

                    self._ts_feature_norm.append(ts_col)

        return df

    def _get_feature_matrices(self, df, dst_indices):
        # get aggregated features with agg function
        agg_dict = {f: lambda x: list(x) for f in self._ts_feature_norm}

        def correct_dst(agg):
            """interpolate or average hours to account for DST. modifies in place"""
            interp, mean = dst_indices
            for date, hour in interp:
                for feature_idx, feature in enumerate(agg[date]):
                    if hour == 0:
                        # there are a handful of countries that use 0:00 as the DST transition
                        interpolated = (
                            agg[date - 1][feature_idx][-1] + feature[hour]
                        ) / 2
                    else:
                        interpolated = (feature[hour - 1] + feature[hour]) / 2
                    feature.insert(hour, interpolated)
            for date, hour in mean:
                for feature in agg[date]:
                    mean = (feature[hour + 1] + feature.pop(hour)) / 2
                    feature[hour] = mean

        agg_x = df.groupby("date").agg(agg_dict).values.tolist()
        correct_dst(agg_x)

        # get the features and target for each day
        ts_feature = np.array(agg_x)

        ts_feature = ts_feature.reshape(
            ts_feature.shape[0], ts_feature.shape[1] * ts_feature.shape[2]
        )

        # get the first categorical features for each day for each sample
        unique_dummies = (
            df[self._categorical_features + ["date"]].groupby("date").first()
        )

        X = np.concatenate((ts_feature, unique_dummies), axis=1)

        if not self.is_fit:
            agg_y = (
                df.groupby("date")
                .agg({"observed_norm": lambda x: list(x)})
                .values.tolist()
            )
            correct_dst(agg_y)
            y = np.array(agg_y)
            y = y.reshape(y.shape[0], y.shape[1] * y.shape[2])

        else:
            y = None

        return X, y

    def to_dict(self):
        feature_scaler = {}
        if self.settings.SCALING_METHOD == _settings.ScalingChoice.STANDARDSCALER:
            for i, key in enumerate(self._ts_features):
                feature_scaler[key] = [
                    self._feature_scaler.mean_[i],
                    self._feature_scaler.scale_[i],
                ]

            y_scaler = [self._y_scaler.mean_, self._y_scaler.scale_]
            
        elif self.settings.SCALING_METHOD == _settings.ScalingChoice.ROBUSTSCALER:
            for i, key in enumerate(self._ts_features):
                feature_scaler[key] = [
                    self._feature_scaler.center_[i],
                    self._feature_scaler.scale_[i],
                ]

            y_scaler = [self._y_scaler.center_, self._y_scaler.scale_]

        # convert self._df_temporal_clusters to list of lists
        df_temporal_clusters = self._df_temporal_clusters.reset_index().values.tolist()
        
        params = _settings.SerializeModel(
            SETTINGS=self.settings,
            TEMPORAL_CLUSTERS=df_temporal_clusters,
            TEMPERATURE_BIN_EDGES=self._T_bin_edges,
            TS_FEATURES=self._ts_features,
            CATEGORICAL_FEATURES=self._categorical_features,
            COEFFICIENTS=self._model.coef_.tolist(),
            INTERCEPT=self._model.intercept_.tolist(),
            FEATURE_SCALER=feature_scaler,
            CATAGORICAL_SCALER=None,
            Y_SCALER=y_scaler,
            BASELINE_METRICS=self.baseline_metrics,
        )

        return params.model_dump()

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data):
        # get settings
        train_features = data.get("SETTINGS").get("TRAIN_FEATURES")

        if "ghi" in train_features:
            settings = _settings.HourlySolarSettings(**data.get("SETTINGS"))
        else:
            settings = _settings.HourlyNonSolarSettings(**data.get("SETTINGS"))

        # initialize model class
        model_cls = cls(settings=settings)

        df_temporal_clusters = pd.DataFrame(
            data.get("TEMPORAL_CLUSTERS"),
            columns=["month", "day_of_week", "temporal_cluster"],
        ).set_index(["month", "day_of_week"])

        model_cls._df_temporal_clusters = df_temporal_clusters
        model_cls._T_bin_edges = np.array(data.get("TEMPERATURE_BIN_EDGES"))

        model_cls._ts_features = data.get("TS_FEATURES")
        model_cls._categorical_features = data.get("CATEGORICAL_FEATURES")

        # set scalers
        feature_scaler_values = list(data.get("FEATURE_SCALER").values())
        feature_scaler_loc = [i[0] for i in feature_scaler_values]
        feature_scaler_scale = [i[1] for i in feature_scaler_values]

        y_scaler_values = data.get("Y_SCALER")

        if settings.SCALING_METHOD == _settings.ScalingChoice.STANDARDSCALER:
            model_cls._feature_scaler.mean_ = np.array(feature_scaler_loc)
            model_cls._feature_scaler.scale_ = np.array(feature_scaler_scale)

            model_cls._y_scaler.mean_ = np.array(y_scaler_values[0])
            model_cls._y_scaler.scale_ = np.array(y_scaler_values[1])

        elif settings.SCALING_METHOD == _settings.ScalingChoice.ROBUSTSCALER:
            model_cls._feature_scaler.center_ = np.array(feature_scaler_loc)
            model_cls._feature_scaler.scale_ = np.array(feature_scaler_scale)

            model_cls._y_scaler.center_ = np.array(y_scaler_values[0])
            model_cls._y_scaler.scale_ = np.array(y_scaler_values[1])
        
        # set model
        model_cls._model.coef_ = np.array(data.get("COEFFICIENTS"))
        model_cls._model.intercept_ = np.array(data.get("INTERCEPT"))

        model_cls.is_fit = True

        # set baseline metrics
        model_cls.baseline_metrics = BaselineMetricsFromDict(
            data.get("BASELINE_METRICS")
        )

        return model_cls

    @classmethod
    def from_json(cls, str_data):
        return cls.from_dict(json.loads(str_data))

    def plot(
        self,
        df_eval,
        ax=None,
        title=None,
        figsize=None,
        temp_range=None,
    ):
        """Plot a model fit.

        Parameters
        ----------
        ax : :any:`matplotlib.axes.Axes`, optional
            Existing axes to plot on.
        title : :any:`str`, optional
            Chart title.
        figsize : :any:`tuple`, optional
            (width, height) of chart.
        with_candidates : :any:`bool`
            If True, also plot candidate models.
        temp_range : :any:`tuple`, optionl
            Temperature range to plot

        Returns
        -------
        ax : :any:`matplotlib.axes.Axes`
            Matplotlib axes.
        """
        raise NotImplementedError


class _LabelResult(BaseModel):
    """
    contains metrics about a cluster label returned from sklearn
    """
    class Config:
        arbitrary_types_allowed = True

    labels: np.ndarray
    score: float
    score_unable_to_be_calculated: bool
    n_clusters: int


def cluster_time_series(
    data: np.ndarray,
    recluster_count: int,
    n_cluster_lower: int,
    n_cluster_upper: int,
    score_choice: str,
    dist_metric: str,
    min_cluster_size: int,
    seed: int,
):
    """
    clusters the temporal features of the dataframe
    """
    max_non_outlier_cluster_count = 200

    results = []
    for i in range(recluster_count):
        algo = _bisect_k_means.BisectingKMeans(
            n_clusters=n_cluster_upper,
            init="k-means++",  # does not benefit from k-means++ like other k-means
            n_init=5,  # default is 1
            random_state=seed + i,  # can be set to None or seed_num
            algorithm="elkan",  # ['lloyd', 'elkan']
            bisecting_strategy="largest_cluster",  # ['biggest_inertia', 'largest_cluster']
        )
        algo.fit(data)
        labels_dict = algo.labels_full

        for n_cluster, labels in labels_dict.items():
            score, score_unable_to_be_calculated = _scoring.score_clusters(
                data,
                labels,
                n_cluster_lower,
                score_choice,
                dist_metric,
                min_cluster_size,
                max_non_outlier_cluster_count,
            )

            label_res = _LabelResult(
                labels=labels,
                score=score,
                score_unable_to_be_calculated=score_unable_to_be_calculated,
                n_clusters=n_cluster,
            )
            results.append(label_res)

    # get the results index with the smallest score
    HoF = None
    for result in results:
        if result.score_unable_to_be_calculated:
            continue

        if HoF is None or result.score < HoF.score:
            HoF = result

    return HoF.labels

def cluster_temporal_features(
    data: np.ndarray,
    wavelet_n_levels: int,
    wavelet_name: str,
    wavelet_mode: str,
    min_var_ratio: float,
    recluster_count: int,
    n_cluster_lower: int,
    n_cluster_upper: int,
    score_choice: str,
    dist_metric: str,
    min_cluster_size: int,
    seed: int,
):
    def _dwt_coeffs(data, wavelet='db1', wavelet_mode="periodization", n_levels=4):
        all_features = []
        # iterate through rows of numpy array
        for row in range(len(data)):
            decomp_coeffs = pywt.wavedec(data[row], wavelet=wavelet, mode=wavelet_mode, level=n_levels)
            # remove last level
            # if n_levels > 4:
            # decomp_coeffs = decomp_coeffs[:-1]

            decomp_coeffs = np.hstack(decomp_coeffs)

            all_features.append(decomp_coeffs)

        return np.vstack(all_features)

    def _pca_coeffs(features, min_var_ratio=0.95):
        # standardize the features
        features = StandardScaler().fit_transform(features)

        use_kernel_pca = False
        if use_kernel_pca:
            pca = KernelPCA(n_components=None, kernel='rbf')
            pca_features = pca.fit_transform(features)

            explained_variance_ratio = pca.eigenvalues_ / np.sum(pca.eigenvalues_)

            # get the cumulative explained variance ratio
            cumulative_explained_variance = np.cumsum(explained_variance_ratio)

            # find number of components that explain pct% of the variance
            n_components = np.argmax(cumulative_explained_variance > min_var_ratio)

            # pca = PCA(n_components=n_components)
            pca = KernelPCA(n_components=n_components, kernel='rbf')
            pca_features = pca.fit_transform(features)

        else:
            pca = PCA(n_components=min_var_ratio)
            pca_features = pca.fit_transform(features)

        return pca_features
    
    # calculate wavelet coefficients
    features = _dwt_coeffs(data, wavelet_name, wavelet_mode, wavelet_n_levels)
    pca_features = _pca_coeffs(features, min_var_ratio)

    # cluster the pca features
    cluster_labels = cluster_time_series(
        pca_features,
        recluster_count,
        n_cluster_lower,
        n_cluster_upper,
        score_choice,
        dist_metric,
        min_cluster_size,
        seed,
    )

    return cluster_labels


def fit_exp_growth_decay(x, y, k_only=True, is_x_sorted=False):
    # Courtsey: https://math.stackexchange.com/questions/1337601/fit-exponential-with-constant
    #           https://www.scribd.com/doc/14674814/Regressions-et-equations-integrales
    #           Jean Jacquelin

    # fitting function is actual b*exp(c*x) + a

    # sort x in order
    x = np.array(x)
    y = np.array(y)
    n = len(x)

    if not is_x_sorted:
        sort_idx = np.argsort(x)
        x = x[sort_idx]
        y = y[sort_idx]

    s = [0]
    for i in range(1, len(x)):
        s.append(s[i-1] + 0.5*(y[i] + y[i-1])*(x[i] - x[i-1]))

    s = np.array(s)
    
    x_diff_sq = np.sum((x - x[0])**2)
    xs_diff = np.sum(s*(x - x[0]))
    s_sq = np.sum(s**2)
    xy_diff = np.sum((x - x[0])*(y - y[0]))
    ys_diff = np.sum(s*(y - y[0]))

    A = np.array([[x_diff_sq, xs_diff], [xs_diff, s_sq]])
    b = np.array([xy_diff, ys_diff])

    _, c = np.linalg.solve(A, b)
    k = 1/c

    if k_only:
        a, b = None, None
    else:
        theta_i = np.exp(c*x)

        theta = np.sum(theta_i)
        theta_sq = np.sum(theta_i**2)
        y_sum = np.sum(y)
        y_theta = np.sum(y*theta_i)

        A = np.array([[n, theta], [theta, theta_sq]])
        b = np.array([y_sum, y_theta])

        a, b = np.linalg.solve(A, b)

    return a, b, k


def _get_dst_indices(df):
    """
    given a datetime-indexed dataframe,
    return the indices which need to be interpolated and averaged
    in order to ensure exact 24 hour slots
    """
    # TODO test on baselines that begin/end on DST change
    counts = df.groupby(df.index.date).count()
    interp = counts[counts["observed"] == 23]
    mean = counts[counts["observed"] == 25]

    interp_idx = []
    for idx in interp.index:
        month = df.loc[idx.isoformat()]
        date_idx = counts.index.get_loc(idx)
        missing_hour = set(range(24)) - set(month.index.hour)
        if len(missing_hour) != 1:
            raise ValueError("too many missing hours")
        hour = missing_hour.pop()
        interp_idx.append((date_idx, hour))

    mean_idx = []
    for idx in mean.index:
        date_idx = counts.index.get_loc(idx)
        month = df.loc[idx.isoformat()]
        seen = set()
        for i in month.index:
            if i.hour in seen:
                hour = i.hour
                break
            seen.add(i.hour)
        mean_idx.append((date_idx, hour))

    return interp_idx, mean_idx


def _transform_dst(prediction, dst_indices):
    interp, mean = dst_indices

    START_END = 0
    REMOVE = 1
    INTERPOLATE = 2

    # get concrete indices
    remove_idx = [(REMOVE, date * 24 + hour) for date, hour in interp]
    interp_idx = [(INTERPOLATE, date * 24 + hour + 1) for date, hour in mean]

    # these values will be inserted for the 25th hour
    interpolated_vals = []
    for _, idx in interp_idx:
        interpolated = (prediction[idx - 1] + prediction[idx]) / 2
        interpolated_vals.append(interpolated)
    interpolation = iter(interpolated_vals)

    # sort "operations" by index (can't assume a strict back-and-forth ordering)
    ops = sorted(remove_idx + interp_idx, key=lambda t: t[1])

    # create fenceposts where slices end
    pairs = list(zip([(START_END, 0)] + ops, ops + [(START_END, None)]))
    slices = []
    for start, end in pairs:
        start_i = start[1]
        end_i = end[1]
        if start[0] == REMOVE:
            start_i += 1
        if start[0] == INTERPOLATE:
            slices.append([next(interpolation)])
        slices.append(prediction[slice(start_i, end_i)])
    return np.concatenate(slices)

    ## the block above is equivalent to:
    # shift = 0
    # for op in ops:
    #     if op[0] == REMOVE:
    #         # delete artificial DST hour
    #         idx = op[1] + shift
    #         prediction = np.delete(prediction, idx)
    #         shift -= 1
    #     if op[0] == INTERPOLATE:
    #         # interpolate missing DST hour
    #         idx = op[1] + shift
    #         interp = (prediction[idx - 1] + prediction[idx]) / 2
    #         prediction = np.insert(prediction, idx, interp)
    #         shift += 1
    # return prediction
