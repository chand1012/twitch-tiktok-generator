import os

from yt_dlp import YoutubeDL


def download(url, output_dir, output_format='best'):
    """
    Download a file from a given URL to the specified output directory.

    Args:
        url (str): The URL of the file to download.
        output_dir (str): The directory where the file will be saved.
        output_format (str): The output format (default is 'best').

    Returns:
        str: The full path of the newly downloaded file.
    """
    # Create options for youtube_dl
    ydl_opts = {
        'format': output_format,
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
    }

    # Initialize youtube_dl
    with YoutubeDL(ydl_opts) as ydl:
        # Download the video
        info_dict = ydl.extract_info(url, download=True)

        # Get the downloaded file's name
        file_name = ydl.prepare_filename(info_dict)

    return file_name
