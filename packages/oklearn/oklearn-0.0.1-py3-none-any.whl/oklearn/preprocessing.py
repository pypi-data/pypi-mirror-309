import pandas as pd
import numpy as np

def get_outlier(df=None, column=None, weight=1.5):
    # 1/4 분위와 3/4 분위 지점을 np.percentile로 구함
    quantile_25 = np.quantile(df[column].values, .25)
    quantile_75 = np.quantile(df[column].values, .75)
    # quantile_25 = np.quantile(df[column].values, .25)
    # quantile_75 = np.quantile(df[column].values, .75)    
    # print('quantile_25:', quantile_25, 'quantile_75:', quantile_75)
    
    # IQR을 구하고, IQR에 1.5를 곱하여 최대값과 최소값 지점 구함
    iqr = quantile_75 - quantile_25
    print('iqr:', round(iqr, 1))
    
    iqr_weight = iqr * weight
    lowest_val = quantile_25 - iqr_weight  # 최소값: Q1 – 1.5 * IQR
    highest_val = quantile_75 + iqr_weight  # 최대값: Q3 + 1.5 * IQR
    print('lowest_val:', round(lowest_val, 1), 'highest_val:', round(highest_val, 1))
    
    # 최대값 보다 크거나, 최소값 보다 작은 값을 아웃라이어로 설정하고 DataFrame index 반환 
    outlier_index = df[column][(df[column] < lowest_val) | (df[column] > highest_val)].index
    return outlier_index

if __name__ == "__main__":
    df_contbr = pd.read_csv('../../datasets/contrib/contrib.csv')
    outlier_index = get_outlier(df_contbr, 'contb_receipt_amt')
    print(outlier_index)
