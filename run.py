import numpy as np
import helpers as hp
import implementations as impl
import matplotlib.pyplot as plt
import src.utils.functions as f
import src.utils.constants as c
import src.utils.functions as utilsf
import src.model.train_model as train
import src.model.predict_model as pred
import src.evaluation.evaluation as ev
import src.features.build_features as bf
from src.utils.parameters import Parameters

from src.model.Models import Models

print("Loading data...")
x_train, x_test, y_train, train_ids, test_ids = hp.load_csv_data(c.DATA_PATH)
y_train = np.expand_dims(y_train, 1)
y_train = y_train.reshape((y_train.shape[0], 1))

parameters = Parameters(
    seed=42,
    lambda_=6e-3,
    iters=600,
    gamma=0.15,
    batch_size=32,
    degree=5,
    balance=True,
    balance_scale=3,
    drop_calculated=True,
    percentage_col=90,
    percentage_row=50,
    fill_nans="mean",
    num=0,
    how_init="zeros",
    drop_outliers=None,
)

f.set_random_seed(parameters.seed)

(
    x_train_balanced,
    y_train_balanced,
    idx_calc_columns,
    idx_nan_percent,
    x_train_full,
    initial_w,
) = bf.build_all(x_train=x_train, y_train=y_train, parameters=parameters)

print(f"Log reg for {parameters}")

acc, f1, w = train.run_cross_validation(
    x_train_balanced,
    y_train_balanced,
    5,
    impl.logistic_regression,
    Models.LOGISTIC,
    initial_w=initial_w,
    max_iters=parameters.iters,
    gamma=parameters.gamma,
)

results = ev.full_evaluation(
    x_train=x_train_balanced,
    y_train=y_train_balanced,
    x_train_full=x_train_full,
    y_train_full=y_train,
    x_test=None,
    y_test=None,
    w=w,
    results={},
    parameters=parameters,
    compute_predictions_func=pred.compute_predictions_logistic,
    loss=None,
)

bf.build_test_features(
    x_train,
    idx_calc_columns=idx_calc_columns,
    idx_nan_percent=idx_nan_percent,
    fill_nans=parameters.fill_nans,
    num=parameters.num,
    polynomial_expansion_degree=parameters.degree,
)

utilsf.create_submission(
    x=x_test,
    ids=test_ids,
    w=w,
    model=Models.LOGISTIC,
    idx_calc_columns=idx_calc_columns,
    idx_nan_percent=idx_nan_percent,
    fill_nans=parameters.fill_nans,
    num=parameters.num,
    filename="submission2.csv",
    degree=parameters.degree,
)
