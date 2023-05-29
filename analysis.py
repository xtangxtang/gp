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


with open('000001_20171130.csv', 'r', encoding='utf-8') as file:
    data = file.readlines()
  
# print(data)
data[0] = "市场代码,证券代码,时间,最新价,成交笔数,成交额,成交量,方向,买一价,买二价,买三价,买四价,买五价,卖一价,卖二价,卖三价,卖四价,卖五价,买一量,买二量,买三量,买四量,买五量,卖一量,卖二量,卖三量,卖四量,卖五量\n"
  
with open('000001_20171130.csv', 'w', encoding='utf-8') as file:
    file.writelines(data)

dataset = pd.read_csv("000001_20171130.csv")
# dataset.head()

group_zxj = dataset.groupby("最新价").agg({'成交笔数': ['sum']})
print(group_zxj)

bin_num=len(group_zxj.index)
print(f"bin_num {bin_num}")
cjbs_list =  np.array(list(group_zxj.iloc[:, 0]))
print(cjbs_list)
entr = entropy(cjbs_list)
print("entropy: " + str(entr))