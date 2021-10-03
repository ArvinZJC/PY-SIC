'''
Description: a patch for Pillow to save transparent GIF images
Version: 1.0.2.20210924
Author: egocarib (https://github.com/egocarib)
Date: 2021-09-19 13:12:58
Last Editors: Arvin Zhao
LastEditTime: 2021-09-24 00:47:39
'''

# Origin: https://gist.github.com/egocarib/ea022799cca8a102d14c54a22c45efe0.
# This code adapted from https://github.com/python-pillow/Pillow/issues/4644 to resolve an issue described in https://github.com/python-pillow/Pillow/issues/4640.
# Some details have been adjusted to generally provide satisfying results for WeiboEmoji (https://github.com/ArvinZJC/WeiboEmoji). For example, `alpha_threshold`.
# There is a known issue with the Pillow library that messes up GIF transparency by replacing the transparent pixels with black pixels (among other issues) when the GIF is saved using PIL.Image.save(). This code works around the issue and allows us to properly generate transparent GIFs.

from collections import defaultdict
from itertools import chain
from pathlib import Path
from random import randrange
from typing import List, Tuple, Union

from PIL.Image import Image


ALPHA_THRESHOLD = 128
EXT_TARGET = 'GIF'


class TransparentAnimatedGifConverter:
    '''
    The class for defining a transparent animated GIF converter.
    '''

    __PALETTE_SLOTSET = set(range(256))

    def __init__(self, img_rgba: Image, alpha_threshold: int = ALPHA_THRESHOLD) -> None:
        '''
        The constructor of the class for defining a transparent animated GIF converter.

        Parameters
        ----------
        `img_rgba`: the initial image frame
        `alpha_threshold`: the threshold for the alpha channel
        '''
        
        self.__img_rgba = img_rgba
        self.__alpha_threshold = alpha_threshold

    def __process_pixels(self) -> None:
        '''
        Set the transparent pixels to the color 0.
        '''

        self.__transparent_pixels = set(
            idx for idx, alpha in enumerate(self.__img_rgba.getchannel(channel = 'A').getdata())
            if alpha <= self.__alpha_threshold)

    def __set_parsed_palette(self) -> None:
        '''
        Parse the RGB palette color tuples from the palette.
        '''

        palette = self.__img_p.getpalette()
        self.__img_p_used_palette_idxs = set(
            idx for pal_idx, idx in enumerate(self.__img_p_data)
            if pal_idx not in self.__transparent_pixels)
        self.__img_p_parsedpalette = dict((idx, tuple(palette[idx * 3:idx * 3 + 3])) for idx in self.__img_p_used_palette_idxs)

    def __get_similar_color_idx(self) -> int:
        '''
        Return a palette index with the closest similar color.

        Returns
        -------
        `idx`: a palette index with the closest similar color
        '''

        old_color = self.__img_p_parsedpalette[0]
        dict_distance = defaultdict(list)

        for idx in range(1, 256):
            color_item = self.__img_p_parsedpalette[idx]

            if color_item == old_color:
                return idx
            
            distance = sum((
                abs(old_color[0] - color_item[0]),  # Red.
                abs(old_color[1] - color_item[1]),  # Green.
                abs(old_color[2] - color_item[2])))  # Blue.
            dict_distance[distance].append(idx)

        return dict_distance[sorted(dict_distance)[0]][0]

    def __remap_palette_idx_zero(self) -> None:
        '''
        Since the first color is used in the palette, remap it.
        '''

        free_slots = self.__PALETTE_SLOTSET - self.__img_p_used_palette_idxs
        new_idx = free_slots.pop() if free_slots else self.__get_similar_color_idx()
        self.__img_p_used_palette_idxs.add(new_idx)
        self.__palette_replaces['idx_from'].append(0)
        self.__palette_replaces['idx_to'].append(new_idx)
        self.__img_p_parsedpalette[new_idx] = self.__img_p_parsedpalette[0]
        del(self.__img_p_parsedpalette[0])

    def __get_unused_color(self) -> tuple:
        '''
        Return a color for the palette that does not collide with any other already in the palette.

        Returns
        -------
        `new_color`: a color for the palette that does not collide with any other already in the palette
        '''

        used_colors = set(self.__img_p_parsedpalette.values())

        while True:
            new_color = (randrange(256), randrange(256), randrange(256))

            if new_color not in used_colors:
                return new_color

    def __process_palette(self) -> None:
        '''
        Adjust palette to have the zeroth color set as transparent. Basically, get another palette index for the zeroth color.
        '''

        self.__set_parsed_palette()

        if 0 in self.__img_p_used_palette_idxs:
            self.__remap_palette_idx_zero()

        self.__img_p_parsedpalette[0] = self.__get_unused_color()

    def __adjust_pixels(self) -> None:
        '''
        Convert the pixels into their new values.
        '''

        if self.__palette_replaces['idx_from']:
            trans_table = bytearray.maketrans(
                bytes(self.__palette_replaces['idx_from']),
                bytes(self.__palette_replaces['idx_to'])
            )
            self.__img_p_data = self.__img_p_data.translate(trans_table)

        for idx_pixel in self.__transparent_pixels:
            self.__img_p_data[idx_pixel] = 0

        self.__img_p.frombytes(data = bytes(self.__img_p_data))

    def __adjust_palette(self) -> None:
        '''
        Modify the palette in the new `Image`.
        '''

        unused_color = self.__get_unused_color()
        final_palette = chain.from_iterable(self.__img_p_parsedpalette.get(x, unused_color) for x in range(256))
        self.__img_p.putpalette(data = final_palette)

    def process(self) -> Image:
        '''
        Return the processed mode `P` `Image`.

        Returns
        -------
        `img_p`: the processed mode `P` `Image`
        '''

        self.__img_p = self.__img_rgba.convert(mode = 'P')
        self.__img_p_data = bytearray(self.__img_p.tobytes())
        self.__palette_replaces = dict(idx_from = list(), idx_to = list())
        self.__process_pixels()
        self.__process_palette()
        self.__adjust_pixels()
        self.__adjust_palette()
        self.__img_p.info['transparency'] = 0
        self.__img_p.info['background'] = 0
        return self.__img_p


