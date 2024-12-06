# Complexifier

This makes your pandas dataframe even worse

## Dependencies

- `pandas`
- `typo`
- `random`

## Installation

`complexifier` can be installed using `pip`

```sh
pip install complexifier
```

## Usage

Once installed you can use `complexifier` to add mistakes and outliers to your data

This library has several methods available:

`introduce_spag_error`: Each item in your pandas has a 10% chance to receive a random spelling error in the data
  
`add_or_subtract_outliers`: Adds 
- `add_standard_deviations`
- `duplicate_rows`
- `add_nulls`