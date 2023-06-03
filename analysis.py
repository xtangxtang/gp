import numpy as np
import pandas as pd
import seaborn as sns
import warnings
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.mathtext import MathTextWarning
from fitter import Fitter, get_common_distributions, get_distributions
import numpy as np
from scipy.stats import entropy
from math import log, e
import os
# Customize matplotlib
warnings.filterwarnings("ignore", message="Glyph 146 missing from current font.")

def entropy1(labels, base=None):
  value,counts = np.unique(labels, return_counts=True)
  return entropy(counts, base=base)

def entropy2(labels, base=None):
  """ Computes entropy of label distribution. """

  n_labels = len(labels)

  if n_labels <= 1:
    return 0

  value,counts = np.unique(labels, return_counts=True)
  probs = counts / n_labels
  n_classes = np.count_nonzero(probs)

  if n_classes <= 1:
    return 0

  ent = 0.

  # Compute entropy
  base = e if base is None else base
  for i in probs:
    ent -= i * log(i, base)

  return ent

def entropy3(labels, base=None):
  vc = pd.Series(labels).value_counts(normalize=True, sort=False)
  base = e if base is None else base
  return -(vc * np.log(vc)/np.log(base)).sum()

def entropy4(labels, base=None):
  value,counts = np.unique(labels, return_counts=True)
  norm_counts = counts / counts.sum()
  base = e if base is None else base
  return -(norm_counts * np.log(norm_counts)/np.log(base)).sum()

def analysis_entropy():
    dir_list = os.listdir("gp_daily")
    cwd = os.getcwd()
    os.chdir("gp_daily")
    
    col_names=["symbols"]

    entr_file = f"entropy/entropy.csv"
    if os.path.exists(entr_file):
      entropy_df = pd.read_csv(entr_file, delimiter=",")      
    else:
      entropy_df = pd.DataFrame(columns=col_names)
    entropy_df.set_index("symbols")

    for symbol in dir_list:
      print(f"{symbol}")
      datefiles = os.listdir(symbol)
      os.chdir(symbol)
      for datef in datefiles:
        dataset = pd.read_csv(datef, delimiter=",")
        date = os.path.splitext(datef)[0]        
        sliced_df = dataset.loc[:,["成交价","成交量(手)"]]
        # print(sliced_df.head)
        group_zxj = dataset.groupby("成交价").agg({'成交量(手)': ['sum']})
        # print(group_zxj) 
        bin_num=len(group_zxj.index)
        # print(f"bin_num {bin_num}")
        cjbs_list =  np.array(list(group_zxj.iloc[:, 0]))
        # print(cjbs_list)
        
        entr = entropy(cjbs_list)
        # print(f"    {date} entropy: {entr}")
        # entr = entropy1(cjbs_list)
        # print("entropy1: " + str(entr))
        # entr = entropy2(cjbs_list)
        # print("entropy2: " + str(entr))
        # entr = entropy3(cjbs_list)
        # print("entropy3: " + str(entr))
        # entr = entropy4(cjbs_list)
        # print("entropy4: " + str(entr)) 
        exist_col_names = entropy_df.columns.values.tolist()
        if (entropy_df["symbols"] == symbol).any():
          if date in exist_col_names:
            entropy_df.loc[entropy_df["symbols"] == symbol, date] = entr
            print("0 entropy_df: ")
            print(entropy_df)
          else:
            entropy_df[date]=""
            entropy_df.loc[entropy_df["symbols"] == symbol, date] = entr
            print("1 entropy_df: ")
            print(entropy_df)            
        else:
          if date in exist_col_names:
            entropy_df.loc[len(entropy_df)] = symbol
            entropy_df.loc[entropy_df["symbols"] == symbol, date] = entr
            print("2 entropy_df: ")
            print(entropy_df)  
          else:
            entropy_df.loc[len(entropy_df)] = symbol
            entropy_df[date]=""
            entropy_df.loc[entropy_df["symbols"] == symbol, date] = entr
            print("3 entropy_df: ")
            print(entropy_df) 
      os.chdir("../")
    entropy_df = entropy_df.reindex(columns=["symbols"])
    entropy_df.to_csv(cwd+"/entropy/entropy.csv")
    os.chdir(cwd)  

if __name__ == "__main__":
  analysis_entropy()