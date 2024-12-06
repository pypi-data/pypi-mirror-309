from main import introduce_spag_error
import pandas as pd

data = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva'],
    'Age': [28, 34, 29, 42, 25],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
    'Salary': [70000, 80000, 72000, 95000, 67000]
})

for _ in range(10):
    data = pd.concat([data, data])

data = introduce_spag_error(data, columns="City")

print(data["City"].value_counts())
