import subprocess
import os


def extract_resolution(input_file: str) -> tuple[int]:
    cmd = f"ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 {input_file}"
    output = subprocess.run(cmd, shell=True, capture_output=True)
    width, height = output.stdout.decode().split('x')
    return int(width), int(height)


def crop_video(input_file: str, output_file: str, x: int, y: int, w: int, h: int, width: int = 608, height: int = 608):
    cmd = f"ffmpeg -y -i {input_file} -filter:v \"crop={w}:{h}:{x}:{y},scale={width}:{height}\" {output_file}"
    subprocess.run(cmd, shell=True)


def scale_video(input_file: str, output_file: str, w: int, h: int):
    cmd = f"ffmpeg -y -i {input_file} -vf scale={w}:{h} {output_file}"
    subprocess.run(cmd, shell=True)


def blur_video(input_file: str, output_file: str, blur: int = 15):
    '''crops the center 9:16 portion of the video and blurs'''
    width, height = extract_resolution(input_file)
    h = height
    w = int(height * 9 / 16)
    x = (width - w) / 2
    y = 0
    # crop and blur in one command
    cmd = f"ffmpeg -y -i {input_file} -filter:v \"crop={w}:{h}:{x}:{y},boxblur={blur}:1\" {output_file}"
    subprocess.run(cmd, shell=True)


def create_mobile_video(background_file, content_file, facecam_file, output_file, blur_strength=15, watermark_file=None, fps=60):
    _, content_height = extract_resolution(content_file)
    background_width, background_height = extract_resolution(background_file)
    content_x = 0
    content_y = int((background_height - content_height) / 2)

    if facecam_file is not None:
        facecam_width, _ = extract_resolution(facecam_file)
        facecam_x = int((background_width - facecam_width) / 2)
        facecam_y = 0
        filter_complex = f'[0:v] boxblur={blur_strength}:1 [a]; [a][1:v] overlay={content_x}:{content_y} [b]; [b][2:v] overlay={facecam_x}:{facecam_y}'
        input_args = f'-i {background_file} -i {content_file} -i {facecam_file}'
    else:
        filter_complex = f'[0:v] boxblur={blur_strength}:1 [a]; [a][1:v] overlay={content_x}:{content_y}'
        input_args = f'-i {background_file} -i {content_file}'

    if watermark_file:
        watermark_command = f"[3:v] scale=500:100,colorchannelmixer=aa=0.5 [d]; [c][d] overlay=10:1720"
        filter_complex = f"{filter_complex};{watermark_command}"
        input_args += f' -i {watermark_file}'

    cmd = f"ffmpeg -y {input_args} -filter_complex '{filter_complex}' -r {fps} -c:v libx264 -pix_fmt yuv420p {output_file}"
    subprocess.run(cmd, shell=True)


if __name__ == "__main__":

    background_file = "./FinalResult/inputBackground.mp4"
    content_file = "./FinalResult/inputContent.mp4"
    facecam_file = "./FinalResult/inputFacecam.mp4"
    output_file = "./FinalResult/output.mp4"

    try:
        os.remove(output_file)
    except OSError:
        pass

    # create_mobile_video(background_file, content_file, facecam_file, output_file)
    create_blurred_mobile_video(background_file, content_file, output_file)

    print("Done!")

    # delete all the video files
