#This is a program which given int 0<=c<=9 and int 0<=p<=3315
#checks whether it is possible to shorten the spine
#of the caterpillar c on point set p using slides  

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
print("got pointsets")

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
  G_edges = [tuple(sorted(e)) for e in G.edges]
  for triang in itertools.combinations(range(n),3):
    a,b,c=triang
    if not len(set(((a,b),(a,c),(b,c))).intersection(set(G_edges))) == 2: continue
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


caterpillars = [[3, 0, 0, 1], [2, 1, 0, 1], [2, 0, 1, 1], [2, 0, 0, 2], [1, 2, 0, 1], [1, 1, 1, 1], [2, 0, 0, 0, 1], [1, 1, 0, 0, 1], [1, 0, 1, 0, 1], [1, 0, 0, 0, 0, 1]]
cp = caterpillars[caterpillar]
sp = len(cp)
pts = data[8*pointset:8*pointset+8]
pillar = seq_to_caterpillar(cp)

print("caterpillar and point set made")

global connected
global pos

#dfs function
def dfs(G):
  global connected
  global pos
  visited = [] 
  stack = []
  stack.append(list(G.edges)) 
 
  while (len(stack)): 
    edges = stack[-1] 
    stack.pop()
    H = nx.empty_graph()
    H.add_edges_from(edges)
    nx.set_node_attributes(H, pos, "pos")
    if is_caterpillar(H):
      if len([p[1] for p in H.degree if p[1]>1])<sp:
        return
      if not edges in visited: 
        visited.append(edges)
        for t in check_empty_triangles(H): 
          a,b,c = t
          pairs = set(((a,b),(b,c),(a,c)))
          (e,f) = pairs.intersection(set(edges))
          (g,) = pairs.difference(set(edges))
          one = [edge for edge in edges if not edge == e] + [g]
          one.sort()
          two = [edge for edge in edges if not edge == f] + [g]
          two.sort()
          if not one in visited: 
            stack.append(one)
          if not two in visited: 
            stack.append(two)
  connected = False
  plt.title("original")
  nx.draw(pillar, nx.get_node_attributes(pillar, 'pos'), with_labels=True, node_size=15)
  plt.savefig(f'original{caterpillar}.png')
  plt.close()
  plt.title("got stuck")
  nx.draw(H, nx.get_node_attributes(H, 'pos'), with_labels=True, node_size=15)
  plt.savefig(f'stuck{caterpillar}{pointset}.png')
  plt.close()
  return

for P in itertools.permutations(pts):
  pos = {}
  connected = True
  for j in range(n): pos[j] = P[j]
  nx.set_node_attributes(pillar, pos, "pos")
  visited = [list(pillar.edges)]
  spine_len = len(cp)
  if check_planar(pillar): dfs(pillar)
  if not connected:
    print("i got stuck here")
    break

end_time = datetime.now()
print("done ")
print(f"total time taken was {end_time-start_time}")
