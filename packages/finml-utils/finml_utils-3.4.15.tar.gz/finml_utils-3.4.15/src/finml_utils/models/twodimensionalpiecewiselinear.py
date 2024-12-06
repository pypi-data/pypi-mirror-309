from typing import Literal

import numpy as np
import pandas as pd
from sklearn.preprocessing import QuantileTransformer
from sklearn.svm import LinearSVC, LinearSVR

from .utils import (
    calc_deciles_to_split,
    calculate_1d_bin_diff,
    calculate_2d_bin_diff,
)
from sklearn.base import BaseEstimator,ClassifierMixin,MultiOutputMixin,TransformerMixin


class TwoDimensionalPiecewiseLinearRegression(
    BaseEstimator, ClassifierMixin, MultiOutputMixin
):
    def __init__(
        self,
        # used to produce the range of deciles/percentiles when the model can split, 0.1 means the range is 0.4 to 0.6 percentile.
        exogenous_threshold_margin: float,
        endogenous_threshold_margin: float,
        # used to produce the range of deciles/percentiles when the model can split, 0.05 means the possible splits will be spaced 5% apart
        exogenous_threshold_step: float,
        endogenous_threshold_step: float,
        # if True, the model determines the optimal sign of the "coefficient", if False, positive_class == 1
        exogenous_determine_positive_class_automatically: bool,
        endogenous_determine_positive_class_automatically: bool,
        # number of extra splits to make around the best split, eg. if 2 and the best quantile is 0.5, then the splits will be [0.45, 0.5, 0.55]
        exogenous_num_splits: int = 4,
        endogenous_num_splits: int = 4,
        aggregate_func: Literal["mean", "sharpe"] = "mean",
    ):
        self.aggregate_func = aggregate_func
        assert (
            exogenous_threshold_margin <= 0.4
        ), f"{exogenous_threshold_margin=} too large (> 0.4)"
        assert (
            endogenous_threshold_margin <= 0.4
        ), f"{endogenous_threshold_margin=} too large (> 0.4)"
        assert (
            0 <= exogenous_threshold_step <= 0.05
        ), f"{exogenous_threshold_step=} too large (> 0.05) or negative"
        assert (
            0 <= endogenous_threshold_step <= 0.05
        ), f"{endogenous_threshold_step=} too large (> 0.05) or negative"
        self.exogenous_determine_positive_class_automatically = (
            exogenous_determine_positive_class_automatically
        )
        self.endogenous_determine_positive_class_automatically = (
            endogenous_determine_positive_class_automatically
        )
        self.exogenous_num_splits = exogenous_num_splits
        self.endogenous_num_splits = endogenous_num_splits
        self.exogenous_threshold_margin = exogenous_threshold_margin
        self.endogenous_threshold_margin = endogenous_threshold_margin
        self.exogenous_threshold_step = exogenous_threshold_step
        self.endogenous_threshold_step = endogenous_threshold_step

        if exogenous_threshold_margin > 0:
            exogenous_threshold_start = max(0.0, 0.5 - exogenous_threshold_margin)
            exogenous_threshold_stop = min(1.0, 0.5 + exogenous_threshold_margin) + 0.0001

            self.exogenous_thresholds_to_test = (
                np.arange(
                    exogenous_threshold_start,
                    exogenous_threshold_stop,
                    self.exogenous_threshold_step,
                )
                .round(3)
                .tolist()
            )
        else:
            self.exogenous_thresholds_to_test = [0.5]

        if endogenous_threshold_margin > 0:
            endogenous_threshold_start = max(0.0, 0.5 - endogenous_threshold_margin)
            endogenous_threshold_stop = min(1.0, 0.5 + endogenous_threshold_margin) + 0.0001

            self.endogenous_thresholds_to_test = (
                np.arange(
                    endogenous_threshold_start,
                    endogenous_threshold_stop,
                    self.endogenous_threshold_step,
                )
                .round(3)
                .tolist()
            )
        else:
            self.endogenous_thresholds_to_test = [0.5]

        self._exogenous_splits = None
        self._endogenous_splits = None

        # Here, "positive class" is used in SKLearn terms for binary classification
        self._exogenous_positive_class: int | None = None
        self._endogenous_positive_class: int | None = None

    def fit(  # noqa: PLR0912
        self, X: np.ndarray, y: np.ndarray, sample_weight: np.ndarray | None = None
    ):
        assert X.shape[1] == 2, "Exactly two features are supported"
        self._exogenous_X_col = 0
        self._endogenous_X_col = 1

        # assert (
        #     X[:, self._exogenous_X_col].var() != 0
        # ), f"{self._exogenous_X_col=} has no variance"
        # assert (
        #     X[:, self._endogenous_X_col].var() != 0
        # ), f"{self._endogenous_X_col=} has no variance"

        exogenous_splits = np.quantile(
            X[:, self._exogenous_X_col],
            self.exogenous_thresholds_to_test,
            axis=0,
            method="closest_observation",
        )
        endogenous_splits = np.quantile(
            X[:, self._endogenous_X_col],
            self.endogenous_thresholds_to_test,
            axis=0,
            method="closest_observation",
        )

        exogenous_best_split_idx = None
        endogenous_best_split_idx = None
        highest_abs_difference = -10_000

        for exogenous_split_idx, exogenous_split in enumerate(exogenous_splits):
            # It could be that the best split comes from considering only the first column in X, not both.
            exogenous_difference = calculate_1d_bin_diff(
                exogenous_split,
                X=X[:, self._exogenous_X_col],
                y=y,
                agg_method=self.aggregate_func,
            )

            if abs(exogenous_difference) > highest_abs_difference:
                highest_abs_difference = abs(exogenous_difference)
                exogenous_best_split_idx = exogenous_split_idx
                endogenous_best_split_idx = None

            # It could be that the best split comes from considering both columns in X.
            for endogenous_split_idx, endogenous_split in enumerate(endogenous_splits):
                differences = calculate_2d_bin_diff(
                    quantile_exogenous=exogenous_split,
                    quantile_endogenous=endogenous_split,
                    X=X,
                    y=y,
                    agg_method=self.aggregate_func,
                )
                if abs(differences) > highest_abs_difference:
                    highest_abs_difference = abs(differences)
                    exogenous_best_split_idx = exogenous_split_idx
                    endogenous_best_split_idx = endogenous_split_idx

        if exogenous_best_split_idx is None and endogenous_best_split_idx is None:
            self._exogenous_splits = [exogenous_splits[0]]
            self._endogenous_splits = [endogenous_splits[0]]
            return

        if self.exogenous_determine_positive_class_automatically:
            diff = calculate_1d_bin_diff(
                self.exogenous_thresholds_to_test[exogenous_best_split_idx],
                X=-X[:, self._exogenous_X_col],
                y=y,
                agg_method=self.aggregate_func,
            )
            self._exogenous_positive_class = 1 if diff > 0 else 0
        else:
            self._exogenous_positive_class = 1

        if self.endogenous_determine_positive_class_automatically:
            diff = calculate_1d_bin_diff(
                np.median(X[:, self._endogenous_X_col])
                if endogenous_best_split_idx is None
                else self.endogenous_thresholds_to_test[endogenous_best_split_idx],
                X=-X[:, self._endogenous_X_col],
                y=y,
                agg_method=self.aggregate_func,
            )
            self._endogenous_positive_class = 1 if diff > 0 else 0
        else:
            self._endogenous_positive_class = 1

        exogenous_deciles_to_split = None
        if exogenous_best_split_idx is not None:
            exogenous_deciles_to_split = calc_deciles_to_split(
                best_quantile=self.exogenous_thresholds_to_test[
                    exogenous_best_split_idx
                ],
                num_splits=self.exogenous_num_splits,
            )

        endogenous_deciles_to_split = None
        if endogenous_best_split_idx is not None:
            endogenous_deciles_to_split = calc_deciles_to_split(
                best_quantile=self.endogenous_thresholds_to_test[
                    endogenous_best_split_idx
                ],
                num_splits=self.endogenous_num_splits,
            )

        if exogenous_best_split_idx is None:
            self._exogenous_splits = None
        else:
            self._exogenous_splits = np.quantile(
                X[:, self._exogenous_X_col],
                exogenous_deciles_to_split,
                axis=0,
                method="nearest",
            )  # translate the percentiles into actual values
            assert np.isnan(self._exogenous_splits).sum() == 0

        if endogenous_best_split_idx is None:
            self._endogenous_splits = None
        else:
            self._endogenous_splits = np.quantile(
                X[:, self._endogenous_X_col],
                endogenous_deciles_to_split,
                axis=0,
                method="nearest",
            )  # translate the percentiles into actual values
            assert np.isnan(self._endogenous_splits).sum() == 0

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        assert X.shape[1] == 2, "Exactly two features are supported"
        assert self._exogenous_positive_class is not None, "Model not fitted"
        assert self._endogenous_positive_class is not None, "Model not fitted"
        assert (
            self._exogenous_splits is not None or self._endogenous_splits is not None
        ), "Model not fitted"

        if self._exogenous_splits is None:
            exogenous_output = None
        else:
            exogenous_output = np.searchsorted(
                self._exogenous_splits,
                X[:, self._exogenous_X_col],
                side="right",
            ) / len(self._exogenous_splits)
            if self._exogenous_positive_class == 0:
                exogenous_output = 1 - exogenous_output

        if self._endogenous_splits is None:
            endogenous_output = None
        else:
            endogenous_output = np.searchsorted(
                self._endogenous_splits,
                X[:, self._endogenous_X_col],
                side="right",
            ) / len(self._endogenous_splits)
            if self._endogenous_positive_class == 0:
                endogenous_output = 1 - endogenous_output

        if exogenous_output is not None and endogenous_output is not None:
            output = (exogenous_output + endogenous_output) / 2
        elif exogenous_output is not None:
            output = exogenous_output
        else:  # endogenous_output is not None
            output = endogenous_output

        return output


