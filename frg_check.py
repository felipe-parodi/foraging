"""Basic foraging check:

Fig 1 is a cumulative reward intake over all patches
Fig 2 is the breakdown of reward intake by patch
Fig 3 is Patch Residence Time in both envs
Fig 3 plots Reward Outcomes by Trial

note:
RT = decision time + reaction time
Total time travel b/w patch time + in patch time"""

# Imports
import argparse
from itertools import groupby
import pandas as pd
from IPython.display import display
from numpy.core.numeric import NaN
import numpy as np
import matplotlib.pyplot as plt
from utils import *  # fix wildcard import

# 0. Take cmd argument and load data
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--id", required=True, help="input user ID")
args = vars(ap.parse_args())
USER_ID = str(args["id"])
CSV = "frg_long.csv"
df = pd.read_csv(CSV)  # Load data
ssn = df[df["ID"] == USER_ID]  # Grab first participant's session by ID

# 1. Preprocess fast and slow sessions
fst_ssn = ssn[ssn["traveltime"] == 1]  # fast env dataframe
slw_ssn = ssn[ssn["traveltime"] == 5]  # slow env dataframe
cln_fst_lst = fst_ssn["BushNo"].tolist()  # put trials in whole list
cln_slw_lst = slw_ssn["BushNo"].tolist()  # put trials in whole list
cln_fst_lols = split_lst_if_less_than(cln_fst_lst)  # split into the 2 blocks
cln_slw_lols = split_lst_if_less_than(cln_slw_lst)  # split into the 2 blocks
fst_len_block1 = len(cln_fst_lols[0])  # get length of first list
slw_len_block1 = len(cln_slw_lols[0])  # get length of first list
fst_len_block2 = len(cln_fst_lols[1])  # get length of 2nd list
slw_len_block2 = len(cln_slw_lols[1])  # get length of 2nd list

# 2. Prep for data cleaning
cln_fst_lols_lst_idx = [
    item[-1] for item in cln_fst_lols
]  # get value of last items in each list
fst_rmvblock1 = int(cln_fst_lols_lst_idx[0])  # 5 in this ex
fst_rmvblock2 = int(cln_fst_lols_lst_idx[1])  # 4 in this ex
fst_block1lst = cln_fst_lols[0]
fst_block1lst_rmv = [s for s in fst_block1lst if s != fst_rmvblock1]
fst_block2lst = cln_fst_lols[1]
fst_block2lst_rmv = [s for s in fst_block2lst if s != fst_rmvblock2]
cln_slw_lols_lst_idx = [
    item[-1] for item in cln_slw_lols
]  # get value of last items in each list
slw_rmvblock1 = int(cln_slw_lols_lst_idx[0])  # 5 in this ex
slw_rmvblock2 = int(cln_slw_lols_lst_idx[1])  # 4 in this ex
slw_block1lst = cln_slw_lols[0]
slw_block1lst_rmv = [s for s in slw_block1lst if s != slw_rmvblock1]
slw_block2lst = cln_slw_lols[1]
slw_block2lst_rmv = [s for s in slw_block2lst if s != slw_rmvblock2]

# ===PROCESSING BERRY COUNT======================================================
# get list of berryct
f_ct_lst = fst_ssn["BerryCount"].tolist()  # put fast env rewards in list
s_ct_lst = slw_ssn["BerryCount"].tolist()  # put slow env rewards in list
f_bct_nn = np.nan_to_num(f_ct_lst)  # Replace nans with 0
s_bct_nn = np.nan_to_num(s_ct_lst)
f_bct = f_bct_nn.tolist()  # array to list
s_bct = s_bct_nn.tolist()

# split into 2 chunks defined by len_block1,2
fst_sizes = [fst_len_block1, fst_len_block2]  #### FAST FIRST
fst_it_bct = iter(f_bct)
split_fst_ssns = [[next(fst_it_bct) for _ in range(size)] for size in fst_sizes]
slw_sizes = [slw_len_block1, slw_len_block2]  #### THEN SLOW
slw_it_bct = iter(s_bct)
split_slw_ssns = [[next(slw_it_bct) for _ in range(size)] for size in slw_sizes]

