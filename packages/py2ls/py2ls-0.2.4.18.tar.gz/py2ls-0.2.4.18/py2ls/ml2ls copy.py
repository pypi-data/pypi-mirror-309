from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    AdaBoostClassifier,
    BaggingClassifier,
)
from sklearn.svm import SVC, SVR
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.linear_model import (
    LassoCV,
    LogisticRegression,
    LinearRegression,
    Lasso,
    Ridge,
    RidgeClassifierCV,
    ElasticNet,
)
from sklearn.feature_selection import RFE
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import xgboost as xgb  # Make sure you have xgboost installed

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    matthews_corrcoef,
    roc_curve,
    auc,
    balanced_accuracy_score,
    precision_recall_curve,
    average_precision_score,
)
from imblearn.over_sampling import SMOTE
from sklearn.pipeline import Pipeline
from collections import defaultdict
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from typing import Dict, Any, Optional, List, Union
import numpy as np
import pandas as pd
from . import ips
from . import plot
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use(str(ips.get_cwd()) + "/data/styles/stylelib/paper.mplstyle")
import logging
import warnings

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

# Ignore specific warnings (UserWarning in this case)
warnings.filterwarnings("ignore", category=UserWarning)
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier


def features_knn(
    x_train: pd.DataFrame, y_train: pd.Series, knn_params: dict
) -> pd.DataFrame:
    """
    A distance-based classifier that assigns labels based on the majority label of nearest neighbors.
    when to use:
        Effective for small to medium datasets with a low number of features.
        It does not directly provide feature importances but can be assessed through feature permutation or similar methods.
    Recommended Use: Effective for datasets with low feature dimensionality and well-separated clusters.

    Fits KNeighborsClassifier and approximates feature influence using permutation importance.
    """
    knn = KNeighborsClassifier(**knn_params)
    knn.fit(x_train, y_train)
    importances = permutation_importance(
        knn, x_train, y_train, n_repeats=30, random_state=1, scoring="accuracy"
    )
    return pd.DataFrame(
        {"feature": x_train.columns, "importance": importances.importances_mean}
    ).sort_values(by="importance", ascending=False)


#! 1. Linear and Regularized Regression Methods
# 1.1 Lasso
def features_lasso(
    x_train: pd.DataFrame, y_train: pd.Series, lasso_params: dict
) -> np.ndarray:
    """
    Lasso (Least Absolute Shrinkage and Selection Operator):
    A regularized linear regression method that uses L1 penalty to shrink coefficients, effectively
    performing feature selection by zeroing out less important ones.
    """
    lasso = LassoCV(**lasso_params)
    lasso.fit(x_train, y_train)
    # Get non-zero coefficients and their corresponding features
    coefficients = lasso.coef_
    importance_df = pd.DataFrame(
        {"feature": x_train.columns, "importance": np.abs(coefficients)}
    )
    return importance_df[importance_df["importance"] > 0].sort_values(
        by="importance", ascending=False
    )


# 1.2 Ridge regression
def features_ridge(
    x_train: pd.DataFrame, y_train: pd.Series, ridge_params: dict
) -> np.ndarray:
    """
    Ridge Regression: A linear regression technique that applies L2 regularization, reducing coefficient
    magnitudes to avoid overfitting, especially with multicollinearity among features.
    """
    from sklearn.linear_model import RidgeCV

    ridge = RidgeCV(**ridge_params)
    ridge.fit(x_train, y_train)

    # Get the coefficients
    coefficients = ridge.coef_

    # Create a DataFrame to hold feature importance
    importance_df = pd.DataFrame(
        {"feature": x_train.columns, "importance": np.abs(coefficients)}
    )
    return importance_df[importance_df["importance"] > 0].sort_values(
        by="importance", ascending=False
    )


# 1.3 Elastic Net(Enet)
def features_enet(
    x_train: pd.DataFrame, y_train: pd.Series, enet_params: dict
) -> np.ndarray:
    """
    Elastic Net (Enet): Combines L1 and L2 penalties (lasso and ridge) in a linear model, beneficial
    when features are highly correlated or for datasets with more features than samples.
    """
    from sklearn.linear_model import ElasticNetCV

    enet = ElasticNetCV(**enet_params)
    enet.fit(x_train, y_train)
    # Get the coefficients
    coefficients = enet.coef_
    # Create a DataFrame to hold feature importance
    importance_df = pd.DataFrame(
        {"feature": x_train.columns, "importance": np.abs(coefficients)}
    )
    return importance_df[importance_df["importance"] > 0].sort_values(
        by="importance", ascending=False
    )


# 1.4 Partial Least Squares Regression for Generalized Linear Models (plsRglm): Combines regression and
# feature reduction, useful for high-dimensional data with correlated features, such as genomics.

#! 2.Generalized Linear Models and Extensions
# 2.1


#!3.Tree-Based and Ensemble Methods
# 3.1 Random Forest(RF)
def features_rf(
    x_train: pd.DataFrame, y_train: pd.Series, rf_params: dict
) -> np.ndarray:
    """
    An ensemble of decision trees that combines predictions from multiple trees for classification or
    regression, effective with high-dimensional, complex datasets.
    when to use:
        Handles high-dimensional data well.
        Robust to overfitting due to averaging of multiple trees.
        Provides feature importance, which can help in understanding the influence of different genes.
    Fit Random Forest and return sorted feature importances.
    Recommended Use: Great for classification problems, especially when you have many features (genes).
    """
    rf = RandomForestClassifier(**rf_params)
    rf.fit(x_train, y_train)
    return pd.DataFrame(
        {"feature": x_train.columns, "importance": rf.featuress_}
    ).sort_values(by="importance", ascending=False)


# 3.2 Gradient Boosting Trees
def features_gradient_boosting(
    x_train: pd.DataFrame, y_train: pd.Series, gb_params: dict
) -> pd.DataFrame:
    """
    An ensemble of decision trees that combines predictions from multiple trees for classification or regression, effective with
    high-dimensional, complex datasets.
    Gradient Boosting
    Strengths:
        High predictive accuracy and works well for both classification and regression.
        Can handle a mixture of numerical and categorical features.
    Recommended Use:
        Effective for complex relationships and when you need a powerful predictive model.
    Fit Gradient Boosting classifier and return sorted feature importances.
    Recommended Use: Effective for complex datasets with many features (genes).
    """
    gb = GradientBoostingClassifier(**gb_params)
    gb.fit(x_train, y_train)
    return pd.DataFrame(
        {"feature": x_train.columns, "importance": gb.feature_importances_}
    ).sort_values(by="importance", ascending=False)


# 3.3 XGBoost
def features_xgb(
    x_train: pd.DataFrame, y_train: pd.Series, xgb_params: dict
) -> pd.DataFrame:
    """
    XGBoost: An advanced gradient boosting technique, faster and more efficient than GBM, with excellent predictive performance on structured data.
    """
    import xgboost as xgb

    xgb_model = xgb.XGBClassifier(**xgb_params)
    xgb_model.fit(x_train, y_train)
    return pd.DataFrame(
        {"feature": x_train.columns, "importance": xgb_model.feature_importances_}
    ).sort_values(by="importance", ascending=False)


# 3.4.decision tree
def features_decision_tree(
    x_train: pd.DataFrame, y_train: pd.Series, dt_params: dict
) -> pd.DataFrame:
    """
    A single decision tree classifier effective for identifying key decision boundaries in data.
    when to use:
        Good for capturing non-linear patterns.
        Provides feature importance scores for each feature, though it may overfit on small datasets.
        Efficient for low to medium-sized datasets, where interpretability of decisions is key.
    Recommended Use: Useful for interpretable feature importance analysis in smaller or balanced datasets.

    Fits DecisionTreeClassifier and returns sorted feature importances.
    """
    dt = DecisionTreeClassifier(**dt_params)
    dt.fit(x_train, y_train)
    return pd.DataFrame(
        {"feature": x_train.columns, "importance": dt.feature_importances_}
    ).sort_values(by="importance", ascending=False)


# 3.5 bagging
def features_bagging(
    x_train: pd.DataFrame, y_train: pd.Series, bagging_params: dict
) -> pd.DataFrame:
    """
    A bagging ensemble of models, often used with weak learners like decision trees, to reduce variance.
    when to use:
        Helps reduce overfitting, especially on high-variance models.
        Effective when the dataset has numerous features and may benefit from ensemble stability.
    Recommended Use: Beneficial for high-dimensional or noisy datasets needing ensemble stability.

    Fits BaggingClassifier and returns averaged feature importances from underlying estimators if available.
    """
    bagging = BaggingClassifier(**bagging_params)
    bagging.fit(x_train, y_train)

    # Calculate feature importance by averaging importances across estimators, if feature_importances_ is available.
    if hasattr(bagging.estimators_[0], "feature_importances_"):
        importances = np.mean(
            [estimator.feature_importances_ for estimator in bagging.estimators_],
            axis=0,
        )
        return pd.DataFrame(
            {"feature": x_train.columns, "importance": importances}
        ).sort_values(by="importance", ascending=False)
    else:
        # If the base estimator does not support feature importances, fallback to permutation importance.
        importances = permutation_importance(
            bagging, x_train, y_train, n_repeats=30, random_state=1, scoring="accuracy"
        )
        return pd.DataFrame(
            {"feature": x_train.columns, "importance": importances.importances_mean}
        ).sort_values(by="importance", ascending=False)


#! 4.Support Vector Machines
def features_svm(
    x_train: pd.DataFrame, y_train: pd.Series, rfe_params: dict
) -> np.ndarray:
    """
    Suitable for classification tasks where the number of features is much larger than the number of samples.
        1. Effective in high-dimensional spaces and with clear margin of separation.
        2. Works well for both linear and non-linear classification (using kernel functions).
    Select features using RFE with SVM.When combined with SVM, RFE selects features that are most critical for the decision boundary,
        helping reduce the dataset to a more manageable size without losing much predictive power.
    SVM (Support Vector Machines),supports various kernels (linear, rbf, poly, and sigmoid), is good at handling high-dimensional
        data and finding an optimal decision boundary between classes, especially when using the right kernel.
    kernel: ["linear", "rbf", "poly", "sigmoid"]
        'linear': simplest kernel that attempts to separate data by drawing a straight line (or hyperplane) between classes. It is effective
            when the data is linearly separable, meaning the classes can be well divided by a straight boundary.
                Advantages:
                    - Computationally efficient for large datasets.
                    - Works well when the number of features is high, which is common in genomic data where you may have thousands of genes
                        as features.
        'rbf':  a nonlinear kernel that maps the input data into a higher-dimensional space to find a decision boundary. It works well for
            data that is not linearly separable in its original space.
                Advantages:
                    - Handles nonlinear relationships between features and classes
                    - Often better than a linear kernel when there is no clear linear decision boundary in the data.
        'poly': Polynomial Kernel: computes similarity between data points based on polynomial functions of the input features. It can model
            interactions between features to a certain degree, depending on the polynomial degree chosen.
                Advantages:
                    - Allows modeling of feature interactions.
                    - Can fit more complex relationships compared to linear models.
        'sigmoid':  similar to the activation function in neural networks, and it works well when the data follows an S-shaped decision boundary.
                Advantages:
                - Can approximate the behavior of neural networks.
                - Use case: It’s not as widely used as the RBF or linear kernel but can be explored when there is some evidence of non-linear
                    S-shaped relationships.
    """
    # SVM (Support Vector Machines)
    svc = SVC(kernel=rfe_params["kernel"])  # ["linear", "rbf", "poly", "sigmoid"]
    # RFE(Recursive Feature Elimination)
    selector = RFE(svc, n_features_to_select=rfe_params["n_features_to_select"])
    selector.fit(x_train, y_train)
    return x_train.columns[selector.support_]


