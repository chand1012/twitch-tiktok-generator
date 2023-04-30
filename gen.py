import os

import fire
from facial_detection import facial_detection, draw_box
from render import crop_video, extract_resolution, blur_video, create_mobile_video


class TikTokGenerator:
    def detect(self, path: str, fps: int = 1, box: bool = False):
        x, y, x2, y2 = facial_detection(path, fps)
        print(f"Top Left: {x} {y}")
        print(f"Bottom Right: {x2} {y2}")
        if box:
            for image_path in os.listdir('thumbs'):
                draw_box(f'thumbs/{image_path}', x, y, x2, y2)

    def crop_face(self, path: str, fps: int = 1):
        x, y, x2, y2 = facial_detection(path, fps)
        w = x2 - x
        h = y2 - y
        crop_video(path, 'output.mp4', x, y, w, h)

    def crop_box(self, path: str):
        width, height = extract_resolution(path)
        # get the center 1:1 box of the video
        x = (width - height) / 2
        y = 0
        w = height
        h = height
        crop_video(path, 'output.mp4', x, y, w, h)

    def blur(self, path: str, blur: int = 15):
        blur_video(path, 'output.mp4', blur)

    def generate(self, path: str, output: str = 'output', fd_fps: int = 1, blur: int = 20, width=720, height=1280, no_facecam: bool = False, fps: int = 60, x_offset: int = 0, y_offset: int = 0):
        if height % 2 != 0:
            height -= 1
        if width % 2 != 0:
            width -= 1
        background = f'{output}_background.mp4'
        box = f'{output}_box.mp4'
        facecam = None
        if not no_facecam:
            facecam = f'{output}_face.mp4'
            # get facecam
            x, y, x2, y2 = facial_detection(path, fd_fps)
            w = x2 - x
            h = y2 - y
            output_h = int(height * 0.21875)
            output_w = int(output_h * w / h)
            if output_w % 2 != 0:
                output_w -= 1
            crop_video(path, facecam, x, y, w, h, output_w, output_h)
        # get background
        bg_width, bg_height = extract_resolution(path)
        h = bg_height
        w = int(bg_height * 0.5625)  # 9/16 in decimal
        x = (bg_width - w) / 2
        y = 0
        crop_video(path, background, x, y, w, h, width, height)
        # get the center 1:1 content of the video
        x = (bg_width - bg_height) / 2 + x_offset
        y = 0 + y_offset
        w = bg_height
        h = bg_height
        crop_video(path, box, x, y, w, h, width, width)
        create_mobile_video(background, box, facecam,
                            f'{output}.mp4', blur_strength=blur, fps=fps)
        if not no_facecam:
            os.remove(facecam)
        os.remove(background)
        os.remove(box)

    def blur_box(self, path: str, output: str = 'output', blur: int = 20, width=720, height=1280, fps: int = 60):
        '''Takes a square video, blurs it, makes it 9:16, then add the original video on top of it'''
        if height % 2 != 0:
            height -= 1
        if width % 2 != 0:
            width -= 1
        background = f'{output}_background.mp4'
        # get background
        bg_width, bg_height = extract_resolution(path)
        h = bg_height
        w = int(bg_height * 0.5625)  # 9/16 in decimal
        x = (bg_width - w) / 2
        y = 0
        if not os.path.exists(background):
            crop_video(path, background, x, y, w, h, width, height)
        # no need to get the center 1:1 content of the video
        # since its already a square
        create_mobile_video(background, path, None,
                            f'{output}.mp4', blur_strength=blur, fps=fps)
        os.remove(background)

    def extract(self, input_file: str):
        '''Extracts the center 9:16 portion of the video'''
        width, height = extract_resolution(input_file)
        print(f"Resolution: {width}x{height}")


if __name__ == '__main__':
    fire.Fire(TikTokGenerator)
