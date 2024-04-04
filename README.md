# Hardness of Approximation of k-Diameter Clustering Project

This repository contains code used in proofs of [hardness of approximation](https://en.wikipedia.org/wiki/Hardness_of_approximation) results for a certain clustering problem known as **k-diameter**. In this version, our objective function is simply the maximum distance between any two points in the same cluster.

Part of our main argument involves constructing a set of points containing three special points **X, Y, Z** with the following property: in any 3-clustering of the pointset with sufficiently small diameter, the points **X, Y, Z** must be placed in three separate clusters. The formal version of this statement is termed the *spread property*, and in our proof for L2 (Euclidean) space, we verify this property using the code in [l2-spread.py](./l2-spread.py).

The code works as follows. We start by constructing the desired set of points and identifying the three special points. We then construct a graph where points correspond to vertices and edges correspond to sufficiently large distances (at least some threshold **r**). This graph can be properly [3-colored](https://en.wikipedia.org/wiki/Graph_coloring) if and only if the original graph can be 3-clustered with sufficiently small diameter (strictly less than **r**). We also add a gadget that ensures that two vertices corresponding to special points must have the same color, thus adding the restriction that two of the three special points must be clustered together. We show that for a sufficient value of **r**, the graph *cannot* be 3-colored, proving that the spread property holds for our construction.

In order to run the code, download the latest version of [Sage](https://www.sagemath.org/). Then run the following command:
```
sage l2-spread.py
```
Alternatively, paste the contents of [l2-spread.py](,/l2-spread.py) in the [Sage Cell Server](https://sagecell.sagemath.org/)

The output `G is not 3-colorable with r = 1.304.` implies that the spread condition holds for this particular value of **r**, which is precisely the result used in the paper.
