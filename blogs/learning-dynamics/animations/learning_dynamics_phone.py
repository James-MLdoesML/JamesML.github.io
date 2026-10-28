"""Portrait companion to the landscape figure; render lossless PNG frames.

manim -r 1080,1920 --fps 30 --format png --media_dir /tmp/learning-dynamics-phone \
    learning_dynamics_phone.py LearningDynamicsPhone
"""
from manim import *
from learning_dynamics_manim import BG, INK, MUTED, BLUE, ORANGE, RED, GREEN, GOLD, trajectories

config.background_color = BG
config.frame_width = 9
config.frame_height = 16


def tex(text, size=32, color=INK, width=8.1):
    m = Tex(r"\mbox{"+text+"}", font_size=size, color=color)
    if m.width > width:
        m.scale_to_fit_width(width)
    return m


def math(text, size=36, color=INK, width=8.1):
    m = MathTex(text, font_size=size, color=color)
    if m.width > width:
        m.scale_to_fit_width(width)
    return m


class LearningDynamicsPhone(Scene):
    def construct(self):
        self.add(tex("How a simple neural network", 38).move_to([0, 7.55, 0]),
                 tex("finds its solution", 38).move_to([0, 7.08, 0]))
        axes = Axes(x_range=[-2.8, 2.8, 1], y_range=[-2.8, 2.8, 1],
                    x_length=7, y_length=7,
                    axis_config={"color":"#828A98", "stroke_width":2,
                                 "tick_size":.06, "tip_width":.12, "tip_height":.12})
        axes.move_to([0, 3.10, 0])
        self.add(axes, math("a", 32).next_to(axes.x_axis.get_end(), RIGHT, buff=.10),
                 math("b", 32).next_to(axes.y_axis.get_end(), UP, buff=.07))
        for v in [-2, -1, 1, 2]:
            self.add(math(str(v), 24, MUTED).next_to(axes.c2p(v, 0), DOWN, buff=.12),
                     math(str(v), 24, MUTED).next_to(axes.c2p(0, v), LEFT, buff=.12))
        self.add(DashedLine(axes.c2p(-2.65, 2.65), axes.c2p(2.65, -2.65),
                            color=RED, stroke_width=2.6, dash_length=.10))
        for domain in [[-2.65, -1/2.65, .01], [1/2.65, 2.65, .01]]:
            self.add(axes.plot(lambda a:1/a, x_range=domain, color=GREEN, stroke_width=5))
        for content, color, position in [("ab=1",GREEN,[1.85,1.06]),
                                         ("a=-b",RED,[-1.83,2.40])]:
            m=math(content,32,color).move_to(axes.c2p(*position))
            m.add_background_rectangle(color=BG,opacity=.95,buff=.06)
            self.add(m)
        self.add(Dot(axes.c2p(0,0), radius=.055, color=INK))
        legend=VGroup()
        for content,color in [("positive branch",BLUE),("negative branch",ORANGE),
                              (r"on $a=-b$",RED)]:
            legend.add(VGroup(Dot(radius=.045,color=color),tex(content,24,color)).arrange(RIGHT,buff=.10))
        legend.arrange(RIGHT,buff=.30).move_to([0,-.70,0])
        self.add(legend)
        progress=ValueTracker(0)
        time_label=math("t=",28,MUTED).move_to(axes.c2p(-2.28,-2.32))
        clock=DecimalNumber(0,num_decimal_places=1,font_size=28,color=MUTED)
        clock.next_to(time_label,RIGHT,buff=.08)
        clock.add_updater(lambda m:m.set_value(progress.get_value()*10))
        self.add(time_label,clock)
        _,runs=trajectories()
        for initial,values,color in runs:
            full=VMobject(color=color,stroke_width=3).set_points_as_corners([axes.c2p(*w) for w in values])
            full.set_stroke(opacity=.72)
            trail=full.copy().pointwise_become_partial(full,0,1e-6)
            trail.add_updater(lambda m,curve=full:m.pointwise_become_partial(curve,0,max(1e-6,progress.get_value())))
            head=Dot(axes.c2p(*initial),radius=.049,color=color)
            def move_head(m,data=values):
                f=progress.get_value()*(len(data)-1)
                k=min(int(f),len(data)-2)
                m.move_to(axes.c2p(*(data[k]*(1-f+k)+data[k+1]*(f-k))))
            head.add_updater(move_head)
            self.add(trail,head)

        self.add(tex("A two-layer, two-neuron linear network",29).move_to([0,-1.20,0]))
        nodes=[np.array([x,-2.00,0]) for x in [-2.8,0,2.8]]
        for p,value,caption in zip(nodes,["x","bx","abx"],["Input","Hidden unit","Output"]):
            self.add(Circle(radius=.38,color=INK,stroke_width=2.5,
                            fill_color=BG,fill_opacity=1).move_to(p),
                     math(value,32).move_to(p),tex(caption,26,MUTED).move_to(p+DOWN*.64))
        for i,(weight,color) in enumerate([("b",BLUE),("a",ORANGE)]):
            self.add(Arrow(nodes[i]+RIGHT*.42,nodes[i+1]-RIGHT*.42,buff=0,
                           color=color,stroke_width=3,tip_length=.12,
                           max_tip_length_to_length_ratio=.08),
                     math(weight,34,color).move_to((nodes[i]+nodes[i+1])/2+UP*.30))
        self.add(tex(r"Let's learn the identity map $y=x$.",30).move_to([0,-3.12,0]))
        loss=VGroup(tex("Then",30),math(r"L(a,b)=\frac12(ab-1)^2",36)).arrange(RIGHT,buff=.18)
        self.add(loss.move_to([0,-3.73,0]))
        self.add(math(r"\text{Symmetries}^{1}\;\Longrightarrow\;\text{conservation law}^{2}",33)
                 .move_to([0,-4.42,0]))

        # Reveal the algebra in three legible stages while training continues.
        symmetry=VGroup(math(r"(a,b)\mapsto\left(\lambda a,\frac b\lambda\right)",42).move_to([0,-5.35,0]),
                        math(r"\lambda>0",34,MUTED).move_to([0,-6.25,0]))
        differentiate=VGroup(
            math(r"\left.\frac{d}{d\lambda}L\!\left(\lambda a,\frac b\lambda\right)\right|_{\lambda=1}=0",36)
              .move_to([0,-5.25,0]),
            math(r"a\frac{\partial L}{\partial a}-b\frac{\partial L}{\partial b}=0",38)
              .move_to([0,-6.34,0]))
        conservation=VGroup(math(r"\frac{d}{dt}(a^2-b^2)=0",44,GOLD).move_to([0,-5.30,0]),
                           math(r"a(t)^2-b(t)^2=a_0^2-b_0^2",36,GOLD).move_to([0,-6.36,0]))
        self.add(tex(r"$^{1}$ Kunin et al. (2021)\qquad $^{2}$ Saxe et al. (2014)",24,MUTED)
                 .move_to([0,-7.43,0]))
        signal=Dot(nodes[0]+RIGHT*.42,radius=.07,color=BLUE)
        def move_signal(m):
            phase=(progress.get_value()*12)%2
            edge=0 if phase<1 else 1
            f=phase-edge
            m.move_to(interpolate(nodes[edge]+RIGHT*.42,nodes[edge+1]-RIGHT*.42,f))
            m.set_color(BLUE if edge==0 else ORANGE)
        signal.add_updater(move_signal)
        self.add(signal,symmetry)
        self.play(progress.animate.set_value(1/6),run_time=2,rate_func=linear)
        self.remove(symmetry)
        self.add(differentiate)
        self.play(progress.animate.set_value(1/3),run_time=2,rate_func=linear)
        self.remove(differentiate)
        self.add(conservation)
        self.play(progress.animate.set_value(.5),run_time=2,rate_func=linear)
        self.wait(1/config.frame_rate)
