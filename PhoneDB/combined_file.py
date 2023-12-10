import pandas as pd

# Load df1 from "PhoneDatabase3.csv"
df1 = pd.read_csv("PhoneDatabase3.csv")

# Load other DataFrames (df2, df3, df4) from additional CSV files
df2 = pd.read_csv("PhoneDatabase-3625.csv")
df3 = pd.read_csv("PhoneDatabase-3915.csv")
df4 = pd.read_csv("PhoneDatabase-6525.csv")

# Find the intersection of columns among all DataFrames
common_columns = set(df1.columns)
for df in [df2, df3, df4]:
    common_columns &= set(df.columns)

# Select common_columns in each DataFrame
df1 = df1[list(common_columns)]
df2 = df2[list(common_columns)]
df3 = df3[list(common_columns)]
df4 = df4[list(common_columns)]

# Append DataFrames
combined_data = df1.append([df2, df3, df4], ignore_index=True)

# Save the combined data to a new CSV file
combined_data.to_csv("FullDB.csv", index=False)