#! 5.Bayesian and Probabilistic Methods
def features_naive_bayes(x_train: pd.DataFrame, y_train: pd.Series) -> list:
    """
    Naive Bayes: A probabilistic classifier based on Bayes' theorem, assuming independence between features, simple and fast, especially
    effective for text classification and other high-dimensional data.
    """
    from sklearn.naive_bayes import GaussianNB

    nb = GaussianNB()
    nb.fit(x_train, y_train)
    probabilities = nb.predict_proba(x_train)
    # Limit the number of features safely, choosing the lesser of half the features or all columns
    n_features = min(x_train.shape[1] // 2, len(x_train.columns))

    # Sort probabilities, then map to valid column indices
    sorted_indices = np.argsort(probabilities.max(axis=1))[:n_features]

    # Ensure indices are within the column bounds of x_train
    valid_indices = sorted_indices[sorted_indices < len(x_train.columns)]

    return x_train.columns[valid_indices]


#! 6.Linear Discriminant Analysis (LDA)
def features_lda(x_train: pd.DataFrame, y_train: pd.Series) -> list:
    """
    Linear Discriminant Analysis (LDA): Projects data onto a lower-dimensional space to maximize class separability, often used as a dimensionality
    reduction technique before classification on high-dimensional data.
    """
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

    lda = LinearDiscriminantAnalysis()
    lda.fit(x_train, y_train)
    coef = lda.coef_.flatten()
    # Create a DataFrame to hold feature importance
    importance_df = pd.DataFrame(
        {"feature": x_train.columns, "importance": np.abs(coef)}
    )

    return importance_df[importance_df["importance"] > 0].sort_values(
        by="importance", ascending=False
    )


def features_adaboost(
    x_train: pd.DataFrame, y_train: pd.Series, adaboost_params: dict
) -> pd.DataFrame:
    """
    AdaBoost
    Strengths:
        Combines multiple weak learners to create a strong classifier.
        Focuses on examples that are hard to classify, improving overall performance.
    Recommended Use:
        Can be effective for boosting weak models in a genomics context.
    Fit AdaBoost classifier and return sorted feature importances.
    Recommended Use: Great for classification problems with a large number of features (genes).
    """
    ada = AdaBoostClassifier(**adaboost_params)
    ada.fit(x_train, y_train)
    return pd.DataFrame(
        {"feature": x_train.columns, "importance": ada.feature_importances_}
    ).sort_values(by="importance", ascending=False)


import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from skorch import NeuralNetClassifier  # sklearn compatible


class DNNClassifier(nn.Module):
    def __init__(self, input_dim, hidden_dim=128, output_dim=2, dropout_rate=0.5):
        super(DNNClassifier, self).__init__()

        self.hidden_layer1 = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
        )

        self.hidden_layer2 = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim), nn.ReLU(), nn.Dropout(dropout_rate)
        )

        # Adding a residual connection between hidden layers
        self.residual = nn.Linear(input_dim, hidden_dim)

        self.output_layer = nn.Sequential(
            nn.Linear(hidden_dim, output_dim), nn.Softmax(dim=1)
        )

    def forward(self, x):
        residual = self.residual(x)
        x = self.hidden_layer1(x)
        x = x + residual  # Residual connection
        x = self.hidden_layer2(x)
        x = self.output_layer(x)
        return x


def validate_classifier(
    clf,
    x_train: pd.DataFrame,
    y_train: pd.Series,
    x_test: pd.DataFrame,
    y_test: pd.Series,
    metrics: list = ["accuracy", "precision", "recall", "f1", "roc_auc"],
    cv_folds: int = 5,
) -> dict:
    """
    Perform cross-validation for a given classifier and return average scores for specified metrics on training data.
    Then fit the best model on the full training data and evaluate it on the test set.

    Parameters:
    - clf: The classifier to be validated.
    - x_train: Training features.
    - y_train: Training labels.
    - x_test: Test features.
    - y_test: Test labels.
    - metrics: List of metrics to evaluate (e.g., ['accuracy', 'roc_auc']).
    - cv_folds: Number of cross-validation folds.

    Returns:
    - results: Dictionary containing average cv_train_scores and cv_test_scores.
    """
    cv_train_scores = {metric: [] for metric in metrics}
    skf = StratifiedKFold(n_splits=cv_folds)
    # Perform cross-validation
    for metric in metrics:
        try:
            if metric == "roc_auc" and len(set(y_train)) == 2:
                scores = cross_val_score(
                    clf, x_train, y_train, cv=skf, scoring="roc_auc"
                )
                cv_train_scores[metric] = (
                    np.nanmean(scores) if not np.isnan(scores).all() else float("nan")
                )
            else:
                score = cross_val_score(clf, x_train, y_train, cv=skf, scoring=metric)
                cv_train_scores[metric] = score.mean()
        except Exception as e:
            cv_train_scores[metric] = float("nan")
    clf.fit(x_train, y_train)

    # Evaluate on the test set
    cv_test_scores = {}
    for metric in metrics:
        if metric == "roc_auc" and len(set(y_test)) == 2:
            try:
                y_prob = clf.predict_proba(x_test)[:, 1]
                cv_test_scores[metric] = roc_auc_score(y_test, y_prob)
            except AttributeError:
                cv_test_scores[metric] = float("nan")
        else:
            score_func = globals().get(
                f"{metric}_score"
            )  # Fetching the appropriate scoring function
            if score_func:
                try:
                    y_pred = clf.predict(x_test)
                    cv_test_scores[metric] = score_func(y_test, y_pred)
                except Exception as e:
                    cv_test_scores[metric] = float("nan")

    # Combine results
    results = {"cv_train_scores": cv_train_scores, "cv_test_scores": cv_test_scores}
    return results


def get_models(
    random_state=1,
    cls=[
        "lasso",
        "ridge",
        "Elastic Net(Enet)",
        "gradient Boosting",
        "Random forest (rf)",
        "XGBoost (xgb)",
        "Support Vector Machine(svm)",
        "naive bayes",
        "Linear Discriminant Analysis (lda)",
        "adaboost",
        "DecisionTree",
        "KNeighbors",
        "Bagging",
    ],
):
    from sklearn.ensemble import (
        RandomForestClassifier,
        GradientBoostingClassifier,
        AdaBoostClassifier,
        BaggingClassifier,
    )
    from sklearn.svm import SVC
    from sklearn.linear_model import (
        LogisticRegression,
        Lasso,
        RidgeClassifierCV,
        ElasticNet,
    )
    from sklearn.naive_bayes import GaussianNB
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
    import xgboost as xgb
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.neighbors import KNeighborsClassifier

    res_cls = {}
    model_all = {
        "Lasso": LogisticRegression(
            penalty="l1", solver="saga", random_state=random_state
        ),
        "Ridge": RidgeClassifierCV(),
        "Elastic Net (Enet)": ElasticNet(random_state=random_state),
        "Gradient Boosting": GradientBoostingClassifier(random_state=random_state),
        "Random Forest (RF)": RandomForestClassifier(random_state=random_state),
        "XGBoost (XGB)": xgb.XGBClassifier(random_state=random_state),
        "Support Vector Machine (SVM)": SVC(kernel="rbf", probability=True),
        "Naive Bayes": GaussianNB(),
        "Linear Discriminant Analysis (LDA)": LinearDiscriminantAnalysis(),
        "AdaBoost": AdaBoostClassifier(random_state=random_state, algorithm="SAMME"),
        "DecisionTree": DecisionTreeClassifier(),
        "KNeighbors": KNeighborsClassifier(n_neighbors=5),
        "Bagging": BaggingClassifier(),
    }
    print("Using default models:")
    for cls_name in cls:
        cls_name = ips.strcmp(cls_name, list(model_all.keys()))[0]
        res_cls[cls_name] = model_all[cls_name]
        print(f"- {cls_name}")
    return res_cls


def get_features(
    X: Union[pd.DataFrame, np.ndarray],  # n_samples X n_features
    y: Union[pd.Series, np.ndarray, list],  # n_samples X n_features
    test_size: float = 0.2,
    random_state: int = 1,
    n_features: int = 10,
    fill_missing=True,
    rf_params: Optional[Dict] = None,
    rfe_params: Optional[Dict] = None,
    lasso_params: Optional[Dict] = None,
    ridge_params: Optional[Dict] = None,
    enet_params: Optional[Dict] = None,
    gb_params: Optional[Dict] = None,
    adaboost_params: Optional[Dict] = None,
    xgb_params: Optional[Dict] = None,
    dt_params: Optional[Dict] = None,
    bagging_params: Optional[Dict] = None,
    knn_params: Optional[Dict] = None,
    cls: list = [
        "lasso",
        "ridge",
        "Elastic Net(Enet)",
        "gradient Boosting",
        "Random forest (rf)",
        "XGBoost (xgb)",
        "Support Vector Machine(svm)",
        "naive bayes",
        "Linear Discriminant Analysis (lda)",
        "adaboost",
        "DecisionTree",
        "KNeighbors",
        "Bagging",
    ],
    metrics: Optional[List[str]] = None,
    cv_folds: int = 5,
    strict: bool = False,
    n_shared: int = 2,  # 只要有两个方法有重合,就纳入common genes
    use_selected_features: bool = True,
    plot_: bool = True,
    dir_save: str = "./",
) -> dict:
    """
    Master function to perform feature selection and validate models.
    """
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import StandardScaler, OneHotEncoder

    # Ensure X and y are DataFrames/Series for consistency
    if isinstance(X, np.ndarray):
        X = pd.DataFrame(X)
    if isinstance(y, (np.ndarray, list)):
        y = pd.Series(y)

    # fill na
    if fill_missing:
        ips.df_fillna(data=X, method="knn", inplace=True, axis=0)
    if isinstance(y, str) and y in X.columns:
        y_col_name = y
        y = X[y]
        y = ips.df_encoder(pd.DataFrame(y), method="dummy")
        X = X.drop(y_col_name, axis=1)
    else:
        y = ips.df_encoder(pd.DataFrame(y), method="dummy").values.ravel()
    y = y.loc[X.index]  # Align y with X after dropping rows with missing values in X
    y = y.ravel() if isinstance(y, np.ndarray) else y.values.ravel()

    if X.shape[0] != len(y):
        raise ValueError("X and y must have the same number of samples (rows).")

    # #! # Check for non-numeric columns in X and apply one-hot encoding if needed
    # Check if any column in X is non-numeric
    if any(not np.issubdtype(dtype, np.number) for dtype in X.dtypes):
        X = pd.get_dummies(X, drop_first=True)
    print(X.shape)

    # #!alternative:  # Identify categorical and numerical columns
    # categorical_cols = X.select_dtypes(include=["object", "category"]).columns
    # numerical_cols = X.select_dtypes(include=["number"]).columns

    # # Define preprocessing pipeline
    # preprocessor = ColumnTransformer(
    #     transformers=[
    #         ("num", StandardScaler(), numerical_cols),
    #         ("cat", OneHotEncoder(drop="first", handle_unknown="ignore"), categorical_cols),
    #     ]
    # )
    # # Preprocess the data
    # X = preprocessor.fit_transform(X)

    # Split data into training and test sets
    x_train, x_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    # Standardize features
    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)

    # Convert back to DataFrame for consistency
    x_train = pd.DataFrame(x_train_scaled, columns=x_train.columns)
    x_test = pd.DataFrame(x_test_scaled, columns=x_test.columns)

    rf_defaults = {"n_estimators": 100, "random_state": random_state}
    rfe_defaults = {"kernel": "linear", "n_features_to_select": n_features}
    lasso_defaults = {"alphas": np.logspace(-4, 4, 100), "cv": 10}
    ridge_defaults = {"alphas": np.logspace(-4, 4, 100), "cv": 10}
    enet_defaults = {"alphas": np.logspace(-4, 4, 100), "cv": 10}
    xgb_defaults = {
        "n_estimators": 100,
        "use_label_encoder": False,
        "eval_metric": "logloss",
        "random_state": random_state,
    }
    gb_defaults = {"n_estimators": 100, "random_state": random_state}
    adaboost_defaults = {"n_estimators": 50, "random_state": random_state}
    dt_defaults = {"max_depth": None, "random_state": random_state}
    bagging_defaults = {"n_estimators": 50, "random_state": random_state}
    knn_defaults = {"n_neighbors": 5}
    rf_params, rfe_params = rf_params or rf_defaults, rfe_params or rfe_defaults
    lasso_params, ridge_params = (
        lasso_params or lasso_defaults,
        ridge_params or ridge_defaults,
    )
    enet_params, xgb_params = enet_params or enet_defaults, xgb_params or xgb_defaults
    gb_params, adaboost_params = (
        gb_params or gb_defaults,
        adaboost_params or adaboost_defaults,
    )
    dt_params = dt_params or dt_defaults
    bagging_params = bagging_params or bagging_defaults
    knn_params = knn_params or knn_defaults

    cls_ = [
        "lasso",
        "ridge",
        "Elastic Net(Enet)",
        "Gradient Boosting",
        "Random Forest (rf)",
        "XGBoost (xgb)",
        "Support Vector Machine(svm)",
        "Naive Bayes",
        "Linear Discriminant Analysis (lda)",
        "adaboost",
    ]
    cls = [ips.strcmp(i, cls_)[0] for i in cls]

    # Lasso Feature Selection
    lasso_importances = (
        features_lasso(x_train, y_train, lasso_params)
        if "lasso" in cls
        else pd.DataFrame()
    )
    lasso_selected_features = (
        lasso_importances.head(n_features)["feature"].values if "lasso" in cls else []
    )
    # Ridge
    ridge_importances = (
        features_ridge(x_train, y_train, ridge_params)
        if "ridge" in cls
        else pd.DataFrame()
    )
    selected_ridge_features = (
        ridge_importances.head(n_features)["feature"].values if "ridge" in cls else []
    )
    # Elastic Net
    enet_importances = (
        features_enet(x_train, y_train, enet_params)
        if "Enet" in cls
        else pd.DataFrame()
    )
    selected_enet_features = (
        enet_importances.head(n_features)["feature"].values if "Enet" in cls else []
    )
    # Random Forest Feature Importance
    rf_importances = (
        features_rf(x_train, y_train, rf_params)
        if "Random Forest" in cls
        else pd.DataFrame()
    )
    top_rf_features = (
        rf_importances.head(n_features)["feature"].values
        if "Random Forest" in cls
        else []
    )
    # Gradient Boosting Feature Importance
    gb_importances = (
        features_gradient_boosting(x_train, y_train, gb_params)
        if "Gradient Boosting" in cls
        else pd.DataFrame()
    )
    top_gb_features = (
        gb_importances.head(n_features)["feature"].values
        if "Gradient Boosting" in cls
        else []
    )
    # xgb
    xgb_importances = (
        features_xgb(x_train, y_train, xgb_params) if "xgb" in cls else pd.DataFrame()
    )
    top_xgb_features = (
        xgb_importances.head(n_features)["feature"].values if "xgb" in cls else []
    )

    # SVM with RFE
    selected_svm_features = (
        features_svm(x_train, y_train, rfe_params) if "svm" in cls else []
    )
    # Naive Bayes
    selected_naive_bayes_features = (
        features_naive_bayes(x_train, y_train) if "Naive Bayes" in cls else []
    )
    # lda: linear discriminant analysis
    lda_importances = features_lda(x_train, y_train) if "lda" in cls else pd.DataFrame()
    selected_lda_features = (
        lda_importances.head(n_features)["feature"].values if "lda" in cls else []
    )
    # AdaBoost Feature Importance
    adaboost_importances = (
        features_adaboost(x_train, y_train, adaboost_params)
        if "AdaBoost" in cls
        else pd.DataFrame()
    )
    top_adaboost_features = (
        adaboost_importances.head(n_features)["feature"].values
        if "AdaBoost" in cls
        else []
    )
    # Decision Tree Feature Importance
    dt_importances = (
        features_decision_tree(x_train, y_train, dt_params)
        if "Decision Tree" in cls
        else pd.DataFrame()
    )
    top_dt_features = (
        dt_importances.head(n_features)["feature"].values
        if "Decision Tree" in cls
        else []
    )
    # Bagging Feature Importance
    bagging_importances = (
        features_bagging(x_train, y_train, bagging_params)
        if "Bagging" in cls
        else pd.DataFrame()
    )
    top_bagging_features = (
        bagging_importances.head(n_features)["feature"].values
        if "Bagging" in cls
        else []
    )
    # KNN Feature Importance via Permutation
    knn_importances = (
        features_knn(x_train, y_train, knn_params) if "KNN" in cls else pd.DataFrame()
    )
    top_knn_features = (
        knn_importances.head(n_features)["feature"].values if "KNN" in cls else []
    )

    #! Find common features
    common_features = ips.shared(
        lasso_selected_features,
        selected_ridge_features,
        selected_enet_features,
        top_rf_features,
        top_gb_features,
        top_xgb_features,
        selected_svm_features,
        selected_naive_bayes_features,
        selected_lda_features,
        top_adaboost_features,
        top_dt_features,
        top_bagging_features,
        top_knn_features,
        strict=strict,
        n_shared=n_shared,
        verbose=False,
    )

    # Use selected features or all features for model validation
    x_train_selected = (
        x_train[list(common_features)] if use_selected_features else x_train
    )
    x_test_selected = x_test[list(common_features)] if use_selected_features else x_test

    if metrics is None:
        metrics = ["accuracy", "precision", "recall", "f1", "roc_auc"]

    # Prepare results DataFrame for selected features
    features_df = pd.DataFrame(
        {
            "type": ["Lasso"] * len(lasso_selected_features)
            + ["Ridge"] * len(selected_ridge_features)
            + ["Random Forest"] * len(top_rf_features)
            + ["Gradient Boosting"] * len(top_gb_features)
            + ["Enet"] * len(selected_enet_features)
            + ["xgb"] * len(top_xgb_features)
            + ["SVM"] * len(selected_svm_features)
            + ["Naive Bayes"] * len(selected_naive_bayes_features)
            + ["Linear Discriminant Analysis"] * len(selected_lda_features)
            + ["AdaBoost"] * len(top_adaboost_features)
            + ["Decision Tree"] * len(top_dt_features)
            + ["Bagging"] * len(top_bagging_features)
            + ["KNN"] * len(top_knn_features),
            "feature": np.concatenate(
                [
                    lasso_selected_features,
                    selected_ridge_features,
                    top_rf_features,
                    top_gb_features,
                    selected_enet_features,
                    top_xgb_features,
                    selected_svm_features,
                    selected_naive_bayes_features,
                    selected_lda_features,
                    top_adaboost_features,
                    top_dt_features,
                    top_bagging_features,
                    top_knn_features,
                ]
            ),
        }
    )

    #! Validate trained each classifier
    models = get_models(random_state=random_state, cls=cls)
    cv_train_results, cv_test_results = [], []
    for name, clf in models.items():
        if not x_train_selected.empty:
            cv_scores = validate_classifier(
                clf,
                x_train_selected,
                y_train,
                x_test_selected,
                y_test,
                metrics=metrics,
                cv_folds=cv_folds,
            )

            cv_train_score_df = pd.DataFrame(cv_scores["cv_train_scores"], index=[name])
            cv_test_score_df = pd.DataFrame(cv_scores["cv_test_scores"], index=[name])
            cv_train_results.append(cv_train_score_df)
            cv_test_results.append(cv_test_score_df)
    if all([cv_train_results, cv_test_results]):
        cv_train_results_df = (
            pd.concat(cv_train_results)
            .reset_index()
            .rename(columns={"index": "Classifier"})
        )
        cv_test_results_df = (
            pd.concat(cv_test_results)
            .reset_index()
            .rename(columns={"index": "Classifier"})
        )
        #! Store results in the main results dictionary
        results = {
            "selected_features": features_df,
            "cv_train_scores": cv_train_results_df,
            "cv_test_scores": rank_models(cv_test_results_df, plot_=plot_),
            "common_features": list(common_features),
        }
        if all([plot_, dir_save]):
            from datetime import datetime

            now_ = datetime.now().strftime("%y%m%d_%H%M%S")
            ips.figsave(dir_save + f"features{now_}.pdf")
    else:
        results = {
            "selected_features": pd.DataFrame(),
            "cv_train_scores": pd.DataFrame(),
            "cv_test_scores": pd.DataFrame(),
            "common_features": [],
        }
        print(f"Warning: 没有找到共同的genes, when n_shared={n_shared}")
    return results


