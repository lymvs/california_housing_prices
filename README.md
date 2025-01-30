# Data Analysis for California Housing Prices dataset

A comprehensive data analysis flow that includes data preprocessing, exploratory data analysis (EDA), and visualizations.

## Overview
This project provides a robust framework for:
- Data preprocessing (handling missing values, encoding categorical variables, and normalizing numerical features)
- Exploratory Dat Analysis (EDA)
- Data visualization
- Report generation

## How to run
1. Clone the repository:\
```git clone https://github.com/lymvs/california_housing_prices.git```\
```cd california_housing_prices```
2. Create a virtual environment (recommended):\
```python -m venv venv```\
```source venv/Script/activate # On Linux, use: venv/bin/activate```
3. Install dependencies:\
```pip install -r requirements.txt```
4. Run the main script:\
```python3 main.py```

## Dependencies
The following Python packages are required:
- matplotlib==3.10.0
- pandas==2.2.3
- scikit_learn==1.6.1
- seaborn==0.13.2

## Design Choices
1. Preprocessing Approach
    * Using median for handling missing values due to outliers existence
    * Implements standardization for numeric features
    * Uses one-hot encoding for categorical variables
2. EDA
    * Automated visualization generation
    * Generate:
        * histograms for univariate analysis
        * scatter plots for bivariate analysis
        * correlation heatmaps for multivariate analysis
    * Reporting functionality
3. Visualizations
    * Uses seaborn and matplotlib for consistent styling
