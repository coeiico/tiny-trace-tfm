"""
Baselines, probes and interventions, run on saved weights.

Experiments:
- Baselines. Random walk, right-hand wall-following, DFS, and BFS shortest path, all on
  the same test mazes.
- Metrics. Solve rate, rate of legal moves, trace length relative to DFS, and steps
  beyond the optimal path.
- Shortcut-breaking tests. Larger mazes than training (length generalization), other
  generators, and loop mazes, where wall-following can circle forever while real fork
  tracking still works.
- Probes. Linear probes on the residual stream at every trace position and layer,
  predicting: current position; visited cells; the most recent fork with an unexplored
  branch; stack depth; whether the current cell is a dead end. Controls: the same probes
  on a randomly initialized model, and evaluation on held-out mazes.
- Attention. At each BACKTRACK, which earlier tokens get attention? The hypothesis is
  the matching FORK token.
- Interventions. Edit the probed representation and check behavior changes as
  predicted. Mark a branch as unexplored and the model should go back for it; mark a cell
  visited and it should avoid it. Also patch activations between two mazes that differ by
  one wall.
"""

# TODO: implement. See README.md for the plan.