#! # usage:
# # Get features and common features
# results = get_features(X, y)
# common_features = results["common_features"]
def validate_features(
    x_train: pd.DataFrame,
    y_train: pd.Series,
    x_true: pd.DataFrame,
    y_true: pd.Series,
    common_features: set = None,
    models: Optional[Dict[str, Any]] = None,
    metrics: Optional[list] = None,
    random_state: int = 1,
    smote: bool = False,
    n_jobs: int = -1,
    plot_: bool = True,
    class_weight: str = "balanced",
) -> dict:
    """
    Validate models using selected features on the validation dataset.

    Parameters:
    - x_train (pd.DataFrame): Training feature dataset.
    - y_train (pd.Series): Training target variable.
    - x_true (pd.DataFrame): Validation feature dataset.
    - y_true (pd.Series): Validation target variable.
    - common_features (set): Set of common features to use for validation.
    - models (dict, optional): Dictionary of models to validate.
    - metrics (list, optional): List of metrics to compute.
    - random_state (int): Random state for reproducibility.
    - plot_ (bool): Option to plot metrics (to be implemented if needed).
    - class_weight (str or dict): Class weights to handle imbalance.

    """
    from tqdm import tqdm

    # Ensure common features are selected
    common_features = ips.shared(
        common_features, x_train.columns, x_true.columns, strict=True, verbose=False
    )

    # Filter the training and validation datasets for the common features
    x_train_selected = x_train[common_features]
    x_true_selected = x_true[common_features]

    if not x_true_selected.index.equals(y_true.index):
        raise ValueError(
            "Index mismatch between validation features and target. Ensure data alignment."
        )

    y_true = y_true.loc[x_true_selected.index]

    # Handle class imbalance using SMOTE
    if smote:
        if (
            y_train.value_counts(normalize=True).max() < 0.8
        ):  # Threshold to decide if data is imbalanced
            smote = SMOTE(random_state=random_state)
            x_train_resampled, y_train_resampled = smote.fit_resample(
                x_train_selected, y_train
            )
        else:
            # skip SMOTE
            x_train_resampled, y_train_resampled = x_train_selected, y_train
    else:
        x_train_resampled, y_train_resampled = x_train_selected, y_train

    # Default models if not provided
    if models is None:
        models = {
            "Random Forest": RandomForestClassifier(
                class_weight=class_weight, random_state=random_state
            ),
            "SVM": SVC(probability=True, class_weight=class_weight),
            "Logistic Regression": LogisticRegression(
                class_weight=class_weight, random_state=random_state
            ),
            "Gradient Boosting": GradientBoostingClassifier(random_state=random_state),
            "AdaBoost": AdaBoostClassifier(
                random_state=random_state, algorithm="SAMME"
            ),
            "Lasso": LogisticRegression(
                penalty="l1", solver="saga", random_state=random_state
            ),
            "Ridge": LogisticRegression(
                penalty="l2", solver="saga", random_state=random_state
            ),
            "Elastic Net": LogisticRegression(
                penalty="elasticnet",
                solver="saga",
                l1_ratio=0.5,
                random_state=random_state,
            ),
            "XGBoost": xgb.XGBClassifier(eval_metric="logloss"),
            "Naive Bayes": GaussianNB(),
            "LDA": LinearDiscriminantAnalysis(),
        }

    # Hyperparameter grids for tuning
    param_grids = {
        "Random Forest": {
            "n_estimators": [100, 200, 300, 400, 500],
            "max_depth": [None, 3, 5, 10, 20],
            "min_samples_split": [2, 5, 10],
            "min_samples_leaf": [1, 2, 4],
            "class_weight": [None, "balanced"],
        },
        "SVM": {
            "C": [0.01, 0.1, 1, 10, 100, 1000],
            "gamma": [0.001, 0.01, 0.1, "scale", "auto"],
            "kernel": ["linear", "rbf", "poly"],
        },
        "Logistic Regression": {
            "C": [0.01, 0.1, 1, 10, 100],
            "solver": ["liblinear", "saga", "newton-cg", "lbfgs"],
            "penalty": ["l1", "l2"],
            "max_iter": [100, 200, 300],
        },
        "Gradient Boosting": {
            "n_estimators": [100, 200, 300, 400, 500],
            "learning_rate": np.logspace(-3, 0, 4),
            "max_depth": [3, 5, 7, 9],
            "min_samples_split": [2, 5, 10],
        },
        "AdaBoost": {
            "n_estimators": [50, 100, 200, 300, 500],
            "learning_rate": np.logspace(-3, 0, 4),
        },
        "Lasso": {"C": np.logspace(-3, 1, 10), "max_iter": [100, 200, 300]},
        "Ridge": {"C": np.logspace(-3, 1, 10), "max_iter": [100, 200, 300]},
        "Elastic Net": {
            "C": np.logspace(-3, 1, 10),
            "l1_ratio": [0.1, 0.5, 0.9],
            "max_iter": [100, 200, 300],
        },
        "XGBoost": {
            "n_estimators": [100, 200],
            "max_depth": [3, 5, 7],
            "learning_rate": [0.01, 0.1, 0.2],
            "subsample": [0.8, 1.0],
            "colsample_bytree": [0.8, 1.0],
        },
        "Naive Bayes": {},
        "LDA": {"solver": ["svd", "lsqr", "eigen"]},
    }
    # Default metrics if not provided
    if metrics is None:
        metrics = [
            "accuracy",
            "precision",
            "recall",
            "f1",
            "roc_auc",
            "mcc",
            "specificity",
            "balanced_accuracy",
            "pr_auc",
        ]

    results = {}

    # Validate each classifier with GridSearchCV
    for name, clf in tqdm(
        models.items(),
        desc="for metric in metrics",
        colour="green",
        bar_format="{l_bar}{bar} {n_fmt}/{total_fmt}",
    ):
        print(f"\nValidating {name} on the validation dataset:")

        # Check if `predict_proba` method exists; if not, use CalibratedClassifierCV
        # 没有predict_proba的分类器，使用 CalibratedClassifierCV 可以获得校准的概率估计。此外，为了使代码更灵活，我们可以在创建分类器
        # 时检查 predict_proba 方法是否存在，如果不存在且用户希望计算 roc_auc 或 pr_auc，则启用 CalibratedClassifierCV
        if not hasattr(clf, "predict_proba"):
            print(
                f"Using CalibratedClassifierCV for {name} due to lack of probability estimates."
            )
            calibrated_clf = CalibratedClassifierCV(clf, method="sigmoid", cv="prefit")
        else:
            calibrated_clf = clf
        # Stratified K-Fold for cross-validation
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)

        # Create GridSearchCV object
        gs = GridSearchCV(
            estimator=calibrated_clf,
            param_grid=param_grids[name],
            scoring="roc_auc",  # Optimize for ROC AUC
            cv=skf,  # Stratified K-Folds cross-validation
            n_jobs=n_jobs,
            verbose=1,
        )

        # Fit the model using GridSearchCV
        gs.fit(x_train_resampled, y_train_resampled)
        # Best estimator from grid search
        best_clf = gs.best_estimator_
        # Make predictions on the validation set
        y_pred = best_clf.predict(x_true_selected)
        # Calculate probabilities for ROC AUC if possible
        if hasattr(best_clf, "predict_proba"):
            y_pred_proba = best_clf.predict_proba(x_true_selected)[:, 1]
        elif hasattr(best_clf, "decision_function"):
            # If predict_proba is not available, use decision_function (e.g., for SVM)
            y_pred_proba = best_clf.decision_function(x_true_selected)
            # Ensure y_pred_proba is within 0 and 1 bounds
            y_pred_proba = (y_pred_proba - y_pred_proba.min()) / (
                y_pred_proba.max() - y_pred_proba.min()
            )
        else:
            y_pred_proba = None  # No probability output for certain models

        # Calculate metrics
        validation_scores = {}
        for metric in metrics:
            if metric == "accuracy":
                validation_scores[metric] = accuracy_score(y_true, y_pred)
            elif metric == "precision":
                validation_scores[metric] = precision_score(
                    y_true, y_pred, average="weighted"
                )
            elif metric == "recall":
                validation_scores[metric] = recall_score(
                    y_true, y_pred, average="weighted"
                )
            elif metric == "f1":
                validation_scores[metric] = f1_score(y_true, y_pred, average="weighted")
            elif metric == "roc_auc" and y_pred_proba is not None:
                validation_scores[metric] = roc_auc_score(y_true, y_pred_proba)
            elif metric == "mcc":
                validation_scores[metric] = matthews_corrcoef(y_true, y_pred)
            elif metric == "specificity":
                tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
                validation_scores[metric] = tn / (tn + fp)  # Specificity calculation
            elif metric == "balanced_accuracy":
                validation_scores[metric] = balanced_accuracy_score(y_true, y_pred)
            elif metric == "pr_auc" and y_pred_proba is not None:
                precision, recall, _ = precision_recall_curve(y_true, y_pred_proba)
                validation_scores[metric] = average_precision_score(
                    y_true, y_pred_proba
                )

        # Calculate ROC curve
        # https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html
        if y_pred_proba is not None:
            # fpr, tpr, roc_auc = dict(), dict(), dict()
            fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
            lower_ci, upper_ci = cal_auc_ci(y_true, y_pred_proba, verbose=False)
            roc_auc = auc(fpr, tpr)
            roc_info = {
                "fpr": fpr.tolist(),
                "tpr": tpr.tolist(),
                "auc": roc_auc,
                "ci95": (lower_ci, upper_ci),
            }
            # precision-recall curve
            precision_, recall_, _ = precision_recall_curve(y_true, y_pred_proba)
            avg_precision_ = average_precision_score(y_true, y_pred_proba)
            pr_info = {
                "precision": precision_,
                "recall": recall_,
                "avg_precision": avg_precision_,
            }
        else:
            roc_info, pr_info = None, None
        results[name] = {
            "best_params": gs.best_params_,
            "scores": validation_scores,
            "roc_curve": roc_info,
            "pr_curve": pr_info,
            "confusion_matrix": confusion_matrix(y_true, y_pred),
        }

    df_results = pd.DataFrame.from_dict(results, orient="index")

    return df_results


