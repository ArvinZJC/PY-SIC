"""
Description: user-defined exceptions for SIC
Version: 1.0.0.20211009
Author: Arvin Zhao
Date: 2021-10-05 16:59:04
Last Editors: Arvin Zhao
LastEditTime: 2021-10-09 01:13:13
"""


class EmptyInputError(Exception):
    """The class for defining the user-defined exception indicating that the input directory contains no image for
    conversion."""

    def __init__(self, message: str = "image(s) for conversion not found") -> None:
        """The constructor of the class for defining the user-defined exception indicating that the input directory
        contains no image for conversion.

        Parameters
        ----------
        message : str, optional
            The error message (the default is "image(s) for conversion not found").
        """
        super().__init__(message)
