# Modelling steps

# Data preparation

## DataInitTrain: 
1. Replace infinite values with NaN
2. 80/20 split to create train and test sets

## DataPreTrain:
1. For some of the features, we may have default values that we want to apply when the value is missing
2. For all the features that are categorical, there are to be replaced with a numeric value. To do so, we need to compute the default rate for each distinct categories within the feature, then sort in ascending order and finally apply the change.
3. All those transformation are to be saved in a json file so we can apply them to the test set as well as being used in PROD
4. Features with too many missing values are dropped based on a given threshold

# Gini analysis

## Gini analysis:
1. Computes the Gini for each individual feature
2. Each features are to be sorted from the highest gini to the lowest
3. Depending on the number of features, we might want to only focus on the first 150ish

# Single feature analysis

# Notebook:
1. For each feature, we want to generate some cells in the notebook
2. Utils to be used in the SFA: 
    - compute default rate
    - compute gini
    - feature distribution
    - relationship plot between the feature and the default rate
    - replace missing values in a dataset with mean, median, or mode
    - Remove a specified value from the column of a dataframe. To be used when removing outliers
    - group values together
    - winsorize
    - function fit a / (b + np.exp(m*x + t))
    - discretization: MDLP, quantile or numpy
    - create own bins
    - own bins for the NaN; what to do with 0s
3. Save each parameters in a config file to be used for later

# Transformation

## Transform to log odds

```python
def transform_to_log_odds(dataframe, column, output_flag):
    """
        Transform dataframe column to its log odds equivalent to ensure each column has the same score currency
         - Takes the default rate of a column
         - Replaces any extreme values (1's and 0's)
         - Converts the default rate to its log odds format
         - Formula: log( DR / (1-DR) )
         - Saves all the different possible mappings from the original value to the log odds value
         - Renames the column with _log and drops original column
         - Returns the dataframe and set of mapping tuples
    """
    dataframe = compute_default_rate(data=dataframe, feature=column, output_flag=output_flag)
    dataframe['{}_DR'.format(column)].replace(0, 0.000000000001, inplace=True)
    dataframe['{}_DR'.format(column)].replace(1, 0.999999999999, inplace=True)
    dataframe['{}_DR'.format(column)] = np.log(dataframe['{}_DR'.format(column)]/(1-dataframe['{}_DR'.format(column)]))
    mapping_tuples = set(zip(dataframe[column], dataframe['{}_DR'.format(column)]))
    dataframe.rename(columns={'{}_DR'.format(column): '{}_logOR'.format(column)}, inplace=True)
    dataframe.drop(column, axis=1, inplace=True)
    return dataframe, {column: mapping_tuples}
```
## Scale features

```python
dataframe[column] = dataframe[column].astype(float)
    standard_scaler = StandardScaler(copy=True, with_mean=True, with_std=True)
    standard_scaler.fit(dataframe[column].to_frame())
    sc_mean = standard_scaler.mean_[0]
    sigma = math.sqrt(standard_scaler.var_[0])
    dataframe['{}_stand'.format(column)] = standard_scaler.transform(dataframe[column].to_frame())
    dataframe.drop(column, axis=1, inplace=True)
    scale_metrics = [sc_mean, sigma]
    return dataframe, {column: scale_metrics}
```

