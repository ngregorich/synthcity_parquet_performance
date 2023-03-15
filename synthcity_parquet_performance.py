# %% imports

import pandas as pd

# this import is to force pipreqs to install fastparquet
import fastparquet
import duckdb as db
import polars as pl
import matplotlib.pyplot as plt

# %% user variables

# SynthCity synthetic point cloud dataset: http://www.synthcity.xyz/
# download from: https://rdr.ucl.ac.uk/s/9067d92ff2f0a3297204
file_in = "area3.parquet"

# %% pandas test

# save timestamp when we start processing
start_time = pd.Timestamp.now().timestamp()
# read parquet file
pandas_df = pd.read_parquet(file_in)
# save column names of dataframe
pandas_columns = pandas_df.columns
# calculate max of R column
pandas_max_R = pandas_df.R.max()
# calculate min of G column
pandas_min_G = pandas_df.G.min()
# calculate mean of B column
pandas_mean_B = pandas_df.B.mean()
# calculate duration using post processing time stamp
pandas_time = pd.Timestamp.now().timestamp() - start_time
# print results
print(
    f"""
pandas
max(R) = {pandas_max_R} 
min(G) = {pandas_min_G}
mean(B) = {pandas_mean_B}
run = {pandas_time:.1f} seconds
"""
)

# %% duckdb test

start_time = pd.Timestamp.now().timestamp()
duckdb_columns = db.sql(
    f"""
DESCRIBE FROM read_parquet('area3.parquet')
"""
).fetchall()
duckdb_max_R = db.sql(
    f"""
SELECT MAX(R) FROM read_parquet('area3.parquet')
"""
).fetchall()
duckdb_min_G = db.sql(
    f"""
SELECT MIN(G) FROM read_parquet('area3.parquet')
"""
).fetchall()
duckdb_mean_B = db.sql(
    f"""
SELECT MEAN(B) FROM read_parquet('area3.parquet')
"""
).fetchall()
duckdb_time = pd.Timestamp.now().timestamp() - start_time
print(
    f"""
duckdb
max(R) = {duckdb_max_R[0][0]} 
min(G) = {duckdb_min_G[0][0]}
mean(B) = {duckdb_mean_B[0][0]}
run = {duckdb_time:.1f} seconds
"""
)

# %% polars test

start_time = pd.Timestamp.now().timestamp()
polars_df = pl.read_parquet(file_in)
polars_columns = polars_df.columns
polars_max_R = polars_df.select("R").max()
polars_min_G = polars_df.select("G").min()
polars_mean_B = polars_df.select("B").mean()
polars_time = pd.Timestamp.now().timestamp() - start_time
print(
    f"""
polars
max(R) = {polars_max_R.to_numpy()[0][0]} 
min(G) = {polars_min_G.to_numpy()[0][0]}
mean(B) = {polars_mean_B.to_numpy()[0][0]}
run = {polars_time:.1f} seconds
"""
)

# %% plot results

fig, ax1 = plt.subplots()
ax1.bar(
    ["pandas", "DuckDB", "Polars"],
    [pandas_time, duckdb_time, polars_time],
)
ax1.grid(alpha=0.25)
ax1.set_ylabel("Processing time (s)")
ax1.set_title("pandas / DuckDB / Polars 2.5 GB parquet performance test")

plt.savefig("synthcity_parquet_performance.png")

# %%
