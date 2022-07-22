import subprocess
import os

def create_mobile_video(background_file, content_file, facecam_file, output_file, blur_strength=15, watermark=True):

    content_x = 0
    content_y = 420
    facecam_x = 260
    facecam_y = 0

    if watermark:
        # put the watermark in the bottom left corner
        watermark_command = f"[3:v] scale=500:100,colorchannelmixer=aa=0.5 [d]; [c][d] overlay=10:1720"
        watermark_file = 'https://i.imgur.com/fGTUZ13.png' # this can be any public URL

        cmd = f"ffmpeg -i {background_file} -i {content_file} -i {facecam_file} -i {watermark_file} -filter_complex '[0:v] boxblur={blur_strength}:1 [a]; [a][1:v] overlay={content_x}:{content_y} [b]; [b][2:v] overlay={facecam_x}:{facecam_y} [c];{watermark_command}' -r 60 -c:v libx264 -pix_fmt yuv420p {output_file}"
    else:
        cmd = f"ffmpeg -i {background_file} -i {content_file} -i {facecam_file} -filter_complex '[0:v] boxblur={blur_strength}:1 [a]; [a][1:v] overlay={content_x}:{content_y} [b]; [b][2:v] overlay={facecam_x}:{facecam_y}' -r 60 -c:v libx264 -pix_fmt yuv420p {output_file}"


    subprocess.run(cmd, shell=True)


def create_blurred_mobile_video(background_file, content_file, output_file, blur_strength = 15, watermark=True):
    
    # the x and y coordinates will change when we 
    # start working with different aspect ratios

    content_x = 0
    content_y = 420

    if watermark:
        # put the watermark in the bottom left corner
        watermark_command = f"[2:v] scale=500:100,colorchannelmixer=aa=0.5 [c]; [b][c] overlay=10:1720"
        watermark_file = 'https://i.imgur.com/fGTUZ13.png' # this can be any public URL

        cmd = f"ffmpeg -i {background_file} -i {content_file} -i {watermark_file} -filter_complex '[0:v] boxblur={blur_strength}:1 [a]; [a][1:v] overlay={content_x}:{content_y} [b];{watermark_command}' -r 60 -c:v libx264 -pix_fmt yuv420p {output_file}"
    else:
        cmd = f"ffmpeg -i {background_file} -i {content_file} -filter_complex '[0:v] boxblur={blur_strength}:1 [a]; [a][1:v] overlay={content_x}:{content_y}' -r 60 -c:v libx264 -pix_fmt yuv420p {output_file}"

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