#! usage validate_features()
# Validate models using the validation dataset (X_val, y_val)
# validation_results = validate_features(X, y, X_val, y_val, common_features)


# # If you want to access validation scores
# print(validation_results)
def plot_validate_features(res_val):
    """
    plot the results of 'validate_features()'
    """
    colors = plot.get_color(len(ips.flatten(res_val["pr_curve"].index)))
    if res_val.shape[0] > 5:
        alpha = 0
        figsize = [8, 10]
        subplot_layout = [1, 2]
        ncols = 2
        bbox_to_anchor = [1.5, 0.6]
    else:
        alpha = 0.03
        figsize = [10, 6]
        subplot_layout = [1, 1]
        ncols = 1
        bbox_to_anchor = [1, 1]
    nexttile = plot.subplot(figsize=figsize)
    ax = nexttile(subplot_layout[0], subplot_layout[1])
    for i, model_name in enumerate(ips.flatten(res_val["pr_curve"].index)):
        fpr = res_val["roc_curve"][model_name]["fpr"]
        tpr = res_val["roc_curve"][model_name]["tpr"]
        (lower_ci, upper_ci) = res_val["roc_curve"][model_name]["ci95"]
        mean_auc = res_val["roc_curve"][model_name]["auc"]
        plot_roc_curve(
            fpr,
            tpr,
            mean_auc,
            lower_ci,
            upper_ci,
            model_name=model_name,
            lw=1.5,
            color=colors[i],
            alpha=alpha,
            ax=ax,
        )
    plot.figsets(
        sp=2,
        legend=dict(
            loc="upper right",
            ncols=ncols,
            fontsize=8,
            bbox_to_anchor=[1.5, 0.6],
            markerscale=0.8,
        ),
    )
    # plot.split_legend(ax,n=2, loc=["upper left", "lower left"],bbox=[[1,0.5],[1,0.5]],ncols=2,labelcolor="k",fontsize=8)

    ax = nexttile(subplot_layout[0], subplot_layout[1])
    for i, model_name in enumerate(ips.flatten(res_val["pr_curve"].index)):
        plot_pr_curve(
            recall=res_val["pr_curve"][model_name]["recall"],
            precision=res_val["pr_curve"][model_name]["precision"],
            avg_precision=res_val["pr_curve"][model_name]["avg_precision"],
            model_name=model_name,
            color=colors[i],
            lw=1.5,
            alpha=alpha,
            ax=ax,
        )
    plot.figsets(
        sp=2,
        legend=dict(loc="upper right", ncols=1, fontsize=8, bbox_to_anchor=[1.5, 0.5]),
    )
    # plot.split_legend(ax,n=2, loc=["upper left", "lower left"],bbox=[[1,0.5],[1,0.5]],ncols=2,labelcolor="k",fontsize=8)


def plot_validate_features_single(res_val, figsize=None):
    if figsize is None:
        nexttile = plot.subplot(len(ips.flatten(res_val["pr_curve"].index)), 3)
    else:
        nexttile = plot.subplot(
            len(ips.flatten(res_val["pr_curve"].index)), 3, figsize=figsize
        )
    for model_name in ips.flatten(res_val["pr_curve"].index):
        fpr = res_val["roc_curve"][model_name]["fpr"]
        tpr = res_val["roc_curve"][model_name]["tpr"]
        (lower_ci, upper_ci) = res_val["roc_curve"][model_name]["ci95"]
        mean_auc = res_val["roc_curve"][model_name]["auc"]

        # Plotting
        plot_roc_curve(fpr, tpr, mean_auc, lower_ci, upper_ci,
            model_name=model_name, ax=nexttile())
        plot.figsets(title=model_name, sp=2)

        plot_pr_binary(
            recall=res_val["pr_curve"][model_name]["recall"],
            precision=res_val["pr_curve"][model_name]["precision"],
            avg_precision=res_val["pr_curve"][model_name]["avg_precision"],
            model_name=model_name,
            ax=nexttile(),
        )
        plot.figsets(title=model_name, sp=2)

        # plot cm
        plot_cm(res_val["confusion_matrix"][model_name], ax=nexttile(), normalize=False)
        plot.figsets(title=model_name, sp=2)


def cal_auc_ci(
    y_true, y_pred, n_bootstraps=1000, ci=0.95, random_state=1, verbose=True
):
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    bootstrapped_scores = []
    if verbose:
        print("auroc score:", roc_auc_score(y_true, y_pred))
    rng = np.random.RandomState(random_state)
    for i in range(n_bootstraps):
        # bootstrap by sampling with replacement on the prediction indices
        indices = rng.randint(0, len(y_pred), len(y_pred))
        if len(np.unique(y_true[indices])) < 2:
            # We need at least one positive and one negative sample for ROC AUC
            # to be defined: reject the sample
            continue
        if isinstance(y_true, np.ndarray):
            score = roc_auc_score(y_true[indices], y_pred[indices])
        else:
            score = roc_auc_score(y_true.iloc[indices], y_pred.iloc[indices])
        bootstrapped_scores.append(score)
        # print("Bootstrap #{} ROC area: {:0.3f}".format(i + 1, score))
    sorted_scores = np.array(bootstrapped_scores)
    sorted_scores.sort()

    # Computing the lower and upper bound of the 90% confidence interval
    # You can change the bounds percentiles to 0.025 and 0.975 to get
    # a 95% confidence interval instead.
    confidence_lower = sorted_scores[int((1 - ci) * len(sorted_scores))]
    confidence_upper = sorted_scores[int(ci * len(sorted_scores))]
    if verbose:
        print(
            "Confidence interval for the score: [{:0.3f} - {:0.3}]".format(
                confidence_lower, confidence_upper
            )
        )
    return confidence_lower, confidence_upper


def plot_roc_curve(
    fpr=None,
    tpr=None,
    mean_auc=None,
    lower_ci=None,
    upper_ci=None,
    model_name=None,
    color="#FF8F00",
    lw=2,
    alpha=0.1,
    ci_display=True,
    title="ROC Curve",
    xlabel="1−Specificity",
    ylabel="Sensitivity",
    legend_loc="lower right",
    diagonal_color="0.5",
    figsize=(5, 5),
    ax=None,
    **kwargs,
):
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    if mean_auc is not None:
        model_name = "ROC curve" if model_name is None else model_name
        if ci_display:
            label = f"{model_name} (AUC = {mean_auc:.3f})\n95% CI: {lower_ci:.3f} - {upper_ci:.3f}"
        else:
            label = f"{model_name} (AUC = {mean_auc:.3f})"
    else:
        label = None

    # Plot ROC curve and the diagonal reference line
    ax.fill_between(fpr, tpr, alpha=alpha, color=color)
    ax.plot([0, 1], [0, 1], color=diagonal_color, clip_on=False, linestyle="--")
    ax.plot(fpr, tpr, color=color, lw=lw, label=label, clip_on=False, **kwargs)
    # Setting plot limits, labels, and title
    ax.set_xlim([-0.01, 1.0])
    ax.set_ylim([0.0, 1.0])
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(loc=legend_loc)
    return ax


# * usage: ml2ls.plot_roc_curve(fpr, tpr, mean_auc, lower_ci, upper_ci)
# for model_name in flatten(validation_results["roc_curve"].keys())[2:]:
#     fpr = validation_results["roc_curve"][model_name]["fpr"]
#     tpr = validation_results["roc_curve"][model_name]["tpr"]
#     (lower_ci, upper_ci) = validation_results["roc_curve"][model_name]["ci95"]
#     mean_auc = validation_results["roc_curve"][model_name]["auc"]

#     # Plotting
#     ml2ls.plot_roc_curve(fpr, tpr, mean_auc, lower_ci, upper_ci)
#     figsets(title=model_name)

def plot_pr_curve(
    recall=None,
    precision=None,
    avg_precision=None,
    model_name=None,
    lw=2,
    figsize=[5, 5],
    title="Precision-Recall Curve",
    xlabel="Recall",
    ylabel="Precision",
    alpha=0.1,
    color="#FF8F00",
    legend_loc="lower left",
    ax=None,
    **kwargs,
):
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    model_name = "PR curve" if model_name is None else model_name
    # Plot Precision-Recall curve
    ax.plot(
        recall,
        precision,
        lw=lw,
        color=color,
        label=(f"{model_name} (AP={avg_precision:.2f})"),
        clip_on=False,
        **kwargs,
    )
    # Fill area under the curve
    ax.fill_between(recall, precision, alpha=alpha, color=color)

    # Customize axes
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xlim([-0.01, 1.0])
    ax.set_ylim([0.0, 1.0])
    ax.grid(False)
    ax.legend(loc=legend_loc)
    return ax

# * usage: ml2ls.plot_pr_curve()
# for md_name in flatten(validation_results["pr_curve"].keys()):
#     ml2ls.plot_pr_curve(
#         recall=validation_results["pr_curve"][md_name]["recall"],
#         precision=validation_results["pr_curve"][md_name]["precision"],
#         avg_precision=validation_results["pr_curve"][md_name]["avg_precision"],
#         model_name=md_name,
#         lw=2,
#         alpha=0.1,
#         color="r",
#     )

