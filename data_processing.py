
import pandas as pd

def get_missing_report(df):
    '''Считает пустые значения и выводит отчет'''
    report = df.isnull().sum()
    print("--- Отчет о пропущенных значениях ---")
    print(report[report > 0])
    return report

def fill_missing_values(df, column, strategy='median'):
    '''Заполняет пропуски в колонке'''
    if strategy == 'mean':
        val = df[column].mean()
    elif strategy == 'median':
        val = df[column].median()
    else:
        val = df[column].mode()[0]
    
    df[column] = df[column].fillna(val)
    return df
