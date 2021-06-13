from mylib.ex import *
from mylib.imageutil import *

comp_image_position = RIGHT * 6.75
slice_size = 50


class ImageCompressionScene(MovingCameraScene):
    def construct(self):
        unscaled = original_image()
        orig_image = scale_image(unscaled).convert(mode='L')

        orig_size = round(unscaled.size[0] * unscaled.size[1] / 1000000, 2)
        orig = ImageMobject(orig_image)
        orig_text = Tex("Original image").next_to(orig, direction=DOWN)
        orig_size = Tex(f"{orig_size} MB").next_to(orig_text, direction=DOWN)
        orig_group = Group(orig, orig_text, orig_size)
        self.camera.frame.move_to(orig_group)
        self.play(FadeIn(orig_group))

        k_tracker = ValueTracker(1)
        comp_image = scale_image(construct_image(1))
        csize = round(compressed_size(unscaled.size, 1) / 1000000, 2)
        comp = ImageMobject(comp_image).move_to(comp_image_position)
        comp_text = MathTex("\\text{Compressed}, k = 1").next_to(comp, direction=DOWN)
        comp_size = Tex(f"{csize} MB").next_to(comp_text, direction=DOWN)
        comp_group = Group(comp, comp_text, comp_size)

        self.play(AnimationGroup(
            self.camera.frame.animate.move_to(Group(orig_group, comp_group)),
            FadeIn(comp_group),
        ))

        comp.add_updater(lambda d: update_image(d, k_tracker))
        comp_text.add_updater(lambda d: update_text(d, k_tracker, comp))
        comp_size.add_updater(lambda d: update_size(d, k_tracker, unscaled, comp_text))

        self.play(k_tracker.animate.set_value(10))
        self.wait()
        self.play(k_tracker.animate.set_value(20))
        self.wait()
        self.play(k_tracker.animate.set_value(50))
        self.wait()
        self.play(k_tracker.animate.set_value(100))
        self.wait()
        self.play(k_tracker.animate.set_value(500))
        self.wait()


def update_image(d, tracker):
    new_image = scale_image(construct_image(int(tracker.get_value())))
    d.become(ImageMobject(new_image).move_to(comp_image_position))


def update_text(d, tracker, comp):
    val = int(tracker.get_value())
    d.become(MathTex(f"\\text{{Compressed}}, k = {val}").next_to(comp, direction=DOWN))


def update_size(d, tracker, img, comp_text):
    val = int(tracker.get_value())
    size = round(compressed_size(img.size, val) / 1000000, 2)
    d.become(Tex(f"{size} MB").next_to(comp_text, direction=DOWN))


def compressed_size(size, k):
    return size[0] * k + k + size[1] * k
