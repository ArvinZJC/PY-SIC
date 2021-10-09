"""
Description: the unit test of the simple image converter's engine
Version: 1.0.0.20211008
Author: Arvin Zhao
Date: 2021-09-26 23:57:52
Last Editors: Arvin Zhao
LastEditTime: 2021-10-08 10:42:47
"""

import os
import sys
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from src.pysic.engine import SIC
from src.pysic.engine_errors import EmptyInputError


class EngineTest(unittest.TestCase):
    """The class for defining the unit test of the simple image converter's engine."""

    def __init__(self, method_name: str) -> None:
        """The constructor of the class for defining the unit test of the simple image converter's engine.

        Parameters
        ----------
        method_name : str
            The named test function for the base class's constructor.
        """
        super().__init__(methodName=method_name)
        self.__FAIL = "Fail:"
        self.__sic = SIC(
            input_path=os.path.join("cases", "img")
        )  # ATTENTION: you need to prepare your own test images to perform valid tests.

    def __convert(self, to_fmt: str) -> bool:
        """Execute the image conversion function properly.

        Parameters
        ----------
        to_fmt : str
            The target image format for conversion.

        Returns
        -------
        bool
            A flag indicating if the conversion is valid.
        """
        print("Target format:", to_fmt)

        try:
            self.__sic.convert(has_init_output=True, to_fmt=to_fmt)
            return True  # TODO: real conversion check?
        except EmptyInputError as empty_input:
            print(self.__FAIL, empty_input)
        except FileExistsError as file_exists:
            print(self.__FAIL, file_exists)
        except FileNotFoundError as input_not_found:
            print(self.__FAIL, input_not_found)
        except ValueError as value:
            print(self.__FAIL, value)

        return False

    def test_convert_to_gif(self) -> None:
        """Test the image conversion function's ability to convert to GIF images."""
        self.assertTrue(self.__convert("GIF"))

    def test_convert_to_png(self) -> None:
        """Test the image conversion function's ability to convert to PNG images."""
        self.assertTrue(self.__convert("PNG"))


if __name__ == "__main__":
    unittest.main()
