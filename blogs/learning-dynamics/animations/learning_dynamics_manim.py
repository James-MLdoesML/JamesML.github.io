"""Manim Community 0.19 scene for the Training Dynamics primer.

Render: manim -r 5760,3600 --fps 24 --media_dir /tmp/learning-dynamics-render \
    learning_dynamics_manim.py LearningDynamics
No finite-step gradient-descent approximation: trajectories use DOP853.
"""
from manim import *
from scipy.integrate import solve_ivp
import json
BG = "#0B0D12"
INK = "#F4F4F4"
MUTED = "#A6ADB9"
RULE = "#343B49"
BLUE = "#58C4DD"
ORANGE = "#FFB86B"
RED = "#FC6255"
GREEN = "#83C167"
GOLD = "#F5D76E"

config.background_color = BG
config.frame_width = 16
config.frame_height = 10


def label(content, size=22, color=INK, **kwargs):
    return Text(content, font="Avenir Next", font_size=size, color=color, **kwargs)


def equation(content, size=30, color=INK):
    return MathTex(content, font_size=size, color=color)


def field(t, w):
    a, b = w
    return np.array([b * (1 - a * b), a * (1 - a * b)])


def trajectories():
    """A thin band straddles the separatrix, plus five exact-line starts."""
    times = np.linspace(0, 10, 801)
    runs = []
    for s in np.linspace(-2, 2, 9):
        for delta in (-0.27, -0.10, 0.10, 0.27):
            initial = np.array([s + delta, -s + delta])
            sol = solve_ivp(field, (0, 10), initial, t_eval=times,
                            method="DOP853", rtol=1e-11, atol=1e-13)
            runs.append((initial, sol.y.T, BLUE if delta > 0 else ORANGE))
    for s in (-1.8, -0.9, 0, 0.9, 1.8):
        sol = solve_ivp(lambda t, z: [-z[0] * (1 + z[0]**2)],
                        (0, 10), [s], t_eval=times,
                        method="DOP853", rtol=1e-11, atol=1e-13)
        values = np.column_stack([sol.y[0], -sol.y[0]])
        runs.append((np.array([s, -s]), values, RED))
    return times, runs


