#This is a program which given int 0<=c<=9 and int 0<=p<=3315
#checks whether it is possible to shorten the spine
#of the caterpillar c on point set p using slides
#c refers to a caterpillar on 8 vertices with spine on at least 4 vertices
#p refers to an order type on 8 points

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import itertools
import pandas as pd
import requests
from io import BytesIO
import shapely
from datetime import datetime
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("caterpillar",type=int,help="no 0-9")
parser.add_argument("pointset",type=int,help="no 0-3314")
args = parser.parse_args()

print0 = print
time0 = datetime.now()
def print(*X): 
  time = datetime.now()
  print0(f"[{time}]",*X)

start_time = datetime.now()
print("args",args)

n = 8
caterpillar = args.caterpillar
pointset = args.pointset


#reading data
def read_order_types_for_df(file_content):
    dtype = 'uint8'
    points = file_content.reshape(-1, 2)
    df = pd.DataFrame(points, columns=['x', 'y'], dtype=dtype)
    return df

def read_order_types(file_content):
    dtype = 'uint8'
    points = file_content.reshape(-1, 2)
    return points


file_url = "http://www.ist.tugraz.at/staff/aichholzer/research/rp/triangulations/ordertypes/data/otypes08.b08"

# downloading set points
response = requests.get(file_url)
file_content = response.content

# Use BytesIO to create a file-like object from the bytes content
file_like_object = BytesIO(file_content)


# Reading content into data frame
file_content_array = np.frombuffer(file_like_object.getvalue(), dtype=np.uint8)
df = read_order_types_for_df(file_content_array)
df.head()

data = read_order_types(file_content_array)
data = list(data)
data = [tuple(x) for x in data]

#generating all caterpillars

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

# functions we need

def intersect(A,B,C,D):
  if len(set([A,B,C,D])) == 4:
    line = shapely.LineString([A,B])
    other = shapely.LineString([C,D])
    return line.intersects(other)
  return False


def seq_to_caterpillar(c):
  l = len(c)
  g = nx.path_graph(l)
  spent = l
  for i in range(l):
    nx.add_star(g,[i]+[spent+j for j in range(c[i])])
    spent += c[i]
  return g

def check_planar(g):
  pos = nx.get_node_attributes(g, 'pos')
  edges = list(g.edges)
  for C in itertools.combinations(edges,2):
    e = C[0]
    f = C[1]
    if intersect(pos[e[0]],pos[e[1]],pos[f[0]],pos[f[1]]): return False
  return True

def check_empty_triangles(G):
  pos = nx.get_node_attributes(G, 'pos')
  vertices = set(range(n))
  empty_triangs = []
  for triang in itertools.combinations(range(n),3):
    a,b,c=triang
    if not len(set(((a,b),(a,c),(b,c))).intersection(set(G.edges))) == 2: continue
    t = shapely.convex_hull(shapely.MultiPoint([pos[a],pos[b],pos[c]]))
    rest = list(vertices.difference(triang))
    empty = True
    for p in rest:
      if t.contains(shapely.Point(pos[p])): empty = False
    if empty: empty_triangs.append(triang)
  return empty_triangs

def is_caterpillar(G):
  J= nx.empty_graph()
  J.add_nodes_from(G)
  J.add_edges_from(G.edges)
  spine = []
  leaf = []
  for i in range(n):
    if J.degree(i) == 1: leaf.append(i)
    else: spine.append(i)
  J.remove_nodes_from(leaf)
  if max([p[1] for p in J.degree]) > 2:return False
  return True


caterpillars = generate_caterpillars(8)[10:]
cp = caterpillars[caterpillar]
pts = data[8*pointset:8*pointset+8]
pillar = seq_to_caterpillar(cp)

print("caterpillar and point set made")

# global m 
# m = 0
global pos
global connected

def dfs(G, spine_len, used_slides):
  # global m
  global pos
  global connected
  if spine_len < len(cp):
    return
  triangles = [t for t in check_empty_triangles(G) if t not in used_slides]
  no_flips = False
  for t in triangles:
    a,b,c = t
    pairs = set(((a,b),(b,c),(a,c)))
    (e,f) = pairs.intersection(set(G.edges))
    (g,) = pairs.difference(set(G.edges))
    H = nx.empty_graph()
    H.add_nodes_from(G)
    H.add_edges_from(G.edges)
    H.remove_edge(e[0],e[1])
    H.add_edge(g[0],g[1])
    nx.set_node_attributes(H, pos, "pos")
    I = nx.empty_graph()
    I.add_nodes_from(G)
    I.add_edges_from(G.edges)
    I.remove_edge(f[0],f[1])
    I.add_edge(g[0],g[1])
    nx.set_node_attributes(I, pos, "pos")
    used_slides.append(t)
    if check_planar(H) and is_caterpillar(H):
      H_spine = len([p[1] for p in H.degree if p[1]>1])
      no_flips = False
      dfs(H, H_spine, used_slides)
    if check_planar(I) and is_caterpillar(I): 
      I_spine = len([p[1] for p in I.degree if p[1]>1])
      no_flips = False
      dfs(I, I_spine, used_slides)
  if no_flips:
    connected = False
    plt.title("original")
    nx.draw(pillar, nx.get_node_attributes(pillar, 'pos'), with_labels=False, node_size=15)
    plt.savefig(f'original{caterpillar}.png')
    plt.close()
    plt.title("got stuck")
    nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=False, node_size=15)
    plt.savefig(f'stuck{caterpillar}{pointset}.png')
    plt.close()
    return


for P in itertools.permutations(pts):
  pos = {}
  connected = True
  for j in range(n): pos[j] = P[j]
  nx.set_node_attributes(pillar, pos, "pos")
  used_slides = []
  spine_len = len(cp)
  dfs(pillar, spine_len, used_slides)
  if not connected: print("i got stuck here")

end_time = datetime.now()
print("done ")
print(f"total time taken was {end_time-start_time}")
