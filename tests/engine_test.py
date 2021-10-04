'''
Description: the unit test of the simple image converter's engine
Version: 1.0.0.20211004
Author: Arvin Zhao
Date: 2021-09-26 23:57:52
Last Editors: Arvin Zhao
LastEditTime: 2021-10-04 17:58:41
'''

import os
import sys
import unittest
BASE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'src',
    'pysic'
)
sys.path.append(BASE_DIR)

from engine import SIC


class EngineTest(unittest.TestCase):
    '''
    The class for defining the unit test of the simple image converter's engine.
    '''

    def __convert(self, to_fmt: str) -> None:
        '''
        Execute the image conversion function properly.

        Parameters
        ----------
        `to_fmt`: the target image format for conversion
        '''

        # ATTENTION: you need to prepare your own test images to perform valid tests.
        sic = SIC(input_path = 'img')
        print('Target format:', to_fmt)

        try:
            sic.convert(to_fmt = to_fmt)
        except OSError:
            print('Failed due to empty input directory or no such input path/directory.')
        except ValueError:
            print('Failed due to the unsupported target image format.')

    def test_convert_to_gif(self) -> None:
        '''
        Test the image conversion function's ability to convert to GIF images.
        '''

        self.__convert('GIF')

    def test_convert_to_png(self) -> None:
        '''
        Test the image conversion function's ability to convert to PNG images.
        '''

        self.__convert('PNG')


if __name__ == '__main__':
    unittest.main()