from manimlib.imports import *


# pycharm有自动调整代码格式的快捷键，默认为Alt + Ctrl + L
def HSL(hue, saturation=1, lightness=0.5):
    return Color(hsl=(hue, saturation, lightness))


def annularsec():
    ann = VGroup()
    for i in range(3600):
        ann_pre_sec = AnnularSector(
            outer_radius=3.5,
            inner_radius=2.5,
            fill_opacity=1,
            start_angle=0+i*PI/1800,
            angle=PI/180+PI/180000,
            # Gradient direction
            stroke_width=0)
        ann_pre_sec.set_color(Color(hsl=(i/3600, 1, 0.5)))
        ann.add(ann_pre_sec)
    return ann



class colortracker(Scene):
    CONFIG = {
        "camera_config": {
            "background_color": average_color("#1f252A")
        },
    }
    def construct(self):
        # object
        ann_sec = AnnularSector(
            outer_radius=3,
            inner_radius=2.5,
            fill_opacity=1,
            start_angle=0,
            angle=PI / 3,
            # Gradient direction
            sheen_direction=RIGHT,
            stroke_width=0
        )

        y = annularsec()
        square = Square(fill_opacity=1).scale(0.6)
        color_tracker = ValueTracker(0)
        color_label = Integer(color_tracker.get_value(), unit="^\\circ")
        # 整数
        color_label.add_updater(lambda v: v.set_value(color_tracker.get_value()).next_to(square, UP))
        square.add_updater(lambda s: s.set_color(HSL(color_tracker.get_value() / 360)))

        circle1 = Circle(radius=3)
        color_tracker = ValueTracker(0)

        color_label = Integer(color_tracker.get_value(), unit="^\\circ")
        # 整数
        color_label.add_updater(lambda v: v.set_value(color_tracker.get_value()).next_to(square, UP))

        square.add_updater(lambda s: s.set_color(HSL(color_tracker.get_value() / 360)))

        #arrow = Arrow(LEFT, RIGHT)
        #arrow.add_updater(lambda a: a.put_start_and_end_on(ORIGIN, circle1.point_from_proportion(
         #   color_tracker.get_value() / 360)))
        # put_start_and_end_on 把直线的首尾放在 start, end 上 point_from_proportion(alpha)在整条路径上占比为alpha处的点
        dota = Dot().add_updater(lambda a: a.move_to(circle1.point_from_proportion(color_tracker.get_value() / 360)))
        self.add(y)
        self.wait()
        mobjects = VGroup(square, color_label, dota)
        self.play(
            *[FadeIn(mob) for mob in mobjects]
        )
        self.wait(1)
        self.play(
            color_tracker.set_value, 360,
            rate_func=linear,
            run_time=10,
        )
        self.wait(2)

    def get_hsl_set_colors(self, saturation=1, lightness=0.5):
        return [*[HSL(i / 360, saturation, lightness) for i in range(360)]]