class LearningDynamics(Scene):
    def construct(self):
        title = Tex(r"How a simple neural network finds its solution", font_size=40, color=INK).move_to([0, 4.48, 0])
        self.add(title)
        # Open blackboard layout, retaining the reference sketch's three regions.
        self.add(Line([.40, 3.45, 0], [.40, -4.05, 0], color=RULE, stroke_width=1),
                 Line([.95, -.57, 0], [7.0, -.57, 0], color=RULE, stroke_width=1))
        self.add(Tex("Phase portrait", font_size=29, color=INK).move_to([-5.20, 3.16, 0]))
        self.add(Tex(r"A two-layer, two-neuron linear network", font_size=26, color=INK).move_to([3.98, 3.16, 0]))
        implication_heading = equation(r"\text{Symmetries}^{1}\;\Longrightarrow\;\text{conservation law}^{2}", 28)
        implication_heading.move_to([3.98, -.96, 0])
        self.add(implication_heading)
        references = [
            r"$^{1}$ Kunin et al. (2021). \textit{Neural Mechanics: Symmetry and Broken Conservation Laws in Deep Learning Dynamics.}",
            r"$^{2}$ Saxe, McClelland \& Ganguli (2014). \textit{Exact solutions to the nonlinear dynamics of learning in deep linear neural networks.}",
        ]
        for text, y in zip(references, [-4.57, -4.84]):
            reference = Tex(r"\mbox{" + text + "}", font_size=15, color=MUTED)
            if reference.width > 14.6:
                reference.scale_to_fit_width(14.6)
            self.add(reference.move_to([0, y, 0]))

        axes = Axes(x_range=[-2.8, 2.8, 1], y_range=[-2.8, 2.8, 1],
                    x_length=6.10, y_length=6.10,
                    axis_config={"color": "#828A98", "stroke_width": 1.2,
                                 "include_ticks": True, "tick_size": .045,
                                 "include_tip": True, "tip_width": .10, "tip_height": .10})
        axes.move_to([-3.60, -.12, 0])
        for val in [-2, -1, 1, 2]:
            self.add(equation(str(val), 17, MUTED).next_to(axes.c2p(val, 0), DOWN, buff=.10))
            self.add(equation(str(val), 17, MUTED).next_to(axes.c2p(0, val), LEFT, buff=.10))
        self.add(axes, equation("a", 26).next_to(axes.x_axis.get_end(), RIGHT, buff=.08),
                 equation("b", 26).next_to(axes.y_axis.get_end(), UP, buff=.07))
        # Faint arrows show the autonomous vector field, independently of paths.
        arrows = VGroup()
        for a in np.arange(-2.45, 2.5, .40):
            for b in np.arange(-2.45, 2.5, .40):
                v = field(0, [a, b]); norm = np.linalg.norm(v)
                if norm < .18 or abs(a*b-1) < .12:
                    continue
                p = axes.c2p(a, b)
                v = np.array([v[0], v[1], 0]) / norm * .135
                arrows.add(Arrow(p-v/2, p+v/2, buff=0, color="#586171",
                                  stroke_width=1, max_tip_length_to_length_ratio=.30).set_opacity(.55))
        self.add(arrows)
        sep = DashedLine(axes.c2p(-2.65, 2.65), axes.c2p(2.65, -2.65),
                         color=RED, stroke_width=1.7, dash_length=.08)
        manifold = VGroup(*[axes.plot(lambda a: 1/a, x_range=r, color=GREEN,
                                      stroke_width=3.5, use_smoothing=True)
                            for r in [[-2.65, -1/2.65, .01], [1/2.65, 2.65, .01]]])
        self.add(sep, manifold)
        ml = equation("ab=1", 25, GREEN).move_to(axes.c2p(1.91, 1.05))
        sl = equation("a=-b", 24, RED).move_to(axes.c2p(-1.82, 2.36))
        for item in [ml, sl]:
            item.add_background_rectangle(color=BG, opacity=.92, buff=.05)
        self.add(ml, sl)
        self.add(Dot(axes.c2p(0, 0), radius=.055, color=INK))

        # Network: input --b--> hidden --a--> output. No activation/bias.
        nodes = [np.array([x, 2.38, 0]) for x in [1.78, 3.98, 6.18]]
        network_edges = VGroup()
        network_nodes = VGroup()
        for p, tex, caption in zip(nodes, ["x", "bx", "abx"], ["Input", "Hidden unit", "Output"]):
            network_nodes.add(Circle(radius=.40, color=INK, stroke_width=1.7,
                                     fill_color=BG, fill_opacity=1).move_to(p),
                              equation(tex, 26).move_to(p), Tex(caption, font_size=20, color=MUTED).move_to(p+DOWN*.67))
        for p, q, tex, col in [(nodes[0], nodes[1], "b", BLUE), (nodes[1], nodes[2], "a", ORANGE)]:
            network_edges.add(Arrow(p+RIGHT*.43, q-RIGHT*.43, buff=0, color=col,
                                    stroke_width=2, tip_length=.10,
                                    max_tip_length_to_length_ratio=.09),
                              equation(tex, 28, col).move_to((p+q)/2+UP*.29))
        self.add(network_edges, network_nodes)
        self.add(Tex(r"Let's learn the identity map $y=x$.", font_size=27, color=INK).move_to([3.98, 1.20, 0]))
        loss_line = VGroup(Tex("Then", font_size=27, color=INK),
                           equation(r"L(a,b)=\frac{1}{2}(ab-1)^2", 30))
        self.add(loss_line.arrange(RIGHT, buff=.20).move_to([3.98, .62, 0]))
        self.add(equation(r"\dot a=b(1-ab),\quad\dot b=a(1-ab)", 28).move_to([3.98, .12, 0]))

        sym = equation(r"(a,b)\mapsto\left(\lambda a,\frac{b}{\lambda}\right),\quad\lambda>0", 27)
        sym.move_to([3.98, -1.48, 0])
        self.add(sym)
        self.add(Tex(r"Differentiate the continuous symmetry at $\lambda=1$:",
                     font_size=19, color=MUTED).move_to([3.98, -2.15, 0]))
        infinitesimal = equation(r"\left.\frac{d}{d\lambda}L\!\left(\lambda a,\frac{b}{\lambda}\right)\right|_{\lambda=1}"
                                 r"=a\frac{\partial L}{\partial a}-b\frac{\partial L}{\partial b}=0", 24)
        if infinitesimal.width > 6.0:
            infinitesimal.scale_to_fit_width(6.0)
        infinitesimal.move_to([3.98, -2.75, 0])
        self.add(infinitesimal)
        conserved = equation(r"\frac{d}{dt}(a^2-b^2)=-2\left(a\frac{\partial L}{\partial a}-b\frac{\partial L}{\partial b}\right)=0", 24, GOLD)
        if conserved.width > 6.0:
            conserved.scale_to_fit_width(6.0)
        conserved.move_to([3.98, -3.48, 0])
        self.add(conserved)
        self.add(equation(r"a(t)^2-b(t)^2=a_0^2-b_0^2", 25, GOLD).move_to([3.98, -4.04, 0]))

        # LaTeX legend; every trajectory uses its basin colour.
        legend = VGroup()
        for col, tex in [(BLUE, "positive branch"), (ORANGE, "negative branch"), (RED, r"exactly on $a=-b$")]:
            legend.add(VGroup(Dot(radius=.035, color=col), Tex(tex, font_size=19, color=col)).arrange(RIGHT, buff=.09))
        legend.arrange(RIGHT, buff=.30).move_to([-3.56, -3.48, 0])
        self.add(legend)
        times, runs = trajectories()
        progress = ValueTracker(0)
        # A compact clock occupies the open lower-left corner of the plot.
        clock_label = equation("t=", 22, MUTED).move_to(axes.c2p(-2.25, -2.30))
        clock = DecimalNumber(0, num_decimal_places=1, color=MUTED, font_size=21)
        clock.next_to(clock_label, RIGHT, buff=.08)
        clock.add_updater(lambda m: m.set_value(progress.get_value()*10))
        self.add(clock_label, clock)

        moving = VGroup()
        for initial, values, col in runs:
            width = 1.7
            curve = VMobject(color=col, stroke_width=width).set_points_as_corners(
                [axes.c2p(*w) for w in values])
            curve.set_stroke(opacity=.67)
            trail = curve.copy()
            trail.pointwise_become_partial(curve, 0, 1e-6)
            trail.add_updater(lambda m, full=curve: m.pointwise_become_partial(full, 0, max(1e-6, progress.get_value())))
            head = Dot(axes.c2p(*initial), radius=.037, color=col)
            def update_head(m, data=values):
                f = progress.get_value()*(len(data)-1)
                k = min(int(f), len(data)-2)
                w = data[k]*(1-(f-k)) + data[k+1]*(f-k)
                m.move_to(axes.c2p(*w))
            head.add_updater(update_head)
            moving.add(trail, head)
            if col != RED:
                self.add(Circle(radius=.037, stroke_width=.75, color=col,
                                stroke_opacity=.4).move_to(axes.c2p(*initial)))
        self.add(moving)
        # Repeat a forward pass concurrently with gradient flow, from the first frame.
        signal = Dot(nodes[0]+RIGHT*.43, radius=.05, color=BLUE)
        def update_signal(m):
            phase = (progress.get_value()*12) % 2
            edge = 0 if phase < 1 else 1
            alpha = phase if edge == 0 else phase-1
            start = nodes[edge]+RIGHT*.43
            end = nodes[edge+1]-RIGHT*.43
            m.move_to(interpolate(start, end, alpha))
            m.set_color(BLUE if edge == 0 else ORANGE)
        signal.add_updater(update_signal)
        self.add(signal)
        self.play(progress.animate.set_value(.5), run_time=6, rate_func=linear)
        # Include the exact t=5 endpoint, then let the GIF restart immediately.
        self.wait(1 / config.frame_rate)


if __name__ == "__main__":
    times, runs = trajectories()
    drift = max(float(np.max(np.abs(v[:, 0]**2-v[:, 1]**2-(w[0]**2-w[1]**2))))
                for w, v, _ in runs)
    error = max(float(abs(v[-1, 0]*v[-1, 1]-1)) for _, v, col in runs if col != RED)
    line_end = max(float(np.linalg.norm(v[-1])) for _, v, col in runs if col == RED)
    assert drift < 1e-8, drift
    assert error < 1e-5, error
    assert line_end < 1e-4, line_end
    print(json.dumps({"trajectories": len(runs), "max_conservation_drift": drift,
                      "max_final_product_error_off_separatrix": error,
                      "max_final_distance_to_saddle_on_separatrix": line_end}, indent=2))
