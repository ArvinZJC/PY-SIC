'''
Description: the simple image converter's engine
Version: 1.0.0.20211002
Author: Arvin Zhao
Date: 2021-09-19 23:17:09
Last Editors: Arvin Zhao
LastEditTime: 2021-10-02 15:52:22
'''

from pathlib import Path
from shutil import copy2
from tqdm import tqdm
import os

from PIL import Image

from pillow_gif_patch import ALPHA_THRESHOLD, save_transparent_gif


class SIC:
    '''
    The class for defining the simple image converter's engine.
    '''

    def __init__(self, input_path: str, has_pbar: bool = True, output_dir: str = None) -> None:
        '''
        The constructor of the class for defining the simple image converter's engine.

        Parameters
        ----------
        `input_path`: the path to an input image or the directory for locating the input image(s)
        `has_pbar`: a flag indicating whether to show the progress bar or not
        `output_dir`: the output directory for the converted image(s)
        '''

        self.__IMG_FMTS_VALID = ['gif', 'png']  # A list of the image formats supported by the engine.
        self.__OUTPUT_FOLDER = 'output_'  # Part of the default output folder name (output_<extension>).

        self.__has_pbar = has_pbar
        self.__input_path = input_path
        self.__output_dir = output_dir
        self.__pbar = None

    def __convert_img(self, input_path: str, output_dir: str, to_fmt: str, alpha_threshold: int = ALPHA_THRESHOLD) -> None:
        '''
        Convert an input image to an image of the specified format.
        
        It will copy the input image rather than convert it if the target image format is the same as that of the input image.

        Parameters
        ----------
        `input_path`: the path to an input image
        `output_dir`: the output directory for the converted image
        `to_fmt`: the target image format for conversion
        `alpha_threshold`: the threshold for the alpha channel

        Raises
        ------
        `ValueError`: the target image format for conversion is not supported; check the target format
        '''

        if to_fmt not in self.__IMG_FMTS_VALID:
            raise ValueError('not an image format supported by SIC.')

        f, ext = os.path.splitext(os.path.basename(input_path))  # The input image filename and the extension.
        ext = ext.lower()
        ext_target = '.' + to_fmt.lower()  # The target extension.

        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

        if ext == ext_target:
            copy2(input_path, output_dir)
        else:
            try:
                with Image.open(input_path) as im:
                    output_path = os.path.join(output_dir, f + ext_target)  # The output path to the converted image.

                    if to_fmt == '.gif':
                        save_transparent_gif(
                            alpha_threshold = alpha_threshold,
                            durations = 0,
                            images = [im],
                            save_file = output_path
                        )
                    else:
                        im.save(format = to_fmt, fp = output_path)
            except OSError:
                print('Failed to convert for', input_path)

    def __plan(self, input_path: str, count: int = 0) -> int:
        '''
        Count the number of conversion tasks.

        Parameters
        ----------
        `input_path`: the path to an input image or the directory for locating the input image(s)
        `count`: the initial number of conversion tasks

        Returns
        -------
        `task_count`: the number of conversion tasks
        '''

        if os.path.isfile(input_path):
            return 1
        
        with os.scandir(input_path) as entries:
            for entry in entries:
                count += self.__plan(input_path = entry.path, count = count)
        
        return count

    def convert(self, to_fmt: str, alpha_threshold: int = ALPHA_THRESHOLD, input_path: str = None, output_dir: str = None) -> None:
        '''
        Perform the image conversion tasks.

        Parameters
        ----------
        `to_fmt`: the target image format for conversion
        `alpha_threshold`: the threshold for the alpha channel
        `input_path`: the path to an input image or the directory for locating the input image(s)
        `output_dir`: the output directory for the converted image(s)

        Raises
        ------
        `OSError`: the path to an input image or the directory for locating the input image(s) does not exist; check the input path
        '''

        input_path = self.__input_path if input_path is None else input_path

        if self.__has_pbar and self.__pbar is None:
            self.__pbar = tqdm(total = self.__plan(input_path = input_path))

        if output_dir is None:
            if self.__output_dir is None:
                self.__output_dir = self.__OUTPUT_FOLDER + to_fmt.lower()
            
            output_dir = self.__output_dir

        if os.path.isfile(self.__input_path):
            self.__convert_img(
                alpha_threshold = alpha_threshold,
                input_path = self.__input_path,
                output_dir = self.__output_dir,
                to_fmt = to_fmt
            )

            if self.__has_pbar:
                self.__pbar.update()
        else:
            if os.path.isdir(self.__input_path):
                with os.scandir(self.__input_path) as entries:
                    for entry in entries:
                        self.convert(
                            alpha_threshold = alpha_threshold,
                            input_path = entry.path,
                            output_dir = os.path.join(output_dir, *Path(entry.path).parts[len(Path(input_path).parts):-1]),
                            to_fmt = to_fmt
                        )
            else:
                raise OSError('no such input path.')


def guide() -> None:
    '''
    A default guide for a console application to convert images using the engine.
    '''

    input_path = input('Enter the full path to an input image or the directory for locating the input image(s):\n').strip()
    to_fmt = input('\nEnter the target image format for conversion:\n').strip()

    # TODO: output? rmtree for path/dir?

    if to_fmt.lower() == 'gif':
        alpha_threshold = int(input('\nEnter the threshold for the alpha channel:\n'))  # TODO: fail to convert to int? more hints? default?

    with SIC(input_path = input_path) as sic:
        print('Start to convert. Please do not operate the input path/directory until the conversion process completes.')

        try:
            sic.convert(alpha_threshold = alpha_threshold, to_fmt = to_fmt)
        except OSError:
            print('Failed due to no such input path/directory.')
        except ValueError:
            print('Failed due to the unsupported target image format.')