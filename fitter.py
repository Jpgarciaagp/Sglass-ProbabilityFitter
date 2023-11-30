# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 10:02:38 2023

@author: jpgarcia
"""
from distfit import distfit
import os
import re

class DataFitter:
    def __init__(self, data, label:str):
        self.data = data
        self.label = self.clean_paths(label)
        
    def fitting(self):
        model_data = []
        for i in range(len(self.data.columns)-1):
            dfit = distfit(distr=['norm', 'gamma', 'lognorm', 'expon', 'dweibull']) # Todas las distribuciones a probar. Todas las posibles se encuentran en la documentación de la librería dfit
            selected_data = self.data.iloc[:, [i]].dropna().squeeze() # Esto sirve para convertir el dataframe en una serie
            file_name = self.clean_paths(selected_data.name)
            try:
                data_array = selected_data.to_numpy()
                if len(data_array) < 20: # No se consideran modelos con menos de 20 datos para generar las distribuciones
                    raise ValueError
                dfit.fit_transform(data_array)
                model_params = {'Label': self.label, 'Column': selected_data.name, 'CII_MIN': dfit.model['CII_min_alpha'], 'CII_MAX': dfit.model['CII_max_alpha']}
                model_data.append(model_params)
            except ValueError:
                print('La variable no tiene suficientes datos (Se necesitan más de 20 datos). Pasando a la siguiente')
            except:
                print('La variable no contiene datos para revisar. Pasando a siguiente label')
                break
            else:
                # Guardar cada modelo como un archivo binario junto a exception handling para crear las carpetas si no existen
                try:
                    dfit.save(rf'.\src\models\{self.label}_{file_name}', overwrite=True)
                except FileNotFoundError:
                    try:
                        os.mkdir('.\src\models')
                    except FileExistsError:
                        pass
                    dfit.save(rf'.\src\models\{self.label}_{file_name}', overwrite=True)
                # Generar los plots para cada modelo y guardarlos en local
                fig, ax = dfit.plot(title=f'Distribución de {self.label} - Punto {selected_data.name}', chart='cdf', n_top=4)
                try:
                    fig.savefig(rf'.\src\models\plots\{self.label}_{file_name}')
                except FileNotFoundError:
                    try:
                        os.mkdir('.\src\models\plots')
                    except FileExistsError:
                        pass
                    finally:
                        try:
                            os.mkdir(r'.\src\models\plots')
                        except FileExistsError:
                            pass
                    fig.savefig(rf".\src\models\plots\{self.label}_{file_name}")
        return model_data
    
    def clean_paths(self, input_label):
        special_symbols_pattern = r'[\'/\\_@,.\s]'
        fixed = re.sub(special_symbols_pattern, '_', input_label)
        return fixed