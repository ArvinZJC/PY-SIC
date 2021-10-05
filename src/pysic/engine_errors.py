'''
Description: user-defined exceptions for SIC
Version: 1.0.0.20211005
Author: Arvin Zhao
Date: 2021-10-05 16:59:04
Last Editors: Arvin Zhao
LastEditTime: 2021-10-05 18:42:24
'''

class EmptyInputError(Exception):
    '''
    The class for defining the user-defined exception indicating that the input directory contains no image for conversion.
    '''

    def __init__(self, message: str = 'image(s) for conversion not found') -> None:
        '''
        The constructor of the class for defining the user-defined exception indicating that the input directory contains no image for conversion.

        Parameters
        ----------
        `message`: the error message
        '''

        super().__init__(message)