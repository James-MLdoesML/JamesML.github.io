# Training Dynamics animation

A three-region Manim figure matching the article's two-layer linear network, with a dark canvas, LaTeX typography, bright trajectories, and repeated signal pulses along the network's thin arrows. Trajectories start moving immediately while three network forward passes run concurrently over the six-second training animation. Displayed training time runs from t=0 to t=5, then loops immediately.

Network captions and the symmetry explanation use LaTeX text. The frame omits the subtitle, model-assumption footnotes and bottom narration.

The origin has no text label. Equations remain still, with no expression-emphasis effects or final endpoint hold.

The standalone green loss-invariance equation is omitted; the remaining derivation differentiates the rescaling symmetry directly.

Superscript 1 on “Symmetries” refers to Kunin et al. (2021), [Neural Mechanics: Symmetry and Broken Conservation Laws in Deep Learning Dynamics](https://arxiv.org/abs/2012.04728). Superscript 2 on “conservation law” refers to Saxe, McClelland and Ganguli (2014), [Exact solutions to the nonlinear dynamics of learning in deep linear neural networks](https://arxiv.org/abs/1312.6120). Compact matching citations appear at the bottom of the animation.

Outputs in `../images/`: `learning-dynamics-animated.gif` (5760 × 3600, 6.04 seconds, infinite loop), `learning-dynamics-animated-poster.png`, and `learning-dynamics-animated.mp4`.

- **Phase portrait:** 36 initialisations in a narrow band on either side of `a=-b`, plus five starts exactly on that line. Blue and orange approach the positive and negative branches of `ab=1`. Red starts approach the saddle at the origin.
- **Network:** a two-layer, two-neuron linear network, `x → bx → abx`. The setup reads “Let's learn the identity map y=x”, followed by the squared loss and continuous gradient-flow equations. The fixed input mean square is absorbed into time.
- **Symmetries ⇒ conservation law:** the heading uses a LaTeX implication arrow. Positive rescaling preserves the model and loss; the derivation explicitly differentiates `L(λa,b/λ)=L(a,b)` with respect to the continuous symmetry parameter at `λ=1`, giving `a∂L/∂a − b∂L/∂b = 0`. Euclidean gradient flow without weight decay then gives `d(a²-b²)/dt = −2(a∂L/∂a − b∂L/∂b) = 0`. All trajectories use their basin colours, with no singled-out path or imbalance readout. The legend labels use LaTeX text.

All paths use SciPy's DOP853 solver with tight tolerances. Symmetry transformations are not training trajectories. Points exactly on the separatrix are integrated in one dimension to avoid numerical roundoff sending them into a neighbouring basin. Training time increases to t=5, then the loop resets directly, with no hold or fade-out.

Over the full solver check to t=10 (the animation displays only t=0 to t=5), maximum conservation drift is `7.79e-12`, maximum final error in `ab=1` for off-line starts is `2.05e-7`, and exact-line starts finish within `5.62e-5` of the saddle. Start, intermediate and endpoint frames and the palette-encoded GIF were visually checked.

## Reproduce

Install Python 3.11+, LaTeX with `dvisvgm`, Cairo/Pango, and the dependencies in `requirements.txt`. The scene uses Avenir Next, with Manim/Pango's fallback on systems without that font.

From this directory:

```sh
python -m pip install -r requirements.txt
python learning_dynamics_manim.py
manim -r 5760,3600 --fps 24 --media_dir /tmp/learning-dynamics-render learning_dynamics_manim.py LearningDynamics
python export_animation.py /tmp/learning-dynamics-render/videos/learning_dynamics_manim/3600p24/LearningDynamics.mp4 ../images
```

The first command that runs the scene source checks conservation drift, final product errors, and convergence of separatrix starts. The export uses one shared palette and an infinite loop. The MP4 is a smaller alternative for embedding in a web page.