def plot_pr_binary(
    recall=None,
    precision=None,
    avg_precision=None,
    model_name=None,
    lw=2,
    figsize=[5, 5],
    title="Precision-Recall Curve",
    xlabel="Recall",
    ylabel="Precision",
    alpha=0.1,
    color="#FF8F00",
    legend_loc="lower left",
    ax=None,
    show_avg_precision=False,
    **kwargs,
    ):
    from scipy.interpolate import interp1d
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    model_name = "Binary PR Curve" if model_name is None else model_name

    #* use sklearn bulitin function 'PrecisionRecallDisplay'?
    # from sklearn.metrics import PrecisionRecallDisplay
    # disp = PrecisionRecallDisplay(precision=precision, 
    #                               recall=recall, 
    #                               average_precision=avg_precision,**kwargs)
    # disp.plot(ax=ax, name=model_name, color=color)
    
    # Plot Precision-Recall curve
    ax.plot(
        recall,
        precision,
        lw=lw,
        color=color,
        label=(f"{model_name} (AP={avg_precision:.2f})"),
        clip_on=False,
        **kwargs,
    )

    # Fill area under the curve
    ax.fill_between(recall, precision, alpha=alpha, color=color)
    # Add F1 score iso-contours
    f_scores = np.linspace(0.2, 0.8, num=4)
    # for f_score in f_scores:
    #     x = np.linspace(0.01, 1)
    #     y = f_score * x / (2 * x - f_score)
    #     plt.plot(x[y >= 0], y[y >= 0], color="gray", alpha=1)
    #     plt.annotate(f"$f_1={f_score:0.1f}$", xy=(0.8, y[45] + 0.02))

    pr_boundary = interp1d(recall, precision, kind="linear", fill_value="extrapolate")
    for f_score in f_scores:
        x_vals = np.linspace(0.01, 1, 10000)
        y_vals = f_score * x_vals / (2 * x_vals - f_score)
        y_vals_clipped = np.minimum(y_vals, pr_boundary(x_vals))
        y_vals_clipped = np.clip(y_vals_clipped, 1e-3, None)  # Prevent going to zero
        valid =  y_vals_clipped < pr_boundary(x_vals)
        valid_ = y_vals_clipped > 1e-3 
        valid = valid&valid_ 
        x_vals = x_vals[valid] 
        y_vals_clipped = y_vals_clipped[valid]
        if len(x_vals) > 0:  # Ensure annotation is placed only if line segment exists
            ax.plot(x_vals, y_vals_clipped, color="gray", alpha=1)
            plt.annotate(f"$f_1={f_score:0.1f}$", xy=(0.8, y_vals_clipped[-int(len(y_vals_clipped)*0.35)] + 0.02))


    # # Plot the average precision line
    if show_avg_precision:
        plt.axhline(
            y=avg_precision,
            color="red",
            ls="--",
            lw=lw,
            label=f"Avg. precision={avg_precision:.2f}",
        )
    # Customize axes
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xlim([-0.01, 1.0])
    ax.set_ylim([0.0, 1.0])
    ax.grid(False)
    ax.legend(loc=legend_loc)
    return ax
    
def plot_cm(
    cm,
    labels_name=None,
    thresh=0.8,
    axis_labels=None,
    cmap="Reds",
    normalize=True,
    xlabel="Predicted Label",
    ylabel="Actual Label",
    fontsize=12,
    figsize=[5, 5],
    ax=None,
):
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    cm_normalized = np.round(
        cm.astype("float") / cm.sum(axis=1)[:, np.newaxis] * 100, 2
    )
    cm_value = cm_normalized if normalize else cm.astype("int")
    # Plot the heatmap
    cax = ax.imshow(cm_normalized, interpolation="nearest", cmap=cmap)
    plt.colorbar(cax, ax=ax, fraction=0.046, pad=0.04)
    cax.set_clim(0, 100)

    # Define tick labels based on provided labels
    num_local = np.arange(len(labels_name)) if labels_name is not None else range(2)
    if axis_labels is None:
        axis_labels = labels_name if labels_name is not None else ["No", "Yes"]
    ax.set_xticks(num_local)
    ax.set_xticklabels(axis_labels)
    ax.set_yticks(num_local)
    ax.set_yticklabels(axis_labels)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)

    # Add TN, FP, FN, TP annotations specifically for binary classification (2x2 matrix)
    if labels_name is None or len(labels_name) == 2:
        # True Negative (TN), False Positive (FP), False Negative (FN), and True Positive (TP)
        #                 Predicted
        #                0   |   1
        #             ----------------
        #         0 |   TN   |  FP
        # Actual      ----------------
        #         1 |   FN   |  TP
        tn_label = "TN"
        fp_label = "FP"
        fn_label = "FN"
        tp_label = "TP"

        # Adjust positions slightly for TN, FP, FN, TP labels
        ax.text(
            0,
            0,
            (
                f"{tn_label}:{cm_normalized[0, 0]:.2f}%"
                if normalize
                else f"{tn_label}:{cm_value[0, 0]}"
            ),
            ha="center",
            va="center",
            color="white" if cm_normalized[0, 0] > thresh * 100 else "black",
            fontsize=fontsize,
        )
        ax.text(
            1,
            0,
            (
                f"{fp_label}:{cm_normalized[0, 1]:.2f}%"
                if normalize
                else f"{fp_label}:{cm_value[0, 1]}"
            ),
            ha="center",
            va="center",
            color="white" if cm_normalized[0, 1] > thresh * 100 else "black",
            fontsize=fontsize,
        )
        ax.text(
            0,
            1,
            (
                f"{fn_label}:{cm_normalized[1, 0]:.2f}%"
                if normalize
                else f"{fn_label}:{cm_value[1, 0]}"
            ),
            ha="center",
            va="center",
            color="white" if cm_normalized[1, 0] > thresh * 100 else "black",
            fontsize=fontsize,
        )
        ax.text(
            1,
            1,
            (
                f"{tp_label}:{cm_normalized[1, 1]:.2f}%"
                if normalize
                else f"{tp_label}:{cm_value[1, 1]}"
            ),
            ha="center",
            va="center",
            color="white" if cm_normalized[1, 1] > thresh * 100 else "black",
            fontsize=fontsize,
        )
    else:
        # Annotate cells with normalized percentage values
        for i in range(len(labels_name)):
            for j in range(len(labels_name)):
                val = cm_normalized[i, j]
                color = "white" if val > thresh * 100 else "black"
                ax.text(
                    j,
                    i,
                    f"{val:.2f}%",
                    ha="center",
                    va="center",
                    color=color,
                    fontsize=fontsize,
                )

    plot.figsets(ax=ax, boxloc="none")
    return ax


def rank_models(
    cv_test_scores,
    rm_outlier=False,
    metric_weights=None,
    plot_=True,
):
    """
    Selects the best model based on a multi-metric scoring approach, with outlier handling, optional visualization,
    and additional performance metrics.

    Parameters:
    - cv_test_scores (pd.DataFrame): DataFrame with cross-validation results across multiple metrics.
                                     Assumes columns are 'Classifier', 'accuracy', 'precision', 'recall', 'f1', 'roc_auc'.
    - metric_weights (dict): Dictionary specifying weights for each metric (e.g., {'accuracy': 0.2, 'precision': 0.3, ...}).
                             If None, default weights are applied equally across available metrics.
                a. equal_weights(standard approch): 所有的metrics同等重要
                    e.g., {"accuracy": 0.2, "precision": 0.2, "recall": 0.2, "f1": 0.2, "roc_auc": 0.2}
                b. accuracy_focosed:  classification correctness (e.g., in balanced datasets), accuracy might be weighted more heavily.
                    e.g., {"accuracy": 0.4, "precision": 0.2, "recall": 0.2, "f1": 0.1, "roc_auc": 0.1}
                c. Precision and Recall Emphasis: In cases where false positives and false negatives are particularly important (such as
                    in medical applications or fraud detection), precision and recall may be weighted more heavily.
                    e.g., {"accuracy": 0.2, "precision": 0.3, "recall": 0.3, "f1": 0.1, "roc_auc": 0.1}
                d. F1-Focused: When balance between precision and recall is crucial (e.g., in imbalanced datasets)
                    e.g., {"accuracy": 0.2, "precision": 0.2, "recall": 0.2, "f1": 0.3, "roc_auc": 0.1}
                e. ROC-AUC Emphasis: In some cases, ROC AUC may be prioritized, particularly in classification tasks where class imbalance
                    is present, as ROC AUC accounts for the model's performance across all classification thresholds.
                    e.g., {"accuracy": 0.1, "precision": 0.2, "recall": 0.2, "f1": 0.3, "roc_auc": 0.3}

    - normalize (bool): Whether to normalize scores of each metric to range [0, 1].
    - visualize (bool): If True, generates visualizations (e.g., bar plot, radar chart).
    - outlier_threshold (float): The threshold to detect outliers using the IQR method. Default is 1.5.
    - cv_folds (int): The number of cross-validation folds used.

    Returns:
    - best_model (str): Name of the best model based on the combined metric scores.
    - scored_df (pd.DataFrame): DataFrame with an added 'combined_score' column used for model selection.
    - visualizations (dict): A dictionary containing visualizations if `visualize=True`.
    """
    from sklearn.preprocessing import MinMaxScaler
    import seaborn as sns
    import matplotlib.pyplot as plt
    from py2ls import plot

    # Check for missing metrics and set default weights if not provided
    available_metrics = cv_test_scores.columns[1:]  # Exclude 'Classifier' column
    if metric_weights is None:
        metric_weights = {
            metric: 1 / len(available_metrics) for metric in available_metrics
        }  # Equal weight if not specified
    elif metric_weights == "a":
        metric_weights = {
            "accuracy": 0.2,
            "precision": 0.2,
            "recall": 0.2,
            "f1": 0.2,
            "roc_auc": 0.2,
        }
    elif metric_weights == "b":
        metric_weights = {
            "accuracy": 0.4,
            "precision": 0.2,
            "recall": 0.2,
            "f1": 0.1,
            "roc_auc": 0.1,
        }
    elif metric_weights == "c":
        metric_weights = {
            "accuracy": 0.2,
            "precision": 0.3,
            "recall": 0.3,
            "f1": 0.1,
            "roc_auc": 0.1,
        }
    elif metric_weights == "d":
        metric_weights = {
            "accuracy": 0.2,
            "precision": 0.2,
            "recall": 0.2,
            "f1": 0.3,
            "roc_auc": 0.1,
        }
    elif metric_weights == "e":
        metric_weights = {
            "accuracy": 0.1,
            "precision": 0.2,
            "recall": 0.2,
            "f1": 0.3,
            "roc_auc": 0.3,
        }
    else:
        metric_weights = {
            metric: 1 / len(available_metrics) for metric in available_metrics
        }

    # Normalize weights if they don’t sum to 1
    total_weight = sum(metric_weights.values())
    metric_weights = {
        metric: weight / total_weight for metric, weight in metric_weights.items()
    }
    if rm_outlier:
        cv_test_scores_ = ips.df_outlier(cv_test_scores)
    else:
        cv_test_scores_ = cv_test_scores

    # Normalize the scores of metrics if normalize is True
    scaler = MinMaxScaler()
    normalized_scores = pd.DataFrame(
        scaler.fit_transform(cv_test_scores_[available_metrics]),
        columns=available_metrics,
    )
    cv_test_scores_ = pd.concat(
        [cv_test_scores_[["Classifier"]], normalized_scores], axis=1
    )

    # Calculate weighted scores for each model
    cv_test_scores_["combined_score"] = sum(
        cv_test_scores_[metric] * weight for metric, weight in metric_weights.items()
    )
    top_models = cv_test_scores_.sort_values(by="combined_score", ascending=False)
    cv_test_scores = cv_test_scores.loc[top_models.index]
    top_models.reset_index(drop=True, inplace=True)
    cv_test_scores.reset_index(drop=True, inplace=True)

    if plot_:

        def generate_bar_plot(ax, cv_test_scores):
            ax = plot.plotxy(
                y="Classifier", x="combined_score", data=cv_test_scores, kind="bar"
            )
            plt.title("Classifier Performance")
            plt.tight_layout()
            return plt

        nexttile = plot.subplot(2, 2, figsize=[10, 7])
        generate_bar_plot(nexttile(), top_models.dropna())
        plot.radar(
            ax=nexttile(projection="polar"),
            data=cv_test_scores.set_index("Classifier"),
            ylim=[0.5, 1],
            color=plot.get_color(10),
            alpha=0.05,
            circular=1,
        )
    return cv_test_scores


# # Example Usage:
# metric_weights = {
#     "accuracy": 0.2,
#     "precision": 0.3,
#     "recall": 0.2,
#     "f1": 0.2,
#     "roc_auc": 0.1,
# }
# cv_test_scores = res["cv_test_scores"].copy()
# best_model = rank_models(
#     cv_test_scores, metric_weights=metric_weights, normalize=True, plot_=True
# )

# figsave("classifier_performance.pdf")


