from mylib.ex import *
from PIL import Image


class ImageToMatrix(MovingCameraScene):
    def construct(self):
        orig = np.array(Image.open("data/amongus.png").convert(mode='L'))
        shape = orig.shape
        scale = 60
        img = np.zeros((shape[0] * scale, shape[1] * scale))
        for y in range(img.shape[0]):
            for x in range(img.shape[1]):
                img[y][x] = orig[int(y / scale)][int(x / scale)]

        image = ImageMobject(img).scale(1.0)
        image_credit = Tex("Image by u/vytenis20").scale(0.4).next_to(image, direction=DOWN, buff=0.1, aligned_edge=RIGHT)

        self.play(FadeIn(Group(image, image_credit)))
        self.wait()

        height = image.height
        block_size = height / shape[0]
        pixel_values = []
        border_anims = []
        anims = []
        for y in range(shape[0]):
            for x in range(shape[1]):
                y_pos = y * block_size + image.get_bottom()
                x_pos = x * block_size + image.get_left()
                border = Square(side_length=block_size, stroke_width=0.1, stroke_color=BLACK)
                border.move_to(y_pos * DOWN + x_pos * RIGHT, UL)
                border_anims.append(FadeIn(border))

                rect = border.copy()
                rect.stroke_width = 0
                rect.set_fill(BLACK, 0.75)

                text = MathTex(f"{orig[y][x]}").scale(0.4)
                text.move_to(rect)
                pixel_value = Group(rect, text)
                pixel_values.append(pixel_value)
                anims.append(FadeIn(pixel_value))
        self.play(LaggedStart(*border_anims, lag_ratio=0.005))
        self.wait()
        self.play(LaggedStart(*anims, lag_ratio=0.005))
        self.wait()