class TwoDimensionalPiecewiseLinearSupportVector(
    BaseEstimator, ClassifierMixin, MultiOutputMixin, TransformerMixin
):
    def __init__(
        self,
        # Ignore threshold margins for now.
        # used to produce the range of deciles/percentiles when the model can split, 0.1 means the range is 0.4 to 0.6 percentile.
        # exogenous_threshold_margin: float,
        # endogenous_threshold_margin: float,
        # used to produce the range of deciles/percentiles when the model can split, 0.05 means the possible splits will be spaced 5% apart
        exogenous_threshold_step: float,
        endogenous_threshold_step: float,
        # With a linear decision boundary in a (quantized) square of [0, 1] x [0, 1], that is much more likely to be
        # not perpendicular to any axes, the meaning of positive class for endogenous and exogenous data becomes
        # hard to interpret, making any such definition would be artificial and unnecessary.
        # number of extra splits to make around the best split, eg. if 2 and the best quantile is 0.5, then the splits will be [0.45, 0.5, 0.55]
        num_splits: int = 4,
        aggregate_func: Literal["mean", "sharpe"] = "mean",
        is_classification: bool = True,
        C: float = 1.0,
        epsilon: float | None = None,
        penalty: Literal["l1","l2"] | None = None,
        loss: Literal["hinge","squared_hinge","epsilon_insensitive","squared_epsilon_insensitive"] | None = None,
    ):
        self.aggregate_func = aggregate_func
        if is_classification:
            assert epsilon is None, f"Invalid {epsilon=} for {is_classification=}"
            assert penalty is not None, f"Invalid {penalty=} for {is_classification=}"
            assert loss in {"hinge", "squared_hinge"}, f"Invalid {loss=} for {is_classification=}"
        else:
            assert epsilon is not None, f"Invalid {epsilon=} for {is_classification=}"
            assert penalty is None, f"Invalid {penalty=} for {is_classification=}"
            assert loss in {"epsilon_insensitive", "squared_epsilon_insensitive"}, f"Invalid {loss=} for {is_classification=}"

        self.is_classification = is_classification
        self.C = C
        self.epsilon = epsilon
        self.penalty = penalty
        self.loss = loss
        # assert (
        #     exogenous_threshold_margin <= 0.4
        # ), f"{exogenous_threshold_margin=} too large (> 0.4)"
        # assert (
        #     endogenous_threshold_margin <= 0.4
        # ), f"{endogenous_threshold_margin=} too large (> 0.4)"
        assert (
            0 <= exogenous_threshold_step <= 0.05
        ), f"{exogenous_threshold_step=} too large (> 0.05) or negative"
        assert (
            0 <= endogenous_threshold_step <= 0.05
        ), f"{endogenous_threshold_step=} too large (> 0.05) or negative"
        self.n_exogenous_quantiles = int(1 / exogenous_threshold_step)
        self.n_endogenous_quantiles = int(1 / endogenous_threshold_step)
        self.num_splits = num_splits
        # self.exogenous_threshold_margin = exogenous_threshold_margin
        # self.endogenous_threshold_margin = endogenous_threshold_margin
        self.exogenous_threshold_step = exogenous_threshold_step
        self.endogenous_threshold_step = endogenous_threshold_step

        self._exogenous_X_col = 0
        self._endogenous_X_col = 1

        self._exogenous_quantile_transformer = None
        self._endogenous_quantile_transformer = None
        self._model: LinearSVC | LinearSVR | None = None
        self._distances: list[float] | None = None

        self._exogenous_splits = None
        self._endogenous_splits = None

    def transform(self, X: np.ndarray) -> np.ndarray:
        assert X.shape[1] == 2,"Exactly two features are supported"

        exogenous_X = pd.Series(X[:,self._exogenous_X_col]).to_frame()
        endogenous_X = pd.Series(X[:,self._endogenous_X_col]).to_frame()

        # Because the number of quantiles can be different for endogenous and exogenous, using SKLearn Pipeline
        # would be too cumbersome.

        self._exogenous_quantile_transformer = QuantileTransformer(
            n_quantiles=self.n_exogenous_quantiles,output_distribution="uniform",subsample=None,random_state=0
        )
        self._endogenous_quantile_transformer = QuantileTransformer(
            n_quantiles=self.n_endogenous_quantiles,output_distribution="uniform",subsample=None,random_state=0
        )

        transformed_exogenous_X = self._exogenous_quantile_transformer.fit_transform(exogenous_X)
        transformed_endogenous_X = self._endogenous_quantile_transformer.fit_transform(endogenous_X)

        return np.concatenate(
            (
                np.reshape(transformed_exogenous_X,(-1,1)),
                np.reshape(transformed_endogenous_X,(-1,1))
            ),
            axis=1
        )

    def fit(
        self, X: np.ndarray, y: np.ndarray, sample_weight: np.ndarray | None = None
    ):
        if self._exogenous_quantile_transformer is None or self._endogenous_quantile_transformer:
            X = self.transform(X)

        assert self._exogenous_quantile_transformer is not None, "X not transformed"
        assert self._endogenous_quantile_transformer is not None, "X not transformed"

        # Using hinge loss function (vs squared hinge) results in a harder decision boundary
        # which is what we need to minimize the chance of overfitting.
        if self.is_classification:
            self._model = LinearSVC(
                penalty=self.penalty,
                loss=self.loss,
                dual="auto",  # default
                tol=1e-4,  # default
                C=self.C,
                random_state=0,
            )
        else:
            self._model = LinearSVR(
                epsilon=self.epsilon,
                tol=1e-4,  # default
                C=self.C,
                loss=self.loss,
                dual="auto",  # default
                random_state=0,
            )
        # Gross simplification of the true supplied y.
        if self.is_classification:
            negative_y_filter = y < 0
            y[negative_y_filter] = 0
            y[~negative_y_filter] = 1
        else:
            # Min-max scaling.
            y = (y - y.min()) / (y.max() - y.min())
            assert float(y.min()) >= 0, f"y must be >= 0 but {float(y.min())=}"
            assert float(y.max()) <= 1, f"y must be <= 0 but {float(y.max())=}"

        self._model.fit(X,y)
        self._distances = calc_deciles_to_split(best_quantile=0, num_splits=self.num_splits)

    def predict(self, X: np.ndarray) -> np.ndarray:
        assert X.shape[1] == 2, "Exactly two features are supported"
        assert self._model,"Model not fitted"

        transformed_X = self.transform(X)
        if self.is_classification:
            signed_y_pred = self._model.predict(transformed_X)
            signed_y_pred[signed_y_pred < 0] = -1
            signed_y_pred[signed_y_pred >= 0] = 1

            # Calculate distance from the linear decision boundary.
            confidence_scores = self._model.decision_function(transformed_X)
            w_norms = np.linalg.norm(self._model.coef_)
            abs_distances_from_decision_boundary = confidence_scores / w_norms
            distances_from_decision_boundary = (
                abs_distances_from_decision_boundary
                * signed_y_pred
            )

            return (
                np.searchsorted(self._distances, distances_from_decision_boundary, side="right")
                / len(self._distances)
            )

        y_pred = self._model.predict(X)
        y_pred[y_pred < 0] = 0
        y_pred[y_pred > 1] = 1
        return y_pred