def predict(
    x_train: pd.DataFrame,
    y_train: pd.Series,
    x_true: pd.DataFrame = None,
    y_true: Optional[pd.Series] = None,
    common_features: set = None,
    purpose: str = "classification",  # 'classification' or 'regression'
    cls: Optional[Dict[str, Any]] = None,
    metrics: Optional[List[str]] = None,
    random_state: int = 1,
    smote: bool = False,
    n_jobs: int = -1,
    plot_: bool = True,
    dir_save: str = "./",
    test_size: float = 0.2,  # specific only when x_true is None
    cv_folds: int = 5,  # more cv_folds 得更加稳定,auc可能更低
    cv_level: str = "l",  # "s":'low',"m":'medium',"l":"high"
    class_weight: str = "balanced",
    verbose: bool = False,
) -> pd.DataFrame:
    """
    第一种情况是内部拆分，第二种是直接预测，第三种是外部验证。
    Usage:
        (1). predict(x_train, y_train,...) 对 x_train 进行拆分训练/测试集，并在测试集上进行验证.
            predict 函数会根据 test_size 参数，将 x_train 和 y_train 拆分出内部测试集。然后模型会在拆分出的训练集上进行训练，并在测试集上验证效果。
        (2). predict(x_train, y_train, x_true,...)使用 x_train 和 y_train 训练并对 x_true 进行预测
            由于传入了 x_true，函数会跳过 x_train 的拆分，直接使用全部的 x_train 和 y_train 进行训练。然后对 x_true 进行预测，但由于没有提供 y_true，
            因此无法与真实值进行对比。
        (3). predict(x_train, y_train, x_true, y_true,...)使用 x_train 和 y_train 训练，并验证 x_true 与真实标签 y_true.
            predict 函数会在 x_train 和 y_train 上进行训练，并将 x_true 作为测试集。由于提供了 y_true，函数可以将预测结果与 y_true 进行对比，从而
            计算验证指标，完成对 x_true 的真正验证。
    trains and validates a variety of machine learning models for both classification and regression tasks.
    It supports hyperparameter tuning with grid search and includes additional features like cross-validation,
    feature scaling, and handling of class imbalance through SMOTE.

    Parameters:
        - x_train (pd.DataFrame):Training feature data, structured with each row as an observation and each column as a feature.
        - y_train (pd.Series):Target variable for the training dataset.
        - x_true (pd.DataFrame, optional):Test feature data. If not provided, the function splits x_train based on test_size.
        - y_true (pd.Series, optional):Test target values. If not provided, y_train is split into training and testing sets.
        - common_features (set, optional):Specifies a subset of features common across training and test data.
        - purpose (str, default = "classification"):Defines whether the task is "classification" or "regression". Determines which
            metrics and models are applied.
        - cls (dict, optional):Dictionary to specify custom classifiers/regressors. Defaults to a set of common models if not provided.
        - metrics (list, optional):List of evaluation metrics (like accuracy, F1 score) used for model evaluation.
        - random_state (int, default = 1):Random seed to ensure reproducibility.
        - smote (bool, default = False):Applies Synthetic Minority Oversampling Technique (SMOTE) to address class imbalance if enabled.
        - n_jobs (int, default = -1):Number of parallel jobs for computation. Set to -1 to use all available cores.
        - plot_ (bool, default = True):If True, generates plots of the model evaluation metrics.
        - test_size (float, default = 0.2):Test data proportion if x_true is not provided.
        - cv_folds (int, default = 5):Number of cross-validation folds.
        - cv_level (str, default = "l"):Sets the detail level of cross-validation. "s" for low, "m" for medium, and "l" for high.
        - class_weight (str, default = "balanced"):Balances class weights in classification tasks.
        - verbose (bool, default = False):If True, prints detailed output during model training.
        - dir_save (str, default = "./"):Directory path to save plot outputs and results.

    Key Steps in the Function:
        Model Initialization: Depending on purpose, initializes either classification or regression models.
        Feature Selection: Ensures training and test sets have matching feature columns.
        SMOTE Application: Balances classes if smote is enabled and the task is classification.
        Cross-Validation and Hyperparameter Tuning: Utilizes GridSearchCV for model tuning based on cv_level.
        Evaluation and Plotting: Outputs evaluation metrics like AUC, confusion matrices, and optional plotting of performance metrics.
    """
    from tqdm import tqdm
    from sklearn.ensemble import (
        RandomForestClassifier,
        RandomForestRegressor,
        ExtraTreesClassifier,
        ExtraTreesRegressor,
        BaggingClassifier,
        BaggingRegressor,
        AdaBoostClassifier,
        AdaBoostRegressor,
    )
    from sklearn.svm import SVC, SVR
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.linear_model import (
        LogisticRegression,
        ElasticNet,
        ElasticNetCV,
        LinearRegression,
        Lasso,
        RidgeClassifierCV,
        Perceptron,
        SGDClassifier,
    )
    from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
    from sklearn.naive_bayes import GaussianNB, BernoulliNB
    from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
    import xgboost as xgb
    import lightgbm as lgb
    import catboost as cb
    from sklearn.neural_network import MLPClassifier, MLPRegressor
    from sklearn.model_selection import GridSearchCV, StratifiedKFold, KFold
    from sklearn.discriminant_analysis import (
        LinearDiscriminantAnalysis,
        QuadraticDiscriminantAnalysis,
    )
    from sklearn.preprocessing import PolynomialFeatures

    # 拼写检查
    purpose = ips.strcmp(purpose, ["classification", "regression"])[0]
    print(f"{purpose} processing...")
    # Default models or regressors if not provided
    if purpose == "classification":
        model_ = {
            "Random Forest": RandomForestClassifier(
                random_state=random_state, class_weight=class_weight
            ),
            # SVC (Support Vector Classification)
            "SVM": SVC(
                kernel="rbf",
                probability=True,
                class_weight=class_weight,
                random_state=random_state,
            ),
            # fit the best model without enforcing sparsity, which means it does not directly perform feature selection.
            "Logistic Regression": LogisticRegression(
                class_weight=class_weight, random_state=random_state
            ),
            # Logistic Regression with L1 Regularization (Lasso)
            "Lasso Logistic Regression": LogisticRegression(
                penalty="l1", solver="saga", random_state=random_state
            ),
            "Gradient Boosting": GradientBoostingClassifier(random_state=random_state),
            "XGBoost": xgb.XGBClassifier(
                eval_metric="logloss",
                random_state=random_state,
            ),
            "KNN": KNeighborsClassifier(n_neighbors=5),
            "Naive Bayes": GaussianNB(),
            "Linear Discriminant Analysis": LinearDiscriminantAnalysis(),
            "AdaBoost": AdaBoostClassifier(
                algorithm="SAMME", random_state=random_state
            ),
            # "LightGBM": lgb.LGBMClassifier(random_state=random_state, class_weight=class_weight),
            "CatBoost": cb.CatBoostClassifier(verbose=0, random_state=random_state),
            "Extra Trees": ExtraTreesClassifier(
                random_state=random_state, class_weight=class_weight
            ),
            "Bagging": BaggingClassifier(random_state=random_state),
            "Neural Network": MLPClassifier(max_iter=500, random_state=random_state),
            "DecisionTree": DecisionTreeClassifier(),
            "Quadratic Discriminant Analysis": QuadraticDiscriminantAnalysis(),
            "Ridge": RidgeClassifierCV(
                class_weight=class_weight, store_cv_results=True
            ),
            "Perceptron": Perceptron(random_state=random_state),
            "Bernoulli Naive Bayes": BernoulliNB(),
            "SGDClassifier": SGDClassifier(random_state=random_state),
        }
    elif purpose == "regression":
        model_ = {
            "Random Forest": RandomForestRegressor(random_state=random_state),
            "SVM": SVR(),  # SVR (Support Vector Regression)
            # "Lasso": Lasso(random_state=random_state), # 它和LassoCV相同(必须要提供alpha参数),
            "LassoCV": LassoCV(
                cv=cv_folds, random_state=random_state
            ),  # LassoCV自动找出最适alpha,优于Lasso
            "Gradient Boosting": GradientBoostingRegressor(random_state=random_state),
            "XGBoost": xgb.XGBRegressor(eval_metric="rmse", random_state=random_state),
            "Linear Regression": LinearRegression(),
            "Lasso": Lasso(random_state=random_state),
            "AdaBoost": AdaBoostRegressor(random_state=random_state),
            # "LightGBM": lgb.LGBMRegressor(random_state=random_state),
            "CatBoost": cb.CatBoostRegressor(verbose=0, random_state=random_state),
            "Extra Trees": ExtraTreesRegressor(random_state=random_state),
            "Bagging": BaggingRegressor(random_state=random_state),
            "Neural Network": MLPRegressor(max_iter=500, random_state=random_state),
            "ElasticNet": ElasticNet(random_state=random_state),
            "Ridge": Ridge(),
            "KNN": KNeighborsRegressor(),
        }
    # indicate cls:
    if ips.run_once_within(30):  # 10 min
        print(f"supported models: {list(model_.keys())}")
    if cls is None:
        models = model_
    else:
        if not isinstance(cls, list):
            cls = [cls]
        models = {}
        for cls_ in cls:
            cls_ = ips.strcmp(cls_, list(model_.keys()))[0]
            models[cls_] = model_[cls_]
    if "LightGBM" in models:
        x_train = ips.df_special_characters_cleaner(x_train)
        x_true = (
            ips.df_special_characters_cleaner(x_true) if x_true is not None else None
        )

    if isinstance(y_train, str) and y_train in x_train.columns:
        y_train_col_name = y_train
        y_train = x_train[y_train]
        # y_train = ips.df_encoder(pd.DataFrame(y_train), method="dummy")
        x_train = x_train.drop(y_train_col_name, axis=1)
    # else:
    #     y_train = ips.df_encoder(pd.DataFrame(y_train), method="dummy").values.ravel()
    y_train=pd.DataFrame(y_train)
    y_train_=ips.df_encoder(y_train, method="dummy")
    is_binary = False if y_train_.shape[1] >1 else True
    print(is_binary)
    if is_binary:
        y_train = ips.df_encoder(pd.DataFrame(y_train), method="dummy").values.ravel() 
    if x_true is None:
        x_train, x_true, y_train, y_true = train_test_split(
            x_train,
            y_train,
            test_size=test_size,
            random_state=random_state,
            stratify=y_train if purpose == "classification" else None,
        )
        if isinstance(y_train, str) and y_train in x_train.columns:
            y_train_col_name = y_train
            y_train = x_train[y_train]
            y_train = ips.df_encoder(pd.DataFrame(y_train), method="dummy")
            x_train = x_train.drop(y_train_col_name, axis=1)
        else:
            y_train = ips.df_encoder(
                pd.DataFrame(y_train), method="dummy"
            ).values.ravel() 
        
    if y_true is not None:
        if isinstance(y_true, str) and y_true in x_true.columns:
            y_true_col_name = y_true
            y_true = x_true[y_true]
            # y_true = ips.df_encoder(pd.DataFrame(y_true), method="dummy")
            y_true =  pd.DataFrame(y_true)
            x_true = x_true.drop(y_true_col_name, axis=1)
        # else:
        #     y_true = ips.df_encoder(pd.DataFrame(y_true), method="dummy").values.ravel()

    # to convert the 2D to 1D: 2D column-vector format (like [[1], [0], [1], ...]) instead of a 1D array ([1, 0, 1, ...]

    # y_train=y_train.values.ravel() if y_train is not None else None
    # y_true=y_true.values.ravel() if y_true is not None else None
    y_train = (
        y_train.ravel() if isinstance(y_train, np.ndarray) else y_train.values.ravel()
    )
    print(len(y_train),len(y_true))
    y_true = y_true.ravel() if isinstance(y_true, np.ndarray) else y_true.values.ravel()
    print(len(y_train),len(y_true))
    # Ensure common features are selected
    if common_features is not None:
        x_train, x_true = x_train[common_features], x_true[common_features]
    else:
        share_col_names = ips.shared(x_train.columns, x_true.columns, verbose=verbose)
        x_train, x_true = x_train[share_col_names], x_true[share_col_names]

    x_train, x_true = ips.df_scaler(x_train), ips.df_scaler(x_true)
    x_train, x_true = ips.df_encoder(x_train, method="dummy"), ips.df_encoder(x_true, method="dummy") 
    # Handle class imbalance using SMOTE (only for classification)
    if (
        smote
        and purpose == "classification"
        and y_train.value_counts(normalize=True).max() < 0.8
    ):
        from imblearn.over_sampling import SMOTE

        smote_sampler = SMOTE(random_state=random_state)
        x_train, y_train = smote_sampler.fit_resample(x_train, y_train)

    # Hyperparameter grids for tuning
    if cv_level in ["low", "simple", "s", "l"]:
        param_grids = {
            "Random Forest": (
                {
                    "n_estimators": [100],  # One basic option
                    "max_depth": [None, 10],
                    "min_samples_split": [2],
                    "min_samples_leaf": [1],
                    "class_weight": [None],
                }
                if purpose == "classification"
                else {
                    "n_estimators": [100],  # One basic option
                    "max_depth": [None, 10],
                    "min_samples_split": [2],
                    "min_samples_leaf": [1],
                    "max_features": [None],
                    "bootstrap": [True],  # Only one option for simplicity
                }
            ),
            "SVM": {
                "C": [1],
                "gamma": ["scale"],
                "kernel": ["rbf"],
            },
            "Lasso": {
                "alpha": [0.1],
            },
            "LassoCV": {
                "alphas": [[0.1]],
            },
            "Logistic Regression": {
                "C": [1],
                "solver": ["lbfgs"],
                "penalty": ["l2"],
                "max_iter": [500],
            },
            "Gradient Boosting": {
                "n_estimators": [100],
                "learning_rate": [0.1],
                "max_depth": [3],
                "min_samples_split": [2],
                "subsample": [0.8],
            },
            "XGBoost": {
                "n_estimators": [100],
                "max_depth": [3],
                "learning_rate": [0.1],
                "subsample": [0.8],
                "colsample_bytree": [0.8],
            },
            "KNN": (
                {
                    "n_neighbors": [3],
                    "weights": ["uniform"],
                    "algorithm": ["auto"],
                    "p": [2],
                }
                if purpose == "classification"
                else {
                    "n_neighbors": [3],
                    "weights": ["uniform"],
                    "metric": ["euclidean"],
                    "leaf_size": [30],
                    "p": [2],
                }
            ),
            "Naive Bayes": {
                "var_smoothing": [1e-9],
            },
            "SVR": {
                "C": [1],
                "gamma": ["scale"],
                "kernel": ["rbf"],
            },
            "Linear Regression": {
                "fit_intercept": [True],
            },
            "Extra Trees": {
                "n_estimators": [100],
                "max_depth": [None, 10],
                "min_samples_split": [2],
                "min_samples_leaf": [1],
            },
            "CatBoost": {
                "iterations": [100],
                "learning_rate": [0.1],
                "depth": [3],
                "l2_leaf_reg": [1],
            },
            "LightGBM": {
                "n_estimators": [100],
                "num_leaves": [31],
                "max_depth": [10],
                "min_data_in_leaf": [20],
                "min_gain_to_split": [0.01],
                "scale_pos_weight": [10],
            },
            "Bagging": {
                "n_estimators": [50],
                "max_samples": [0.7],
                "max_features": [0.7],
            },
            "Neural Network": {
                "hidden_layer_sizes": [(50,)],
                "activation": ["relu"],
                "solver": ["adam"],
                "alpha": [0.0001],
            },
            "Decision Tree": {
                "max_depth": [None, 10],
                "min_samples_split": [2],
                "min_samples_leaf": [1],
                "criterion": ["gini"],
            },
            "AdaBoost": {
                "n_estimators": [50],
                "learning_rate": [0.5],
            },
            "Linear Discriminant Analysis": {
                "solver": ["svd"],
                "shrinkage": [None],
            },
            "Quadratic Discriminant Analysis": {
                "reg_param": [0.0],
                "priors": [None],
                "tol": [1e-4],
            },
            "Ridge": (
                {"class_weight": [None, "balanced"]}
                if purpose == "classification"
                else {
                    "alpha": [0.1, 1, 10],
                }
            ),
            "Perceptron": {
                "alpha": [1e-3],
                "penalty": ["l2"],
                "max_iter": [1000],
                "eta0": [1.0],
            },
            "Bernoulli Naive Bayes": {
                "alpha": [0.1, 1, 10],
                "binarize": [0.0],
                "fit_prior": [True],
            },
            "SGDClassifier": {
                "eta0": [0.01],
                "loss": ["hinge"],
                "penalty": ["l2"],
                "alpha": [1e-3],
                "max_iter": [1000],
                "tol": [1e-3],
                "random_state": [random_state],
                "learning_rate": ["constant"],
            },
        }
    elif cv_level in ["high", "advanced", "h"]:
        param_grids = {
            "Random Forest": (
                {
                    "n_estimators": [100, 200, 500, 700, 1000],
                    "max_depth": [None, 3, 5, 10, 15, 20, 30],
                    "min_samples_split": [2, 5, 10, 20],
                    "min_samples_leaf": [1, 2, 4],
                    "class_weight": (
                        [None, "balanced"] if purpose == "classification" else {}
                    ),
                }
                if purpose == "classification"
                else {
                    "n_estimators": [100, 200, 500, 700, 1000],
                    "max_depth": [None, 3, 5, 10, 15, 20, 30],
                    "min_samples_split": [2, 5, 10, 20],
                    "min_samples_leaf": [1, 2, 4],
                    "max_features": [
                        "auto",
                        "sqrt",
                        "log2",
                    ],  # Number of features to consider when looking for the best split
                    "bootstrap": [
                        True,
                        False,
                    ],  # Whether bootstrap samples are used when building trees
                }
            ),
            "SVM": {
                "C": [0.001, 0.01, 0.1, 1, 10, 100, 1000],
                "gamma": ["scale", "auto", 0.001, 0.01, 0.1],
                "kernel": ["linear", "rbf", "poly"],
            },
            "Logistic Regression": {
                "C": [0.001, 0.01, 0.1, 1, 10, 100, 1000],
                "solver": ["liblinear", "saga", "newton-cg", "lbfgs"],
                "penalty": ["l1", "l2", "elasticnet"],
                "max_iter": [100, 200, 300, 500],
            },
            "Lasso": {
                "alpha": [0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0],
                "max_iter": [500, 1000, 2000, 5000],
                "tol": [1e-4, 1e-5, 1e-6],
                "selection": ["cyclic", "random"],
            },
            "LassoCV": {
                "alphas": [[0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0]],
                "max_iter": [500, 1000, 2000, 5000],
                "cv": [3, 5, 10],
                "tol": [1e-4, 1e-5, 1e-6],
            },
            "Gradient Boosting": {
                "n_estimators": [100, 200, 300, 400, 500, 700, 1000],
                "learning_rate": [0.001, 0.01, 0.1, 0.2, 0.3, 0.5],
                "max_depth": [3, 5, 7, 9, 15],
                "min_samples_split": [2, 5, 10, 20],
                "subsample": [0.8, 1.0],
            },
            "XGBoost": {
                "n_estimators": [100, 200, 500, 700],
                "max_depth": [3, 5, 7, 10],
                "learning_rate": [0.01, 0.1, 0.2, 0.3],
                "subsample": [0.8, 1.0],
                "colsample_bytree": [0.8, 0.9, 1.0],
            },
            "KNN": (
                {
                    "n_neighbors": [1, 3, 5, 10, 15, 20],
                    "weights": ["uniform", "distance"],
                    "algorithm": ["auto", "ball_tree", "kd_tree", "brute"],
                    "p": [1, 2],  # 1 for Manhattan, 2 for Euclidean distance
                }
                if purpose == "classification"
                else {
                    "n_neighbors": [3, 5, 7, 9, 11],  # Number of neighbors
                    "weights": [
                        "uniform",
                        "distance",
                    ],  # Weight function used in prediction
                    "metric": [
                        "euclidean",
                        "manhattan",
                        "minkowski",
                    ],  # Distance metric
                    "leaf_size": [
                        20,
                        30,
                        40,
                        50,
                    ],  # Leaf size for KDTree or BallTree algorithms
                    "p": [
                        1,
                        2,
                    ],  # Power parameter for the Minkowski metric (1 = Manhattan, 2 = Euclidean)
                }
            ),
            "Naive Bayes": {
                "var_smoothing": [1e-10, 1e-9, 1e-8, 1e-7],
            },
            "AdaBoost": {
                "n_estimators": [50, 100, 200, 300, 500],
                "learning_rate": [0.001, 0.01, 0.1, 0.5, 1.0],
            },
            "SVR": {
                "C": [0.01, 0.1, 1, 10, 100, 1000],
                "gamma": [0.001, 0.01, 0.1, "scale", "auto"],
                "kernel": ["linear", "rbf", "poly"],
            },
            "Linear Regression": {
                "fit_intercept": [True, False],
            },
            "Lasso": {
                "alpha": [0.001, 0.01, 0.1, 1.0, 10.0, 100.0],
                "max_iter": [1000, 2000],  # Higher iteration limit for fine-tuning
            },
            "Extra Trees": {
                "n_estimators": [100, 200, 500, 700, 1000],
                "max_depth": [None, 5, 10, 15, 20, 30],
                "min_samples_split": [2, 5, 10, 20],
                "min_samples_leaf": [1, 2, 4],
            },
            "CatBoost": {
                "iterations": [100, 200, 500],
                "learning_rate": [0.001, 0.01, 0.1, 0.2],
                "depth": [3, 5, 7, 10],
                "l2_leaf_reg": [1, 3, 5, 7, 10],
                "border_count": [32, 64, 128],
            },
            "LightGBM": {
                "n_estimators": [100, 200, 500, 700, 1000],
                "learning_rate": [0.001, 0.01, 0.1, 0.2],
                "num_leaves": [31, 50, 100, 200],
                "max_depth": [-1, 5, 10, 20, 30],
                "min_child_samples": [5, 10, 20],
                "subsample": [0.8, 1.0],
                "colsample_bytree": [0.8, 0.9, 1.0],
            },
            "Neural Network": {
                "hidden_layer_sizes": [(50,), (100,), (100, 50), (200, 100)],
                "activation": ["relu", "tanh", "logistic"],
                "solver": ["adam", "sgd", "lbfgs"],
                "alpha": [0.0001, 0.001, 0.01],
                "learning_rate": ["constant", "adaptive"],
            },
            "Decision Tree": {
                "max_depth": [None, 5, 10, 20, 30],
                "min_samples_split": [2, 5, 10, 20],
                "min_samples_leaf": [1, 2, 5, 10],
                "criterion": ["gini", "entropy"],
                "splitter": ["best", "random"],
            },
            "Linear Discriminant Analysis": {
                "solver": ["svd", "lsqr", "eigen"],
                "shrinkage": [
                    None,
                    "auto",
                    0.1,
                    0.5,
                    1.0,
                ],  # shrinkage levels for 'lsqr' and 'eigen'
            },
            "Ridge": (
                {"class_weight": [None, "balanced"]}
                if purpose == "classification"
                else {
                    "alpha": [0.1, 1, 10, 100, 1000],
                    "solver": ["auto", "svd", "cholesky", "lsqr", "lbfgs"],
                    "fit_intercept": [
                        True,
                        False,
                    ],  # Whether to calculate the intercept
                    "normalize": [
                        True,
                        False,
                    ],  # If True, the regressors X will be normalized
                }
            ),
        }
    else:  # median level
        param_grids = {
            "Random Forest": (
                {
                    "n_estimators": [100, 200, 500],
                    "max_depth": [None, 10, 20, 30],
                    "min_samples_split": [2, 5, 10],
                    "min_samples_leaf": [1, 2, 4],
                    "class_weight": [None, "balanced"],
                }
                if purpose == "classification"
                else {
                    "n_estimators": [100, 200, 500],
                    "max_depth": [None, 10, 20, 30],
                    "min_samples_split": [2, 5, 10],
                    "min_samples_leaf": [1, 2, 4],
                    "max_features": [
                        "auto",
                        "sqrt",
                        "log2",
                    ],  # Number of features to consider when looking for the best split
                    "bootstrap": [
                        True,
                        False,
                    ],  # Whether bootstrap samples are used when building trees
                }
            ),
            "SVM": {
                "C": [0.1, 1, 10, 100],  # Regularization strength
                "gamma": ["scale", "auto"],  # Common gamma values
                "kernel": ["rbf", "linear", "poly"],
            },
            "Logistic Regression": {
                "C": [0.1, 1, 10, 100],  # Regularization strength
                "solver": ["lbfgs", "liblinear", "saga"],  # Common solvers
                "penalty": ["l2"],  # L2 penalty is most common
                "max_iter": [
                    500,
                    1000,
                    2000,
                ],  # Increased max_iter for better convergence
            },
            "Lasso": {
                "alpha": [0.001, 0.01, 0.1, 1.0, 10.0, 100.0],
                "max_iter": [500, 1000, 2000],
            },
            "LassoCV": {
                "alphas": [[0.001, 0.01, 0.1, 1.0, 10.0, 100.0]],
                "max_iter": [500, 1000, 2000],
            },
            "Gradient Boosting": {
                "n_estimators": [100, 200, 500],
                "learning_rate": [0.01, 0.1, 0.2],
                "max_depth": [3, 5, 7],
                "min_samples_split": [2, 5, 10],
                "subsample": [0.8, 1.0],
            },
            "XGBoost": {
                "n_estimators": [100, 200, 500],
                "max_depth": [3, 5, 7],
                "learning_rate": [0.01, 0.1, 0.2],
                "subsample": [0.8, 1.0],
                "colsample_bytree": [0.8, 1.0],
            },
            "KNN": (
                {
                    "n_neighbors": [3, 5, 7, 10],
                    "weights": ["uniform", "distance"],
                    "algorithm": ["auto", "ball_tree", "kd_tree", "brute"],
                    "p": [1, 2],
                }
                if purpose == "classification"
                else {
                    "n_neighbors": [3, 5, 7, 9, 11],  # Number of neighbors
                    "weights": [
                        "uniform",
                        "distance",
                    ],  # Weight function used in prediction
                    "metric": [
                        "euclidean",
                        "manhattan",
                        "minkowski",
                    ],  # Distance metric
                    "leaf_size": [
                        20,
                        30,
                        40,
                        50,
                    ],  # Leaf size for KDTree or BallTree algorithms
                    "p": [
                        1,
                        2,
                    ],  # Power parameter for the Minkowski metric (1 = Manhattan, 2 = Euclidean)
                }
            ),
            "Naive Bayes": {
                "var_smoothing": [1e-9, 1e-8, 1e-7],
            },
            "SVR": {
                "C": [0.1, 1, 10, 100],
                "gamma": ["scale", "auto"],
                "kernel": ["rbf", "linear"],
            },
            "Linear Regression": {
                "fit_intercept": [True, False],
            },
            "Lasso": {
                "alpha": [0.1, 1.0, 10.0],
                "max_iter": [1000, 2000],  # Sufficient iterations for convergence
            },
            "Extra Trees": {
                "n_estimators": [100, 200, 500],
                "max_depth": [None, 10, 20, 30],
                "min_samples_split": [2, 5, 10],
                "min_samples_leaf": [1, 2, 4],
            },
            "CatBoost": {
                "iterations": [100, 200],
                "learning_rate": [0.01, 0.1],
                "depth": [3, 6, 10],
                "l2_leaf_reg": [1, 3, 5, 7],
            },
            "LightGBM": {
                "n_estimators": [100, 200, 500],
                "learning_rate": [0.01, 0.1],
                "num_leaves": [31, 50, 100],
                "max_depth": [-1, 10, 20],
                "min_data_in_leaf": [20],  # Minimum samples in each leaf
                "min_gain_to_split": [0.01],  # Minimum gain to allow a split
                "scale_pos_weight": [10],  # Address class imbalance
            },
            "Bagging": {
                "n_estimators": [10, 50, 100],
                "max_samples": [0.5, 0.7, 1.0],
                "max_features": [0.5, 0.7, 1.0],
            },
            "Neural Network": {
                "hidden_layer_sizes": [(50,), (100,), (100, 50)],
                "activation": ["relu", "tanh"],
                "solver": ["adam", "sgd"],
                "alpha": [0.0001, 0.001],
            },
            "Decision Tree": {
                "max_depth": [None, 10, 20],
                "min_samples_split": [2, 10],
                "min_samples_leaf": [1, 4],
                "criterion": ["gini", "entropy"],
            },
            "AdaBoost": {
                "n_estimators": [50, 100],
                "learning_rate": [0.5, 1.0],
            },
            "Linear Discriminant Analysis": {
                "solver": ["svd", "lsqr", "eigen"],
                "shrinkage": [None, "auto"],
            },
            "Quadratic Discriminant Analysis": {
                "reg_param": [0.0, 0.1, 0.5, 1.0],  # Regularization parameter
                "priors": [None, [0.5, 0.5], [0.3, 0.7]],  # Class priors
                "tol": [
                    1e-4,
                    1e-3,
                    1e-2,
                ],  # Tolerance value for the convergence of the algorithm
            },
            "Perceptron": {
                "alpha": [1e-4, 1e-3, 1e-2],  # Regularization parameter
                "penalty": ["l2", "l1", "elasticnet"],  # Regularization penalty
                "max_iter": [1000, 2000],  # Maximum number of iterations
                "eta0": [1.0, 0.1],  # Learning rate for gradient descent
                "tol": [1e-3, 1e-4, 1e-5],  # Tolerance for stopping criteria
                "random_state": [random_state],  # Random state for reproducibility
            },
            "Bernoulli Naive Bayes": {
                "alpha": [0.1, 1.0, 10.0],  # Additive (Laplace) smoothing parameter
                "binarize": [
                    0.0,
                    0.5,
                    1.0,
                ],  # Threshold for binarizing the input features
                "fit_prior": [
                    True,
                    False,
                ],  # Whether to learn class prior probabilities
            },
            "SGDClassifier": {
                "eta0": [0.01, 0.1, 1.0],
                "loss": [
                    "hinge",
                    "log",
                    "modified_huber",
                    "squared_hinge",
                    "perceptron",
                ],  # Loss function
                "penalty": ["l2", "l1", "elasticnet"],  # Regularization penalty
                "alpha": [1e-4, 1e-3, 1e-2],  # Regularization strength
                "l1_ratio": [0.15, 0.5, 0.85],  # L1 ratio for elasticnet penalty
                "max_iter": [1000, 2000],  # Maximum number of iterations
                "tol": [1e-3, 1e-4],  # Tolerance for stopping criteria
                "random_state": [random_state],  # Random state for reproducibility
                "learning_rate": [
                    "constant",
                    "optimal",
                    "invscaling",
                    "adaptive",
                ],  # Learning rate schedule
            },
            "Ridge": (
                {"class_weight": [None, "balanced"]}
                if purpose == "classification"
                else {
                    "alpha": [0.1, 1, 10, 100],
                    "solver": [
                        "auto",
                        "svd",
                        "cholesky",
                        "lsqr",
                    ],  # Solver for optimization
                }
            ),
        }

    results = {}
    # Use StratifiedKFold for classification and KFold for regression
    cv = (
        StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=random_state)
        if purpose == "classification"
        else KFold(n_splits=cv_folds, shuffle=True, random_state=random_state)
    )

    # Train and validate each model
    for name, clf in tqdm(
        models.items(),
        desc="models",
        colour="green",
        bar_format="{l_bar}{bar} {n_fmt}/{total_fmt}",
    ):
        if verbose:
            print(f"\nTraining and validating {name}:")

        # Grid search with KFold or StratifiedKFold
        gs = GridSearchCV(
            clf,
            param_grid=param_grids.get(name, {}),
            scoring=(
                "roc_auc" if purpose == "classification" else "neg_mean_squared_error"
            ),
            cv=cv,
            n_jobs=n_jobs,
            verbose=verbose,
        )
        gs.fit(x_train, y_train)
        best_clf = gs.best_estimator_
        # make sure x_train and x_test has the same name
        x_true = x_true.reindex(columns=x_train.columns, fill_value=0)
        y_pred = best_clf.predict(x_true)

        # y_pred_proba
        if hasattr(best_clf, "predict_proba"):
            y_pred_proba = best_clf.predict_proba(x_true)[:, 1]
        elif hasattr(best_clf, "decision_function"):
            # If predict_proba is not available, use decision_function (e.g., for SVM)
            y_pred_proba = best_clf.decision_function(x_true)
            # Ensure y_pred_proba is within 0 and 1 bounds
            y_pred_proba = (y_pred_proba - y_pred_proba.min()) / (
                y_pred_proba.max() - y_pred_proba.min()
            )
        else:
            y_pred_proba = None  # No probability output for certain models

        validation_scores = {}
        if y_true is not None:
            validation_scores = cal_metrics(
                y_true,
                y_pred,
                y_pred_proba=y_pred_proba,
                is_binary=is_binary,
                purpose=purpose,
                average="weighted",
            )

            # Calculate ROC curve
            # https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html
            if y_pred_proba is not None:
                # fpr, tpr, roc_auc = dict(), dict(), dict()
                fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
                lower_ci, upper_ci = cal_auc_ci(y_true, y_pred_proba, verbose=False)
                roc_auc = auc(fpr, tpr)
                roc_info = {
                    "fpr": fpr.tolist(),
                    "tpr": tpr.tolist(),
                    "auc": roc_auc,
                    "ci95": (lower_ci, upper_ci),
                }
                # precision-recall curve
                precision_, recall_, _ = precision_recall_curve(y_true, y_pred_proba)
                avg_precision_ = average_precision_score(y_true, y_pred_proba)
                pr_info = {
                    "precision": precision_,
                    "recall": recall_,
                    "avg_precision": avg_precision_,
                }
            else:
                roc_info, pr_info = None, None
            if purpose == "classification":
                results[name] = {
                    "best_clf": gs.best_estimator_,
                    "best_params": gs.best_params_,
                    "auc_indiv": [
                        gs.cv_results_[f"split{i}_test_score"][gs.best_index_]
                        for i in range(cv_folds)
                    ],
                    "scores": validation_scores,
                    "roc_curve": roc_info,
                    "pr_curve": pr_info,
                    "confusion_matrix": confusion_matrix(y_true, y_pred),
                    "predictions": y_pred.tolist(),
                    "predictions_proba": (
                        y_pred_proba.tolist() if y_pred_proba is not None else None
                    ),
                }
            else:  # "regression"
                results[name] = {
                    "best_clf": gs.best_estimator_,
                    "best_params": gs.best_params_,
                    "scores": validation_scores,  # e.g., neg_MSE, R², etc.
                    "predictions": y_pred.tolist(),
                    "predictions_proba": (
                        y_pred_proba.tolist() if y_pred_proba is not None else None
                    ),
                }

        else:
            results[name] = {
                "best_clf": gs.best_estimator_,
                "best_params": gs.best_params_,
                "scores": validation_scores,
                "predictions": y_pred.tolist(),
                "predictions_proba": (
                    y_pred_proba.tolist() if y_pred_proba is not None else None
                ),
            }

    # Convert results to DataFrame
    df_results = pd.DataFrame.from_dict(results, orient="index")

    # sort
    if y_true is not None and purpose == "classification":
        df_scores = pd.DataFrame(
            df_results["scores"].tolist(), index=df_results["scores"].index
        ).sort_values(by="roc_auc", ascending=False)
        df_results = df_results.loc[df_scores.index]

        if plot_:
            from datetime import datetime

            now_ = datetime.now().strftime("%y%m%d_%H%M%S")
            nexttile = plot.subplot(figsize=[12, 10])
            plot.heatmap(df_scores, kind="direct", ax=nexttile())
            plot.figsets(xangle=30)
            if dir_save:
                ips.figsave(dir_save + f"scores_sorted_heatmap{now_}.pdf")
            if df_scores.shape[0] > 1:  # draw cluster
                plot.heatmap(df_scores, kind="direct", cluster=True)
                plot.figsets(xangle=30)
                if dir_save:
                    ips.figsave(dir_save + f"scores_clus{now_}.pdf")
    if all([plot_, y_true is not None, purpose == "classification"]):
        try:
            if len(models) > 3:
                plot_validate_features(df_results)
            else:
                plot_validate_features_single(df_results, figsize=(12, 4 * len(models)))
            if dir_save:
                ips.figsave(dir_save + f"validate_features{now_}.pdf")
        except Exception as e:
            print(f"Error: 在画图的过程中出现了问题:{e}")
    return df_results


