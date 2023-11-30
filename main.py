# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 15:23:19 2023

@author: jpgarcia
"""
import pandas as pd

from fitter import DataFitter

# data = pd.read_csv('./src/data/P1.csv', delimiter=';')
data = pd.read_excel('./src/data/RBlindados.xlsx')
cols_ignoradas = []
label = input('Inserte un nombre simple con el que quiere nombrar el conjunto de datos: ')

for columna in cols_ignoradas:
    if columna in data.columns:
        data = data.drop(columna, axis=1)

fitter = DataFitter(data, label)
data = pd.DataFrame(fitter.fitting())
data.to_excel(f'./src/data/output/{label}_limits.xlsx')