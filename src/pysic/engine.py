'''
Description: the simple image converter's engine
Version: 1.0.0.20211005
Author: Arvin Zhao
Date: 2021-09-19 23:17:09
Last Editors: Arvin Zhao
LastEditTime: 2021-10-05 18:53:38
'''

from pathlib import Path
from shutil import copy2, rmtree
from tqdm import tqdm
import os

from PIL import Image

from engine_errors import EmptyInputError
from pillow_gif_patch import ALPHA_THRESHOLD, save_transparent_gif


class SIC:
    '''
    The class for defining the simple image converter's engine.
    '''

    def __init__(self, input_path: str, has_pbar: bool = True) -> None:
        '''
        The constructor of the class for defining the simple image converter's engine.

        Parameters
        ----------
        `input_path`: the path to an input image or the directory for locating the input image(s)
        `has_pbar`: a flag indicating whether to show the progress bar or not
        '''

        self.__IMG_FMTS_VALID = ['gif', 'png']  # A list of the image formats supported by the engine.
        self.__INPUT_NOT_FOUND = 'no such input path/directory: '
        self.__OUTPUT_FOLDER = 'output_'  # Part of the default output folder name (output_<extension>).

        self.__has_pbar = has_pbar
        self.__input_path = input_path

    def __init_pbar(self):
        '''
        Initialise the progress bar.
        '''

        if self.__has_pbar:
            self.__pbar = tqdm(total = self.__plan(input_path = self.__input_path))
        else:
            self.__pbar = None

    def __convert_img(
        self,
        input_path: str,
        output_dir: str,
        to_fmt: str,
        alpha_threshold: int = ALPHA_THRESHOLD) -> None:
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

        to_fmt = to_fmt.lower()

        if to_fmt not in self.__IMG_FMTS_VALID:
            raise ValueError(to_fmt + ' is not an image format supported by SIC')

        f, ext = os.path.splitext(os.path.basename(input_path))  # The input image filename and the extension.
        ext = ext.lower()
        ext_target = '.' + to_fmt  # The target extension.

        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

        if ext == ext_target:
            copy2(input_path, output_dir)
        else:
            try:
                with Image.open(input_path) as im:
                    output_path = os.path.join(output_dir, f + ext_target)  # The output path to the converted image.

                    if to_fmt == 'gif':
                        save_transparent_gif(
                            alpha_threshold = alpha_threshold,
                            durations = 0,
                            images = [im],
                            save_file = output_path
                        )
                    else:
                        im.save(format = to_fmt, fp = output_path)
            except OSError:
                print('Failed to convert for', input_path)  # TODO: may interrupt pbar

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

        Raises
        ------
        `FileNotFoundError`: the path to an input image or the directory for locating the input image(s) does not exist; check the input path
        '''

        if os.path.isfile(input_path):
            return 1
        
        if os.path.isdir(input_path):
            with os.scandir(input_path) as entries:
                for entry in entries:
                    count = (count if os.path.isfile(entry.path) else 0) + self.__plan(input_path = entry.path, count = count)  # Only count images for conversion.
            
            return count
        
        raise FileNotFoundError(self.__INPUT_NOT_FOUND + input_path)

    def __convert(
        self,
        to_fmt: str,
        alpha_threshold: int = ALPHA_THRESHOLD,
        has_init_pbar: bool = False,
        has_input_structure: bool = True,
        input_path: str = None,
        output_dir: str = '') -> None:
        '''
        Process the image conversion tasks.

        Parameters
        ----------
        `to_fmt`: the target image format for conversion
        `alpha_threshold`: the threshold for the alpha channel
        `has_init_pbar`: a flag indicating if the progress bar should be initialised
        `has_input_structure`: a flag indicating if the file structure of the input directory should be kept
        `input_path`: the path to an input image or the directory for locating the input image(s), useful for a part of the tasks
        `output_dir`: the output directory for the converted image(s), useful for a part of the tasks

        Raises
        ------
        `EmptyInputError`: the input directory contains no image for conversion; check the input path
        `FileNotFoundError`: the path to an input image or the directory for locating the input image(s) does not exist; check the input path
        `ValueError`: from the function `__convert_img`
        '''

        input_path = self.__input_path if input_path is None else input_path

        if has_init_pbar:
            self.__init_pbar()

        if os.path.isfile(input_path):
            self.__convert_img(
                alpha_threshold = alpha_threshold,
                input_path = input_path,
                output_dir = output_dir,
                to_fmt = to_fmt
            )

            if self.__has_pbar:
                self.__pbar.update()
        else:
            if os.path.isdir(input_path):
                with os.scandir(input_path) as entries:
                    count = 0

                    for entry in entries:
                        count += 1
                        self.__convert(
                            alpha_threshold = alpha_threshold,
                            input_path = entry.path,
                            output_dir = os.path.join(self.__output_dir, *Path(entry.path).parts[len(Path(self.__input_path).parts):-1]) if has_input_structure else self.__output_dir,
                            to_fmt = to_fmt
                        )
                    
                    if count == 0:
                        raise EmptyInputError        
            else:
                raise FileNotFoundError(self.__INPUT_NOT_FOUND + input_path)

    def convert(
        self,
        to_fmt: str,
        alpha_threshold: int = ALPHA_THRESHOLD,
        has_init_output: bool = False,
        has_input_structure: bool = True,
        output_dir: str = None) -> None:
        '''
        Perform the image conversion tasks requested by the user.

        Parameters
        ----------
        `to_fmt`: the target image format for conversion
        `alpha_threshold`: the threshold for the alpha channel
        `has_init_output`: a flag indicating if the output directory should be cleaned up first
        `has_input_structure`: a flag indicating if the file structure of the input directory should be kept
        `output_dir`: the output directory for the converted image(s)

        Returns
        -------
        `EmptyInputError`: from the function `__convert`
        `FileExistsError`: the output directory is not empty; check the output directory
        `FileNotFoundError`: from the function `__convert`
        `ValueError`: from the function `__convert`
        '''

        self.__output_dir = os.path.join(os.path.dirname(os.path.abspath(self.__input_path)), self.__OUTPUT_FOLDER + to_fmt.lower()) if output_dir is None else output_dir

        if os.path.isdir(self.__output_dir):
            if has_init_output:
                try:
                    rmtree(self.__output_dir)
                except Exception:
                    raise FileExistsError('you may need to empty the output directory manually')
            elif sum(1 for _ in os.scandir(self.__output_dir)) > 0:
                    raise FileExistsError('the output directory is not empty')

        self.__convert(
            alpha_threshold = alpha_threshold,
            output_dir = self.__output_dir,
            has_init_pbar = True,
            has_input_structure = has_input_structure,
            to_fmt = to_fmt
        )


# For simple tests only.
if __name__ == '__main__':
    FAIL = 'Fail:'

    sic = SIC(input_path = os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
        ),
        'tests',
        'cases',
        'img')
    )  # ATTENTION: you need to prepare your own test images to perform valid tests.
    to_fmt = 'Gif'

    try:
        sic.convert(has_init_output = True, to_fmt = to_fmt)
        # TODO: real conversion check?
    except EmptyInputError as empty_input:
        print(FAIL, empty_input)
    except FileExistsError as file_exists:
        print(FAIL, file_exists)
    except FileNotFoundError as input_not_found:
        print(FAIL, input_not_found)
    except ValueError as value:
        print(FAIL, value)