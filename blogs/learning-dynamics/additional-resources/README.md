# Training Dynamics — additional resources

Companion to [Training Dynamics](https://jamesmldoesml.github.io/blogs/learning-dynamics/) by James Ming Liang Ang.

## Files

- **[learning-dynamics-tutorial.ipynb](learning-dynamics-tutorial.ipynb)** — self-contained notebook with questions, prediction spaces, runnable experiments and saved outputs for A1, B1, B2, C1, D1, D2, E1, D3, E2 and F1.
- **[learning_dynamics.py](learning_dynamics.py)** — reusable numerical helpers. These same helpers are embedded in the notebook, so downloading the notebook alone is sufficient.
- **[generate_phase_diagrams.py](generate_phase_diagrams.py)** — generates the B2/D2 phase-transition plots and the weight-decay/step-size diagram.
- **[check_resources.py](check_resources.py)** — numerical checks for gradients, conservation updates and known solutions.
- **[requirements.txt](requirements.txt)** — Python dependencies.
- **figures/** — generated PNG and SVG plots, compressed simulation arrays and run settings.

## Run the notebook

Use Python 3.10 or later. In this folder:

~~~sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m jupyterlab learning-dynamics-tutorial.ipynb
~~~

On Windows, activate with .venv\Scripts\activate instead.

Choose **Run → Run All Cells**. The notebook contains its helper code and does not read sibling files or access the network. Alternatively, upload it to Google Colab. NumPy, Matplotlib and SciPy are its only computational dependencies.

Each question includes a prediction space. The notebook is an experimental companion, not a replacement for the algebraic solutions in the primer. Its measured values follow its documented seeds and parameters and need not reproduce older illustrative numbers in the article.

## Generate the diagrams

Keep learning_dynamics.py beside the generator and run:

~~~sh
python generate_phase_diagrams.py --output-dir figures
~~~

For a faster, lower-resolution preview, use a separate output folder:

~~~sh
python generate_phase_diagrams.py --quick --output-dir preview
~~~

Outputs:

- [phase-transitions.png](figures/phase-transitions.png) and [phase-transitions.svg](figures/phase-transitions.svg): B2's continuous two-weight transition and D2's discontinuous three-weight transition.
- [step-size-phase-diagram.png](figures/step-size-phase-diagram.png) and [step-size-phase-diagram.svg](figures/step-size-phase-diagram.svg): the main illustration, with analytic stable-region boundaries and numerically observed oscillatory/divergent regimes.
- [step-size-phase-diagram-finite-budget.png](figures/step-size-phase-diagram-finite-budget.png) and [SVG](figures/step-size-phase-diagram-finite-budget.svg): the separate, unmodified finite-budget classification, including slow transients.
- Two .npz files contain the simulation arrays.
- [run-settings.json](figures/run-settings.json) records resolutions, budgets, initial weights, cutoffs and package versions.

The primer displays the main generated step-size image. Its stable regions are drawn from analytic boundaries, so slow critical convergence does not create a spurious yellow phase at gamma = 1/2. Oscillations and divergence beyond those boundaries are observations for the stated numerical setup, not global guarantees for all initialisations. The separate finite-budget image and .npz data retain the raw simulation classifications.

### What the diagrams measure

B2/D2 use weight decay from 0 to 0.8, matching the first-page diagram, with 0.01 spacing (0.02 in quick mode). They use independent full-batch restarts at every decay value, with step size 0.01. The three-weight plot compares initial common weights 1 and 0.3. The learned stationary branch survives up to approximately 0.2362, but a small initialisation can fall into the origin's basin at a smaller decay. The disappearance of the learned branch is distinct from the point where the two minima have equal loss.

The displayed step-size bounds are 0 to 1.6; simulations begin at 0.02 because a zero step performs no training. The step-size diagram uses 81 weight-decay values from 0 to 0.8 (spacing 0.01), enough to show the phase regions without a costly fine grid. Quick mode uses 41 values (spacing 0.02). The step-size grid begins at (a, b) = (0.10, 0.11). Unequal weights allow perturbations transverse to a = b. No perturbation noise is injected during the deterministic run. The dashed guide is the local condition eta = 2 / lambda_max at the candidate minimum:

- For gamma < 1/2, lambda_max = max(2 − 4 gamma, 4 gamma).
- At the origin for gamma ≥ 1/2, lambda_max = 2 gamma + 1.

In the finite-budget diagnostic, a point is marked settled only if its final gradient norm and the variation of each weight over the final 300 updates are below 1e-5. Collapse additionally requires weight norm below 1e-4; a learned state requires product above 1e-4. Numerical divergence means weights exceed 1e6 in magnitude or become nonfinite. Orange means **bounded but not settled within the budget**, which may include oscillations or long transients. It does not by itself establish an edge-of-stability regime. Finite precision, initialisation and budget affect classification close to boundaries.

## Scientific conventions

- Updates are simultaneous: all new weights use the same old state.
- Product derivatives are computed without dividing by weights, including at zero weights.
- A1 has no weight decay. B1–E2 use the specified decay. F1 explicitly resets decay to zero.
- F1 uses accurate continuous-time integration, not finite-step descent.
- E1/E2 use fixed label noise and normalised inputs. Fresh noise during SGD is a different experiment.
- E2 evaluates exact optimal outputs over 20,000 datasets, isolating statistical error from optimisation failure.
- Settling times use the documented tolerance and finite budget. NaN means unresolved.
- D3 separates local relaxation below the saddle-node from possible slow passage above it; finite curvature at the origin does not exclude an earlier bottleneck.
- Change step sizes, budgets, initialisations and seeds to test sensitivity.

## Check the numerical helpers

~~~sh
python check_resources.py
~~~

Checks compare analytical gradients with finite differences, include zero weights, verify the finite-step imbalance identity, and compare numerical outcomes with known equilibria.

## Citation

~~~bibtex
@misc{ang2026learningdynamics,
  author = {Ang, James Ming Liang},
  title = {Training Dynamics},
  year = {2026},
  month = oct,
  note = {Science of Deep Learning: Primer Series},
  url = {https://jamesmldoesml.github.io/blogs/learning-dynamics/}
}
~~~