# Remove unneeded blocks
fst_blk1_rmv_num = fst_len_block1 - len(fst_block1lst_rmv)
fst_blk2_rmv_num = fst_len_block2 - len(fst_block2lst_rmv)
slw_blk1_rmv_num = slw_len_block1 - len(slw_block1lst_rmv)
slw_blk2_rmv_num = slw_len_block2 - len(slw_block2lst_rmv)
for i in range(0, fst_blk1_rmv_num):
    split_fst_ssns[0].pop()
for i in range(0, fst_blk2_rmv_num):
    split_fst_ssns[1].pop()
for i in range(0, slw_blk1_rmv_num):
    split_slw_ssns[0].pop()
for i in range(0, slw_blk2_rmv_num):
    split_slw_ssns[1].pop()

# merge back to one list with unneeded blocks
fst_bct_final = flatten(split_fst_ssns)
slw_bct_final = flatten(split_slw_ssns)

# Split berry ct list into trials
fst_len = len(fst_bct_final)
slw_len = len(slw_bct_final)

idx_fst_list = [
    idx + 1 for idx, val in enumerate(fst_bct_final) if val == 0.0
]  # Separate each trial by 0
fast_bct_trials_final = [
    fst_bct_final[i:j]
    for i, j in zip(
        [0] + idx_fst_list,
        idx_fst_list + ([fst_len] if idx_fst_list[-1] != fst_len else []),
    )
]
idx_slw_list = [idx + 1 for idx, val in enumerate(slw_bct_final) if val == 0.0]
slow_bct_trials_final = [
    slw_bct_final[i:j]
    for i, j in zip(
        [0] + idx_slw_list,
        idx_slw_list + ([slw_len] if idx_slw_list[-1] != slw_len else []),
    )
]

# if last item is 0, then pop
if fast_bct_trials_final[0][0] == 0.0:
    fast_bct_trials_final.pop(0)
if slow_bct_trials_final[0][0] == 0.0:
    slow_bct_trials_final.pop(0)

# ===PROCESSING TIMES======================================================
# Put all time pts into a list per environment
fst_tott_lst = fst_ssn[
    "TotalTime_sec"
].tolist()  # put all time pts in a list all times in fst env
slw_tott_lst = slw_ssn["TotalTime_sec"].tolist()  # get all times in slow env

# split into 2 chunks defined by len_block1,2
fst_it_time = iter(fst_tott_lst)
slw_it_time = iter(slw_tott_lst)
split_fst_ssns = [[next(fst_it_time) for _ in range(size)] for size in fst_sizes]
split_slw_ssns = [[next(slw_it_time) for _ in range(size)] for size in slw_sizes]

for i in range(0, fst_blk1_rmv_num):
    split_fst_ssns[0].pop()
for i in range(0, fst_blk2_rmv_num):
    split_fst_ssns[1].pop()
for i in range(0, slw_blk1_rmv_num):
    split_slw_ssns[0].pop()
for i in range(0, slw_blk2_rmv_num):
    split_slw_ssns[1].pop()

# merge back to one list
fst_time_final = flatten(split_fst_ssns)
slw_time_final = flatten(split_slw_ssns)

# # split into trials based on a separator
fast_time_trials_final = split_lst_if_less_than(fst_time_final)
slow_time_trials_final = split_lst_if_less_than(slw_time_final)

