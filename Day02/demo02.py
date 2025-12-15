import pandas as pd
import pandasql as ps

# SQL on pandas Dataframes
#     - pandasql
#     - duckdb

filepath= "products.csv"
df=pd.read_csv(filepath)
print("Dataframe column Types: ")
print(df.dtypes)

print("\nProduct data: ")
print(df)

query="SELECT * FROM data WHERE price BETWEEN 500 AND 1000 ORDER BY price"
result=ps.sqldf(query, {"data":df})

print("\n Query Result: ")
print(result)