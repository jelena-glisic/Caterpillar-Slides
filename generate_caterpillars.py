#This is a program which given int n
#outputs all caterpillars on n vertices

import numpy as np
from datetime import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("n",type=int,help="number of vertices")
args = parser.parse_args()

print0 = print
time0 = datetime.now()
def print(*X): 
  time = datetime.now()
  print0(f"[{time}]",*X)

print("args",args)

n = args.n

def is_sym_or_forward(seq, d):
  if seq == seq[::-1]: return True
  for i in range(d-2):
    if seq[i] != seq[d-i-2]:
      if seq[i] > seq[d-i-2]: return True
      return False

def find_s(seq, d):
  j = d-3
  while seq[j] == 0: j-=1
  return j

def new_seq(seq):
  l = len(seq)
  if l == 1: return [int(seq[0]+2)]
  if l == 2: return [int(seq[0]+1), int(seq[1]+1)]
  return [int(seq[0]+1)] + [int(seq[i]) for i in range(1,l-1)] + [int(seq[l-1]+1)]

def generate_caterpillars(n,d=None):
  if d is None:
    cs = []
    for d in range(2,n):
      cs += generate_caterpillars(n,d)
    return cs
  c = [n-d-1] + list(np.zeros(d-2))
  cs = [new_seq(c)]
  while sum(c[:d-2]) > 0:
    s = find_s(c, d)
    if s == d-3:
      c[d-3] -= 1
      c[d-2] += 1
    else:
      c[s] -= 1
      c[s+1] = 1 + c[d-2]
      c[d-2] = 0
    if is_sym_or_forward(c,d):
      cs.append(new_seq(c))
  return cs

print(generate_caterpillars(n))
