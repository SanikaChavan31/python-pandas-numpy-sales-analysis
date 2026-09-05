#Loading and Inspecting the Data
import pandas as pd
import numpy as np

# Part 1:Loading the dataset
print("Loading the dataset")
df = pd.read_csv("../data/sales_data.csv")

# Displaying first 5 records
print(df.head())

# Dataset information
df.info()

# Column data types
df.dtypes

# Checking for missing values
print("Missing values",df.isnull().sum())

# Checking for duplicating records
print("Duplicate records",df.duplicated().sum())

# Part 2: Data Cleaning
print("\nData Cleaning\n")
# 1)Handling missing values
print("Missing values before cleaning")
print(df.isnull().sum())

df["Country"] = df["Country"].fillna(df["Country"].mode()[0])
df["Quantity"] = df["Quantity"].fillna(df["Quantity"].median())
df["Discount"] = df["Discount"].fillna(df["Discount"].median())
df["Sales"] = df["Sales"].fillna(
    df["Quantity"] * df["Unit_Price"] * (1 - df["Discount"] / 100)
)
print("Missing values after cleaning")
print(df.isnull().sum())

#2)Removing duplicates
print("Duplicate values before cleaning")
print(df.duplicated().sum())
df = df.drop_duplicates()
print("Duplicate values after cleaning")
print(df.duplicated().sum())


#3)Ensure numeric columns have the correct data types
print("Column Data types before data cleaning\n")
print(df.dtypes)
numeric_columns = ["Quantity", "Unit_Price", "Discount", "Sales"]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")


# 4)Converting Order_Date to a proper date/datetime format
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
print("\nColumn Data types after data cleaning\n")
print(df.dtypes)

# 5)Standardizing text columns
df["Country"] = df["Country"].str.strip().str.title()
df["Category"] = df["Category"].str.strip().str.title()

# Part 3:Data Analysis
print("\nData Analysis\n")
# 1)Total Sales
total_sales = df["Sales"].sum()
print("Total Sales : ",total_sales)

# 2) Average Sales
avg_sales  = df["Sales"].mean()
print("\nAverage Sales : ",avg_sales)

# 3)Total Quantity Sold
quantity_sold = df["Quantity"].sum()
print("\nTotal Quantity Sold : ",quantity_sold)

# 4)Sales by Country
sales_by_country = df.groupby("Country")["Sales"].sum().sort_values(ascending=False)
print("\nSales by country\n",sales_by_country)

# 5)Sales by Category
sales_by_category = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
print("\nSales by category\n",sales_by_category)

# 6)Top 5 products based on sales
top_products = df.groupby("Product")["Sales"].sum().sort_values(ascending=False).head(5)
print("\nTop 5 product\n",top_products)

# 7)order with highest sales value
highest_value_order = df.sort_values("Sales",ascending=False).head(1)
print("\nOrder with highest sales value\n\n",highest_value_order)

# Part 4: NumPy Analysis
print("\nNumpy Analysis\n")
# average and median of the sales
sales = df["Sales"].to_numpy()
avg_by_numpy = np.mean(sales)
print("\nAverage of the Sales using numpy : ",avg_by_numpy)

median_by_numpy = np.median(sales)
print("\nMedian of the sales using numpy : ", median_by_numpy)

# Standard deviation of the Sales
standard_deviation_by_numpy = np.std(sales)
print("\nStandard deviation of the Sales using numpy : ", standard_deviation_by_numpy)

# Comparison of numpy and pandas calculation
avg_pd = df["Sales"].mean()
print("\nAverage by Pandas : ",avg_pd)
avg_np = np.mean(sales)
print("Average by Numpy : ",avg_np)
if(avg_pd==avg_np):
    print("Both calculations are same")

median_pd = df["Sales"].median()
print("\nMedian by Pandas : ",median_pd)
median_np = np.median(sales)
print("Median by Numpy : ",median_np)
if(median_pd==median_np):
    print("Both calculations are same")

# Part 5: Basic Business Insights
print("Business Insights\n")
# country with highest sales
high_sales_country = df.groupby("Country")["Sales"].sum().sort_values(ascending=False).head(1)
print(high_sales_country.index[0],"has highest sales value among all countries and its total sales is",high_sales_country.iloc[0],"\n")

# top product by sales
top_product_bysales = df.groupby("Product")["Sales"].sum().sort_values(ascending=False).head(1)
print(top_product_bysales.index[0],"is the top product according to sales\n")

# top product by quantity
top_product_byquantity = df.groupby("Product")["Quantity"].sum().sort_values(ascending=False).head(1)
print(top_product_byquantity.index[0],"is the top product according to quantity sold\n")

# best category by sales
best_category_bysales = df.groupby("Category")["Sales"].sum().sort_values(ascending=False).head(1)
print(best_category_bysales.index[0],"is the best performing category according to sales\n")

# best category by quantity
best_category_byquantity = df.groupby("Category")["Quantity"].sum().sort_values(ascending=False).head(1)
print(best_category_byquantity.index[0],"is the best performing category according to quantity sold\n")

# date of highest sales
high_sales_date = df.groupby("Order_Date")["Sales"].sum().sort_values(ascending=False).head(1)
date = high_sales_date.index[0]

print("The highest sales were recorded on:", date.strftime("%d %B %Y"),"\n")

# highest quantity sold
high_quantity = df.groupby("Product")["Quantity"].sum().sort_values(ascending=False).head(1)
print("The product with the highest quantity sold was",high_quantity.index[0],"with", high_quantity.values[0],"units.")
