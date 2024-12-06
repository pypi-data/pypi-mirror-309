import numpy as np

def MAE(y_true, y_pred):  # Mean Absolute Error
    return np.mean(np.abs(y_true - y_pred)) # metrics.mean_absolute_error

def ME(y_true, y_pred):  # Mean Error
    return np.mean(y_true - y_pred)

def MPE(y_true, y_pred):  # Mean Percentage Error
    for y in y_true:
        if y == 0:
            print('zero division is not possible')
            return
    return np.mean((y_true - y_pred) / y_true) * 100

def MAPE(y_true, y_pred):  # Mean Absolute Percentage Error
    return np.mean(np.abs(y_true - y_pred) / y_true) * 100

def MSE(y_true, y_pred):  # Mean Squared Error
    error = np.square(y_true - y_pred)  # (y_true - y_pred)**2
    # metrics.mean_squared_error
    return np.mean(error)

def RMSE(y_true, y_pred):  # Root Mean Squared Error
    error = np.square(y_true - y_pred)  # (y_true - y_pred)**2
    mse = np.mean(error)
    return np.sqrt(mse)

# log 값 변환 시 NaN등의 이슈로 log() 가 아닌 log1p() 를 이용하여 RMSLE 계산
def RMSLE(y, pred):
    log_y = np.log1p(y)
    log_pred = np.log1p(pred)
    squared_error = (log_y - log_pred) ** 2
    rmsle = np.sqrt(np.mean(squared_error))
    return rmsle
