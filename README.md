Route optimization is a python package for optimize deadheads route problem, implementing beam search (BS) algorithm.

## Abstract
This paper discusses a highly effective heuristic procedure for generating optimum and near-optimum solutions
for a deadhead route problem with limit route duration which is a variety of the multi traveling salesman
problem (MTSP). In practice, temporal aspect is a necessary constraint with respect to the routing problems.
MTSP is a NP-hard problem, and computational time of exact algorithm increases exponentially as the number
of trips increases. Hence, we present a beam search (BS) algorithm which is a heuristic based on breadth-first
branch-and-bound without backtracking to solve the Deadhead route problem. BS filters out worse nodes by a
local evaluation and only keep �(called beam width) nodes according to global evaluation at each level. In our
BS, both one-step local evaluation and global evaluation are applied to estimate score of nodes by inserting
unvisited nodes of a given initial solution. The computational results on test instances from the literature show
that our beam search can obtain good solutions with effective computational times for Deadhead route
problem with time windows