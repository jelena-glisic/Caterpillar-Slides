# Caterpillar Slides

This code is related to the paper *Reconfigurations of Plane Caterpillars* and Paths by T. Antić, G. Gamboa Quintero and J. Glišić.

Abstract: Let $S$ be a point set in the plane, $\mathcal{P}(S)$ and $\mathcal{C}(S)$ sets of all plane spanning paths and caterpillars on $S$. We study reconfiguration operations on $\mathcal{P}(S)$ and $\mathcal{C}(S)$. In particular, we prove that all of the commonly studied reconfigurations on plane spanning trees still yield connected reconfiguration graphs for caterpillars when $S$ is in convex position. If $S$ is in general position, we show that the rotation, compatible flip and flip graphs of $\mathcal{C}(S)$ are connected while the slide graph is disconnected. 
For paths, we prove the existence of a connected component of size at least $2^{n-1}$ and that no component of size at most $7$ can exist in the flip graph on $\mathcal{P}(S)$.

## Contents
* python notebook *CaterpillarsOn7Vertices.ipynb* used to show that the slide graph of caterpillars is connected on point sets on $7$ vertices
* python program *caterpillars8.py* which aims to show the same for point sets on $8$ vertices

Note that we have shown that the slide graph is disconnected on $9$ or more vertices, and the only currently unanswered question is that of point sets of size $8$.
