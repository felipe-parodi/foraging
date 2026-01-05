# Imports
import math
import argparse
from itertools import groupby
import pandas as pd
from IPython.display import display
from numpy.core.numeric import NaN
import numpy as np
import matplotlib.pyplot as plt


# get user's complete data
CSV = "frg_long.csv"
df = pd.read_csv(CSV)
# USER_ID = 0

# sort by column "traveltime"
df.sort_values(by=["traveltime"])

# ssn = df[df["user_id"] == USER_ID & df[]]
# do everyone and get NAs?
# replace nas with 1000 in original dataframe
berriez = df["BerryCount"].tolist()
berriez = np.array(berriez)
berriez[np.isnan(berriez)] = 1000
df["berriez1000"] = berriez
oz = 0
total_ounces = []
for x in berriez:
    if x <= 1000 or x != oz:
        oz = oz + x
        #         print(oz)
        if x == 1000:
            y = oz + x
            total_ounces.append(y)
            oz = 0

berry_array = []
for i in total_ounces:
    i -= 2000
    berry_array.append(i)

# print(berry_array) # holds berry maxes
# totaltimes = pd.DataFrame(berriez)
totaltimes_df = df.loc[df["berriez1000"] == 1000]
totaltimes = totaltimes_df["TotalTime_sec"].tolist()
traveltime = totaltimes_df["traveltime"].tolist()
user_id = totaltimes_df["user_id"].tolist()
unique = totaltimes_df["ID"].tolist()
# print(type(totaltimes))
# print(type(berry_array))
# print(type(traveltime))
# print(type(user_id))
# print(type(unique))

berry_array = np.round(berry_array, 2)
# print(berry_array)
d = {
    "Subject": user_id,
    "ID": unique,
    "Travel Time": traveltime,
    "Berries Collected (oz)": berry_array,
    "Total Time in Patch (s)": totaltimes,
}
df_new = pd.DataFrame(d)
df_new
# df_new = pd.DataFrame(user_id, unique, traveltime, berry_array,
#                      totaltimes, columns=["Subject","ID",
#                      "Travel Time","Berries Collected (oz)",
#                      "Total Time in Patch (s)"])
# df_new = pd.DataFrame(user_id, unique, traveltime, berry_array,totaltimes)
# foraging_db_clean = df_new.to_csv(r'C:\Users\parod\Desktop\Foraging')

df_new.to_csv(r"C:\Users\parod\Desktop\Foraging\foraging_db_clean.csv")