def cal_metrics(
    y_true, y_pred, y_pred_proba=None, is_binary=True,purpose="regression", average="weighted"
):
    """
    Calculate regression or classification metrics based on the purpose.

    Parameters:
    - y_true: Array of true values.
    - y_pred: Array of predicted labels for classification or predicted values for regression.
    - y_pred_proba: Array of predicted probabilities for classification (optional).
    - purpose: str, "regression" or "classification".
    - average: str, averaging method for multi-class classification ("binary", "micro", "macro", "weighted", etc.).

    Returns:
    - validation_scores: dict of computed metrics.
    """
    from sklearn.metrics import (
        mean_squared_error,
        mean_absolute_error,
        mean_absolute_percentage_error,
        explained_variance_score,
        r2_score,
        mean_squared_log_error,
        accuracy_score,
        precision_score,
        recall_score,
        f1_score,
        roc_auc_score,
        matthews_corrcoef,
        confusion_matrix,
        balanced_accuracy_score,
        average_precision_score,
        precision_recall_curve,
    )

    validation_scores = {}

    if purpose == "regression":
        y_true = np.asarray(y_true)
        y_true = y_true.ravel()
        y_pred = np.asarray(y_pred)
        y_pred = y_pred.ravel()
        # Regression metrics
        validation_scores = {
            "mse": mean_squared_error(y_true, y_pred),
            "rmse": np.sqrt(mean_squared_error(y_true, y_pred)),
            "mae": mean_absolute_error(y_true, y_pred),
            "r2": r2_score(y_true, y_pred),
            "mape": mean_absolute_percentage_error(y_true, y_pred),
            "explained_variance": explained_variance_score(y_true, y_pred),
            "mbd": np.mean(y_pred - y_true),  # Mean Bias Deviation
        }
        # Check if MSLE can be calculated
        if np.all(y_true >= 0) and np.all(y_pred >= 0):  # Ensure no negative values
            validation_scores["msle"] = mean_squared_log_error(y_true, y_pred)
        else:
            validation_scores["msle"] = "Cannot be calculated due to negative values"

    elif purpose == "classification":
        # Classification metrics
        validation_scores = {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred, average=average),
            "recall": recall_score(y_true, y_pred, average=average),
            "f1": f1_score(y_true, y_pred, average=average),
            "mcc": matthews_corrcoef(y_true, y_pred),
            "specificity": None,
            "balanced_accuracy": balanced_accuracy_score(y_true, y_pred),
        }

        # Confusion matrix to calculate specificity
        if is_binary:
            tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        else:
            cm=onfusion_matrix(y_true, y_pred)
        validation_scores["specificity"] = (
            tn / (tn + fp) if (tn + fp) > 0 else 0
        )  # Specificity calculation

        if y_pred_proba is not None:
            # Calculate ROC-AUC
            validation_scores["roc_auc"] = roc_auc_score(y_true, y_pred_proba)
            # PR-AUC (Precision-Recall AUC) calculation
            validation_scores["pr_auc"] = average_precision_score(y_true, y_pred_proba)
    else:
        raise ValueError(
            "Invalid purpose specified. Choose 'regression' or 'classification'."
        )

    return validation_scores
