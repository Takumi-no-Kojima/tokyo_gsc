"""
ここでは回帰分析の方法の具体例を示しています。
データセットがないため、中身はありません。

構成としては前処理、目的変数が一つの回帰分析、目的変数が複数の場合の回帰分析となっています。
本来であれば目的変数が一つと複数の場合では別のファイルが最適ですが、今回は簡易的に同じファイルに書いています。
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor  # 決定木
from sklearn.ensemble import RandomForestRegressor  # ランダムフォレスト
import xgboost as xgb  # XGB
import lightgbm as lgb  # LGB
from sklearn.multioutput import MultiOutputRegressor # 複数目的変数用
from statsmodels.tsa.vector_ar.vecm import coint_johansen
import random

"""前処理"""

# 説明変数
train_x = pd.read_csv("train_x.csv")
X = pd.DataFrame(train_x)

X = X.drop(["Date"])
X.index = train_x["Date"]

def preprocess(X):
    # いらないもの
    label2 = []
    X = X.drop(label2, axis=1)

    # 平均値で埋めるもの
    X[""] = X[""].fillna(X[""].mean())

    # 標準化
    X = X.sort_index(axis=1)
    SS = StandardScaler()
    X = pd.DataFrame(SS.fit_transform(X))
    return X

X = preprocess(X)

# 目的変数
y = pd.read_csv("train_y.csv")

# データセットを分割
X_array = np.array(X)
y_array = np.array(y)
X_train, X_test, y_train, y_test = train_test_split(X_array, y_array, test_size=0.3, random_state=0)


"""回帰分析 ポジティブ・ネガティブの場合"""
# 学習
DTR = DecisionTreeRegressor(max_depth=7)
RFR = RandomForestRegressor(n_estimators=100)
XGBR = xgb.XGBRegressor(objective="reg:linear", eval_metric='rmse')

list = [DTR, RFR, XGBR]
y_test = np.array(y_test)

for i in list:
    i.fit(X_train, y_train)

# テストデータ読み込み
X_T = pd.read_csv("test_x.csv")
# 前処理
X_T_id = X_T[""]
X_T = np.array(preprocess(X_T))
# 予測
pred = (XGBR.predict(X_T) + RFR.predict(X_T) + DTR.predict(X_T)) / 3


"""回帰分析 複数の感情の場合"""
Multi = MultiOutputRegressor(lgb.LGBMRegressor(n_estimators=500))
Multi.fit(X_train, y_train)
