'''
Description: the unit test of the simple image converter's engine
Version: 1.0.0.20211004
Author: Arvin Zhao
Date: 2021-09-26 23:57:52
Last Editors: Arvin Zhao
LastEditTime: 2021-10-04 22:22:04
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

    def __init__(self, method_name: str) -> None:
        '''
        The constructor of the class for defining the unit test of the simple image converter's engine.

        Parameters
        ----------
        `method_name`: the named test function for the base class's constructor.
        '''
        
        super().__init__(methodName = method_name)
        self.__sic = SIC(input_path = os.path.join('cases', 'img'))  # ATTENTION: you need to prepare your own test images to perform valid tests.

    def __convert(self, to_fmt: str) -> bool:
        '''
        Execute the image conversion function properly.

        Parameters
        ----------
        `to_fmt`: the target image format for conversion

        Returns
        -------
        `success`: a flag indicating if the conversion is valid
        '''

        print('Target format:', to_fmt)

        try:
            self.__sic.convert(to_fmt = to_fmt)
            return True  # TODO: real conversion check?
        except OSError:
            print('Failed due to empty input directory or no such input path/directory.')
        except ValueError:
            print('Failed due to the unsupported target image format.')
        
        return False

    def test_convert_to_gif(self) -> None:
        '''
        Test the image conversion function's ability to convert to GIF images.
        '''

        self.assertTrue(self.__convert('GIF'))

    def test_convert_to_png(self) -> None:
        '''
        Test the image conversion function's ability to convert to PNG images.
        '''

        self.assertTrue(self.__convert('PNG'))


if __name__ == '__main__':
    unittest.main()