# Update 28.09.2024
We have found an isolated caterpillar on 8 points.

![original8](https://github.com/user-attachments/assets/3fcb3245-9437-4890-ae36-1337fc310513)

# Caterpillar Slides

This code is related to the paper *Reconfigurations of Plane Caterpillars* and Paths by T. Antić, G. Gamboa Quintero and J. Glišić.

Abstract: Let $S$ be a point set in the plane, $\mathcal{P}(S)$ and $\mathcal{C}(S)$ sets of all plane spanning paths and caterpillars on $S$. We study reconfiguration operations on $\mathcal{P}(S)$ and $\mathcal{C}(S)$. In particular, we prove that all of the commonly studied reconfigurations on plane spanning trees still yield connected reconfiguration graphs for caterpillars when $S$ is in convex position. If $S$ is in general position, we show that the rotation, compatible flip and flip graphs of $\mathcal{C}(S)$ are connected while the slide graph is disconnected. 
For paths, we prove the existence of a connected component of size at least $2^{n-1}$ and that no component of size at most $7$ can exist in the flip graph on $\mathcal{P}(S)$.

## Contents
* python program *caterpillars.py* which given a size of point set ($7$ or $8$), a caterpillar and a pointset, checks for any permutation of the pointset if embedding the caterpillar into the permutation of points, results in a geometric caterpillar whose spine can be shortened using slides. 
* python program *generate_caterpillars.py* which given $n$ generates all caterpillars on $n$ vertices. We used this to find all caterpillars on which to run the other program.

## Why does this work? 
By Lemma $3$ in the paper we know that we can transform any caterpillar with spine of $3$ vertices into a star using slides. Therefore we start our program by checking if all caterpillars with spine of $4$ vertices can be shortened, if this is true we then continue to check if caterpillars with spine of $5$ vertices can be shortened. If this fails at any point, the slide graph is disconnected, otherwise it is connected. 

## Findings 
The program checked that for any point set on $7$ points, the slide graph of caterpillars is connected. For sets of $8$ points, it found an example of an isolated caterpillar that admits no slides. Therefore the question of connectivity of the slide graph is now resolved.