# ==PLOTTING=========================================================
# Fig 1: Total Reward Intake by environment
fast_bct_trials_final = list(map(add_to_nxt_idx, fast_bct_trials_final))
slow_bct_trials_final = list(map(add_to_nxt_idx, slow_bct_trials_final))
fast_bct_trls_flat = flatten(fast_bct_trials_final)
slow_bct_trls_flat = flatten(slow_bct_trials_final)
fst_bct_fig1 = add_to_nxt_idx(fast_bct_trls_flat)
slw_bct_fig1 = add_to_nxt_idx(slow_bct_trls_flat)
fst_time_fig1 = add_to_nxt_idx(fst_time_final)
slw_time_fig1 = add_to_nxt_idx(slw_time_final)
(fast,) = plt.plot(fst_time_fig1, fst_bct_fig1, "r", label="1s Travel")
(slow,) = plt.plot(slw_time_fig1, slw_bct_fig1, "b", label="5s Travel")
plt.title("Total Intake")
plt.ylabel("Berry Count")
plt.xlabel("Time (s)")
plt.grid(axis="x", color="0.95")
plt.legend(title="Environment Type")
plt.tight_layout()

# should fast be plotted against slow? should i order the lists so that the time bounds are similar?
# if len(fast_bct_trials_final) % 4 == 0:
# determine row, col size based on length size
# Fig 2: Reward Intake by Patch
try:
    for i in range(len(fast_bct_trials_final)):
        fig, ax = plt.subplots(figsize=(6, 7), sharex=True, sharey=True)
        plt.plot(
            fast_time_trials_final[i],
            fast_bct_trials_final[i],
            drawstyle="steps",
            label="1s Travel",
        )
        plt.plot(
            slow_time_trials_final[i],
            slow_bct_trials_final[i],
            drawstyle="steps",
            label="5s Travel",
        )
        plt.title("Patch " + str(i + 1) + " Intake")
        plt.ylabel("Berry Count")
        plt.xlabel("Time (s)")
        plt.grid(axis="x", color="0.95")
        plt.legend(title="Environment Type")
        plt.tight_layout()
except ValueError:
    fast_time_trials_final[0].pop(0)
    for i in range(len(fast_bct_trials_final)):
        fig, ax = plt.subplots(figsize=(6, 7), sharex=True, sharey=True)
        plt.plot(
            fast_time_trials_final[i],
            fast_bct_trials_final[i],
            drawstyle="steps",
            label="1s Travel",
        )
        plt.plot(
            slow_time_trials_final[i],
            slow_bct_trials_final[i],
            drawstyle="steps",
            label="5s Travel",
        )
        plt.title("Cumulative Intake in Patch" + str(i + 1))
        plt.ylabel("Berry Count")
        plt.xlabel("Time (s)")
        plt.grid(axis="x", color="0.95")
        plt.legend(title="Environment Type")
        plt.tight_layout()
        # fig.savefig('reward_intake.png')


# # FIGURE: PATCH RESIDENCE TIME BY ENVIRONMENT
fst_prt = get_prt(fst_time_final)  # Y-axis: Get bush times over session
slw_prt = get_prt(slw_time_final)  # slow env
fst_pts = [1] * len(fst_prt)  # X-axis: fast env
slw_pts = [5] * len(slw_prt)  # x-axis: slow env
fast = plt.scatter(fst_pts, fst_prt, c="r", alpha=0.3, label="1s Travel")
slow = plt.scatter(slw_pts, slw_prt, c="b", alpha=0.3, label="5s Travel")
plt.title("Patch Residence Times")
plt.ylabel("Time in Patch")
plt.xlabel("Environment")
plt.legend(title="Environment Type")
# ax = plt.gca().axes.xaxis.set_ticks([])
plt.show()


# REWARD OUTCOMES BY TRIAL
# x-axis: (right to left) leave, leave - 1, ..., leave - n
# where n = first reward in new bush

# QUESTIONS & things 2do
# draw optimal of each w/ triangle
# Do total time and totaltime_sec include traveltime? I assume so?
# - comment all code and update fxn names
# - remove packages as necessary; import fxns as needed


# fix excel user
# 1. get all unique IDs
# 2. cast to set and number
# 3. fill in excel with those