def create_animated_gif(
    durations: Union[int, List[int]],
    images: List[Image],
    alpha_threshold: int = ALPHA_THRESHOLD) -> Tuple[Image, dict]:
    '''
    If the image is a GIF, create its thumbnail here.

    Parameters
    ----------
    `durations`: an int or `List[int]` that describes the animation durations for the frames of this GIF
    `images`: a list of PIL Image objects that compose the GIF frames
    `alpha_threshold`: the threshold for the alpha channel

    Returns
    -------
    `output_image`: the output image
    `save_kwargs`: the additional arguments for the file saving operation
    '''

    save_kwargs = dict()
    new_images: List[Image] = []

    for frame in images:
        thumbnail = frame.copy()  # Type: Image.
        thumbnail_rgba = thumbnail.convert(mode = 'RGBA')
        thumbnail_rgba.thumbnail(reducing_gap = 3.0, size = frame.size)
        converter = TransparentAnimatedGifConverter(alpha_threshold = alpha_threshold, img_rgba = thumbnail_rgba)
        thumbnail_p = converter.process()  # Type: Image.
        new_images.append(thumbnail_p)

    output_image = new_images[0]
    save_kwargs.update(
        append_images = new_images[1:],
        disposal = 2,  # Other disposals don't work.
        duration = durations,
        format = EXT_TARGET,
        loop = 0,
        optimize = False,
        save_all = True
    )
    return output_image, save_kwargs


def save_transparent_gif(
    durations: Union[int, List[int]],
    images: List[Image],
    save_file: Union[str, bytes, Path],
    alpha_threshold: int = ALPHA_THRESHOLD) -> None:
    '''
    Create a transparent GIF, adjusting to avoid transparency issues that are present in the PIL library.

    Note that this does NOT work for partial alpha. The partial alpha gets discarded and replaced by solid colors.

    Parameters
    ----------
    `durations`: an int or `List[int]` that describes the animation durations for the frames of this GIF
    `images`: a list of PIL Image objects that compose the GIF frames
    `save_file`: a filename (string), `pathlib.Path` object or file object (this parameter corresponds and is passed to the `PIL.Image.save()` method)
    `alpha_threshold`: the threshold for the alpha channel

    Raises
    ------
    `ValueError`: the path for saving a GIF image is invalid; ensure that the file extension is correct
    '''

    if isinstance(save_file, (str, Path)) and not str(save_file).upper().endswith(EXT_TARGET):
        raise ValueError('not a valid path for saving a GIF image.')

    root_frame, save_args = create_animated_gif(alpha_threshold = alpha_threshold, durations = durations, images = images)
    root_frame.save(fp = save_file, **save_args)