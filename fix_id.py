import argparse
from itertools import groupby
from collections import defaultdict
import pandas as pd
from IPython.display import display
from numpy.core.numeric import NaN
import numpy as np
import matplotlib.pyplot as plt
from utils import * # fix wildcard import

CSV = 'frg_long.csv'
df = pd.read_csv(CSV) # Load data

id_df = df['ID'].tolist()
temp = defaultdict(lambda:len(temp))
res = [temp[ele] for ele in id_df]
res_array = np.asarray(res)
df['user_id'] = ''
df['user_id'] = res_array
df.to_csv("CSV")

id_set = set(id_df) # list to set
id_lst = list(id_set)# set to list
# print(len(id_set)) # 492

id_dict = dict(zip(id_lst, range(len(id_lst))))

# use dictionary to say hey if col is equal to key, then replace w value