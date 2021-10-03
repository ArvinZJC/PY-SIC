'''
Description: an image converter for converting input images to GIF images
Version: 1.0.0.20210919
Author: Arvin Zhao
Date: 2021-09-19 13:10:44
Last Editors: Arvin Zhao
LastEditTime: 2021-09-20 10:50:23
'''

from pathlib import Path
from shutil import copy2, rmtree
import os

from PIL import Image
from tqdm import std, tqdm

from pillow_gif_patch import ALPHA_THRESHOLD, save_transparent_gif


DICT_EXCEPTION = {'h_buyao.webp': 0}  # A dictionary recording the special alpha threshold settings for the specified images.
OUTPUT_DIR = 'output'
OUTPUT_DEBUG_DIR = OUTPUT_DIR + '_debug'


def convert(
    input_dir: str,
    path: str,
    progress_bar: std.tqdm,
    output_dir: str = OUTPUT_DIR) -> None:
    '''
    Perform the conversion tasks.

    Parameters
    ----------
    `input_dir`: the initial directory entered by the user for finding the input images
    `path`: the path for locating the input images
    `progress_bar`: the console progress bar
    `output_dir`: the output directory; the folder named output under the same directory of the script, by default
    '''

    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_dir():
                convert(input_dir = input_dir, path = entry.path, progress_bar = progress_bar)
            else:
                to_gif(
                    alpha_threshold = DICT_EXCEPTION[entry.name] if entry.name in DICT_EXCEPTION.keys() else ALPHA_THRESHOLD,
                    output_dir = os.path.join(output_dir, *Path(entry.path).parts[len(Path(input_dir).parts):-1]),
                    path = entry.path  # Set the output directory to keep the directory structure.
                )
                to_gif(
                    alpha_threshold = DICT_EXCEPTION[entry.name] if entry.name in DICT_EXCEPTION.keys() else ALPHA_THRESHOLD,
                    output_dir = OUTPUT_DEBUG_DIR,
                    path = entry.path
                )  # Test purposes only for manually verifing the image count, quality, etc.

            progress_bar.update()


def plan(path: str, count: int = 0) -> int:
    '''
    Count the number of conversion tasks.

    Parameters
    ----------
    `path`: the path for locating the input images
    `count`: the initial number of conversion tasks

    Returns
    -------
    `task_count`: the number of conversion tasks
    '''

    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_dir():
                count = plan(path = entry.path, count = count + 1)
            else:
                count += 1
    
    return count


def to_gif(output_dir: str, path: str, alpha_threshold: int = 128) -> None:
    '''
    Convert an input image to a GIF image if necessary.

    Parameters
    ----------
    `output_dir`: the output directory
    `path`: the path to the input image
    `alpha_threshold`: the threshold for the alpha channel
    '''

    f, ext = os.path.splitext(os.path.basename(path))  # The input image filename and the extension.
    ext_target = '.gif'

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    if ext == ext_target:
        copy2(path, output_dir)
    else:
        try:
            with Image.open(path) as im:
                save_transparent_gif(
                    alpha_threshold = alpha_threshold,
                    durations = 0,
                    images = [im],
                    save_file = os.path.join(output_dir, f + ext_target)
                )
        except OSError:
            print('Failed to convert for', path)


if __name__ == '__main__':
    input_dir = input('Enter the full path to the directory containing input images (e.g., "D:\WeiboEmoji\Images" on Windows):\n').strip()

    if os.path.isdir(input_dir):
        print('Start to convert. Please do not operate the input directory until the conversion process completes.')

        if os.path.isdir(OUTPUT_DIR):
            rmtree(OUTPUT_DIR)  # Assume no read-only files.
        
        if os.path.isdir(OUTPUT_DEBUG_DIR):
            rmtree(OUTPUT_DEBUG_DIR)  # Assume no read-only files.
        
        with tqdm(total = plan(path = input_dir)) as progress_bar:
            convert(
                input_dir = input_dir,
                path = input_dir,
                progress_bar = progress_bar
            )
    else:
        print('No such directory.')