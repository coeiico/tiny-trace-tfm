# tiny-trace-tfm

**An internal model of maze search.** Does a small transformer trained on DFS maze-search traces build, and use, an internal model of search?

**Status:** not started.

The question is whether a small transformer trained on maze search traces builds an internal model of search (visited cells, open forks, a DFS-like stack) and actually uses it. Beating DFS is not the goal; DFS is the teacher.

## Question

Does a small transformer trained on maze search traces build an internal model of search (visited cells, open forks, a DFS-like stack), and does it actually use it?

## Plan

- **Mazes:** N×N grids from several generators: recursive backtracker, Prim's and Wilson's. Train on one generator; keep the others for testing.
- Train on perfect mazes (exactly one path between any two cells). Make loop mazes for testing by knocking out extra walls.
- **Start and goal:** random cells, so the model can't memorize a fixed route.
- **Solver:** DFS that records its full trace: every move, every fork, every dead end and every backtrack.
- **Encoding:** maze tokens first (each cell's wall configuration, plus START and GOAL coordinates), a separator, then the trace. Train with the loss mask on the trace only.

### Example trace

```
<maze tokens> <start> <goal> SEP  E E S FORK(3,4) S S DEADEND BACKTRACK(3,4) E E N ... <goal>
```

### Model variants

| Variant | What the model sees | What it tests |
| --- | --- | --- |
| A: marked trace | Moves plus FORK, DEADEND, BACKTRACK tokens | Baseline: can it learn DFS when shown its structure? |
| B: raw moves | Moves only; backtracking appears as plain moves | Does it need the explicit markers? |
| C: path only | Only the final solution path, no search | Emergence: does search-like structure appear without being shown? |
| D: self-improved (later) | Fine-tuned on its own shorter successful traces | Can it beat its teacher, as in Searchformer? Name it with a method suffix. |

## Experiments

- **Baselines.** Random walk, right-hand wall-following, DFS, and BFS shortest path, all on the same test mazes.
- **Metrics.** Solve rate, rate of legal moves, trace length relative to DFS, and steps beyond the optimal path.
- **Shortcut-breaking tests.** Larger mazes than training (length generalization), other generators, and loop mazes, where wall-following can circle forever while real fork tracking still works.
- **Probes.** Linear probes on the residual stream at every trace position and layer, predicting: current position; visited cells; the most recent fork with an unexplored branch; stack depth; whether the current cell is a dead end. Controls: the same probes on a randomly initialized model, and evaluation on held-out mazes.
- **Attention.** At each BACKTRACK, which earlier tokens get attention? The hypothesis is the matching FORK token.
- **Interventions.** Edit the probed representation and check behavior changes as predicted. Mark a branch as unexplored and the model should go back for it; mark a cell visited and it should avoid it. Also patch activations between two mazes that differ by one wall.

## Success criteria

- Variant A solves in-distribution mazes about as reliably as DFS.
- On loop mazes it clearly beats wall-following.
- At least two probed concepts beat their controls by a wide margin.
- At least one intervention changes behavior in the predicted direction.

Plus the general checklist:

Apply this checklist with the project-specific requirements and exceptions in
[CLAUDE.md](CLAUDE.md#project-specific-scope).

- `just quick` runs end to end on CPU in under 5 minutes, as a smoke test.
- The full run fits on one consumer GPU (8–12 GB VRAM) and auto-detects cuda, mps or cpu.
- Each run saves weights, `metrics.json` and its plots to `runs/<run-name>/`.
- This README shows the headline result with plots, compares against baselines, and states negative results plainly.
- Tests cover data generators, tensor shapes and one tiny overfit check.

## Notes

- Start small: 5×5 to 8×8 mazes, tiny-transformer at default size. Scale only after the pipeline works end to end.
- Alternative name: ariadne. It forms a series with minotaur-rnn (search discovered through RL) and a possible later theseus (combining both).
- The maze generator written here is reused by minotaur-rnn, so the two projects use identical mazes.

## Quickstart

Needs [uv](https://docs.astral.sh/uv/) and [just](https://just.systems/). Everything else, Python 3.12 included, comes from uv.

```sh
just setup              # uv sync, then install the pre-commit hooks
just quick              # CPU smoke test, under 5 minutes
just train              # full run; flags pass through, e.g. --run-name wd1.0-seed0
just analyze <run>      # baselines, probes, interventions and plots
just test               # pytest
just check              # ruff and basedpyright, as in CI
```

Copy `.env.example` to `.env` (gitignored) for `HF_TOKEN` and `HF_USER`.

This repo builds on [tiny-transformer](https://github.com/coeiico/tiny-transformer), installed from GitHub. To work on both at once, run `uv add --editable ../tiny-transformer`, then switch back to the git source before committing.

## Layout

```
tiny-trace-tfm/
├── README.md                goal, plan, results with plots
├── CLAUDE.md                instructions for coding agents; AGENTS.md points here
├── .agents/                 instructions/ (Python formatting, commits) and plans/
├── pyproject.toml           metadata, dependencies, tool settings
├── uv.lock                  committed lockfile
├── .python-version          pinned by uv
├── justfile                 every routine command
├── .pre-commit-config.yaml
├── .github/workflows/ci.yml
├── src/tiny_trace_tfm/
│   └── model.py, data.py, analysis.py, mazes.py, tokens.py, baselines.py, utils.py
├── train.py                 CLI; --quick runs the CPU smoke test
├── predict.py               load weights and run inference
├── analyze.py               baselines, probes, interventions, plots
├── notebooks/               marimo notebooks for exploration
├── tests/
└── runs/                    outputs, gitignored
```

## Results

_No results yet._ The headline result with plots, the comparison against baselines, and any negative results go here.

## Sources

- Lehnert et al. 2024, Beyond A* (Searchformer)
- Gandhi et al. 2024, Stream of Search

## License

MIT
