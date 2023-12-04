# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 15:23:19 2023

@author: jpgarcia
"""
import pandas as pd

from fitter import DataFitter

# data = pd.read_csv('./src/data/P1.csv', delimiter=';')
path = './src/data/RCurvos.xlsx'
data = pd.read_excel(path)
cols_ignoradas = []
label = path.split('/')[3].split('.')[0]

for columna in cols_ignoradas:
    if columna in data.columns:
        data = data.drop(columna, axis=1)

fitter = DataFitter(data, label)
data = pd.DataFrame(fitter.fitting())
data.to_excel(f'./src/data/output/{label}_limits.xlsx')