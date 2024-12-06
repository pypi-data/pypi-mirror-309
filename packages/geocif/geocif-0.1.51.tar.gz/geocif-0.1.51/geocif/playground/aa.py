import pandas as pd
import numpy as np
import os
from catboost import CatBoostRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt
from tqdm import tqdm
from sklearn.linear_model import LinearRegression
from numpy.polynomial import Polynomial

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

# Load dataset
data = pd.read_csv('ukraine_maize_2010.csv')

# Define key columns and parameters
target_column = 'Yield (tn per ha)'
data.rename(columns={target_column: 'Yield'}, inplace=True)
target_column = 'Yield'
year_column = 'Harvest Year'
region_column = 'Region'
common_columns = ["Country", "Region", "Crop", "Area", "Season", "Area (ha)", "Production (tn)"]

# Add a region_ID column as a unique integer identifier
data[region_column] = data[region_column].astype("category")
data["region_ID"] = data[region_column].cat.codes

# Drop rows with NaN values
data = data.dropna()

# Extract feature columns
features = data.drop(columns=[target_column, 'Country', region_column, year_column] + common_columns)
selected_features = features.columns.tolist()

# Helper function for detrending
def detrend_data(data, method='none', aggregation='none'):
    detrended_data = data.copy()

    if method == 'difference':
        # Year-over-year differencing
        if aggregation == 'none':
            detrended_data[target_column] = detrended_data[target_column].diff()
        else:
            detrended_data[target_column] = detrended_data.groupby(region_column if aggregation == 'oblast' else None)[target_column].diff()
        detrended_data.dropna(subset=[target_column], inplace=True)

    elif method == 'linear':
        regions = data[region_column].unique()
        detrended_yield = []

        for region in regions if aggregation != 'national' else [None]:
            region_data = data if region is None else data[data[region_column] == region]
            X = region_data[[year_column]].values
            y = region_data[target_column].values
            model = LinearRegression().fit(X, y)
            trend = model.predict(X)
            detrended_yield.extend(y - trend)

        detrended_data[target_column] = detrended_yield

    elif method == 'quad':
        regions = data[region_column].unique()
        detrended_yield = []

        for region in regions if aggregation != 'national' else [None]:
            region_data = data if region is None else data[data[region_column] == region]
            X = region_data[year_column].values
            y = region_data[target_column].values
            p = Polynomial.fit(X, y, deg=2)
            trend = p(X)
            detrended_yield.extend(y - trend)

        detrended_data[target_column] = detrended_yield

    elif method == 'none':
        return detrended_data

    else:
        raise ValueError("Invalid detrending method. Use 'difference', 'linear', 'quad', or 'none'.")

    return detrended_data

# Define CatBoost evaluation function
def evaluate_model(train_data, test_data):
    X_train, y_train = train_data[selected_features], train_data[target_column]
    X_test, y_test = test_data[selected_features], test_data[target_column]

    model = CatBoostRegressor(
        iterations=2500, depth=6, random_strength=0.5,
        reg_lambda=0.1, learning_rate=0.01, loss_function="RMSE",
        silent=True, random_seed=42, cat_features=["region_ID"]
    )

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)

    return rmse, r2, mae

# Evaluate all combinations of detrending methods and aggregation levels
def evaluate_all_combinations():
    methods = ['difference', 'linear', 'quad', 'none']
    aggregations = ['none', 'oblast', 'national']
    results = []

    for method in methods:
        for aggregation in aggregations:
            print(f"Evaluating combination: Detrending Method = {method}, Aggregation Level = {aggregation}")
            for year in tqdm(years, desc=f"Yearly Evaluation for {method}-{aggregation}"):
                detrended_data = detrend_data(data, method=method, aggregation=aggregation)

                # Split data into train and test sets
                train_data = detrended_data[detrended_data[year_column] != year]
                test_data = detrended_data[detrended_data[year_column] == year]

                # Evaluate the model
                rmse, r2, mae = evaluate_model(train_data, test_data)

                # Store the results
                results.append((method, aggregation, year, rmse, r2, mae))

    # Convert results to a DataFrame
    results_df = pd.DataFrame(results, columns=["Method", "Aggregation", "Year", "RMSE", "R2", "MAE"])
    return results_df

# Main execution
years = sorted(data[year_column].unique())
results_df = evaluate_all_combinations()

# Save results to CSV
results_df.to_csv("output/detrending_evaluation_results_combinations.csv", index=False)

# Plot comparison of detrending methods and aggregation levels
def plot_comparison(results_df):
    metrics = ["RMSE", "R2", "MAE"]

    for metric in metrics:
        plt.figure(figsize=(12, 6))
        for method in ['difference', 'linear', 'quad', 'none']:
            for aggregation in ['none', 'oblast', 'national']:
                subset = results_df[(results_df["Method"] == method) & (results_df["Aggregation"] == aggregation)]
                plt.plot(subset["Year"], subset[metric], marker='o', label=f"{method}-{aggregation}")

        plt.xlabel("Year")
        plt.ylabel(metric)
        plt.title(f"Comparison of Detrending Methods and Aggregation Levels ({metric} by Year)")
        plt.legend()
        plt.grid()
        plt.savefig(f"output/detrending_comparison_{metric.lower()}.png", dpi=300)
        plt.show()

# Plot results
plot_comparison(results_df)
