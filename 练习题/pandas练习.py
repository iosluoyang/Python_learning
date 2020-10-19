# encoding: utf-8

import pandas as pd
import numpy as np

series1 = pd.Series([1, 2, 3, 4])
print("series1:\n{}\n".format(series1))

print("series1.values: {}\n".format(series1.values))

print("series1.index: {}\n".format(series1.index))



df1 = pd.DataFrame(np.arange(12).reshape(4,3),index = ['用户1','用户2','用户3','用户4'],columns=['姓名','年龄','性别'])
print("df1:\n{}\n".format(df1))