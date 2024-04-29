# -*- coding: utf-8 -*-
"""random_forest_regression.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mOrb4LW47Vpq1h9ilI9Pyio5wrJjyaTb
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt

def convert_market_value(value):
    # Remove the currency symbol
    value = value.replace('€', '').strip()
    # Convert millions and thousands to float
    if value.endswith('m'):
        return float(value.replace('m', '')) * 1e6
    elif value.endswith('k'):
        return float(value.replace('k', '')) * 1e3
    else:
        return float(value)

def load_and_preprocess_data():
    players = pd.read_excel('Players.xlsx')
    transfer_values = pd.read_csv('Transfer_Values.csv')

    # Convert market values from string to float
    transfer_values['Market Value'] = transfer_values['Market Value'].apply(convert_market_value)

    data = pd.merge(players, transfer_values, left_on='Player', right_on='Name')
    X = data.drop(['Market Value', 'Name', 'Player', 'Kit Number', 'Date of Birth'], axis=1)
    y = data['Market Value']

    categorical_features = ['Nation', 'Pos', 'Squad', 'Position']
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)],
        remainder='passthrough')

    return preprocessor, X, y

def train_random_forest(preprocessor, X, y):
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f'MSE: {mse}, R2: {r2}')

    return pipeline, X_train, y_test, y_pred

def plot_feature_importances(pipeline, X_train):
    feature_names = list(X_train.columns)
    importances = pipeline.named_steps['regressor'].feature_importances_
    indices = np.argsort(importances)

    plt.figure(figsize=(10, 12))
    plt.title('Feature Importances')
    plt.barh(range(len(indices)), importances[indices], color='b', align='center')
    plt.yticks(range(len(indices)), [feature_names[i] for i in indices])
    plt.xlabel('Relative Importance')
    plt.show()

preprocessor, X, y = load_and_preprocess_data()
pipeline, X_train, y_test, y_pred = train_random_forest(preprocessor, X, y)
plot_feature_importances(pipeline, X_train)

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt

def convert_market_value(value):
    # Remove the currency symbol and convert millions and thousands to float
    value = value.replace('€', '').strip()
    if value.endswith('m'):
        return float(value[:-1]) * 1e6
    elif value.endswith('k'):
        return float(value[:-1]) * 1e3
    return float(value)

def load_and_preprocess_data():
    players = pd.read_excel('Players.xlsx')
    transfer_values = pd.read_csv('Transfer_Values.csv')

    # Convert market values from string to float
    transfer_values['Market Value'] = transfer_values['Market Value'].apply(convert_market_value)

    # Merge data on player name
    data = pd.merge(players, transfer_values, left_on='Player', right_on='Name')
    X = data.drop(['Market Value', 'Name', 'Player', 'Kit Number', 'Date of Birth'], axis=1)
    y = data['Market Value']

    # Identify categorical variables
    categorical_features = ['Nation', 'Pos', 'Squad', 'Position']
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)],
        remainder='passthrough')

    return preprocessor, X, y

def train_random_forest(preprocessor, X, y):
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f'MSE: {mse}, R2: {r2}')

    return pipeline, X_train, y_test, y_pred

def plot_feature_importances(pipeline, X_train):
    # Extract feature names correctly accounting for transformations
    feature_names = []
    for name, transformer, columns in pipeline.named_steps['preprocessor'].transformers_:
        if name == 'cat':
            feature_names.extend(transformer.get_feature_names_out(columns))
        else:
            feature_names.extend(X_train.columns[columns])

    importances = pipeline.named_steps['regressor'].feature_importances_
    indices = np.argsort(importances)

    plt.figure(figsize=(10, 12))
    plt.title('Feature Importances')
    plt.barh(range(len(indices)), importances[indices], color='b', align='center')
    plt.yticks(range(len(indices)), [feature_names[i] for i in indices])
    plt.xlabel('Relative Importance')
    plt.show()

preprocessor, X, y = load_and_preprocess_data()
pipeline, X_train, y_test, y_pred = train_random_forest(preprocessor, X, y)
plot_feature_importances(pipeline, X_train.columns)

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt

def convert_market_value(value):
    value = value.replace('€', '').strip()
    if value.endswith('m'):
        return float(value[:-1]) * 1e6
    elif value.endswith('k'):
        return float(value[:-1]) * 1e3
    return float(value)

def load_and_preprocess_data():
    players = pd.read_excel('Players.xlsx')
    transfer_values = pd.read_csv('Transfer_Values.csv')
    transfer_values['Market Value'] = transfer_values['Market Value'].apply(convert_market_value)
    data = pd.merge(players, transfer_values, left_on='Player', right_on='Name')
    X = data.drop(['Market Value', 'Name', 'Player', 'Kit Number', 'Date of Birth'], axis=1)
    y = data['Market Value']
    categorical_features = ['Nation', 'Pos', 'Squad', 'Position']
    preprocessor = ColumnTransformer(
        transformers=[('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)],
        remainder='passthrough')
    return preprocessor, X, y

def train_random_forest(preprocessor, X, y):
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f'MSE: {mse}, R2: {r2}')
    return pipeline, X_train, y_test, y_pred

def plot_feature_importances(pipeline, feature_names, top_n=20):
    # Extract feature importances from the model
    importances = pipeline.named_steps['regressor'].feature_importances_
    indices = np.argsort(importances)[-top_n:]  # Only top_n most important features

    # Plotting
    plt.figure(figsize=(10, 8))  # Increase figure size
    plt.title('Top Feature Importances')
    plt.barh(range(len(indices)), importances[indices], color='b', align='center')
    plt.yticks(range(len(indices)), [feature_names[i] for i in indices], rotation=45, ha='right', fontsize=8)
    plt.xlabel('Relative Importance')
    plt.tight_layout()  # Adjust layout
    plt.show()

# Usage with the revised function
plot_feature_importances(pipeline, feature_names, top_n=20)

def get_feature_names(pipeline):
    feature_names = []
    for name, transformer, columns in pipeline.named_steps['preprocessor'].transformers_:
        if name == 'cat':
            feature_names.extend(transformer.get_feature_names_out(columns))
        else:
            feature_names.extend(columns)
    return feature_names

preprocessor, X, y = load_and_preprocess_data()
pipeline, X_train, y_test, y_pred = train_random_forest(preprocessor, X, y)
feature_names = get_feature_names(pipeline)
plot_feature_importances(pipeline, feature_names)