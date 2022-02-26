![banner.png](./banner.png)

# PY-SIC

![PyPI](https://img.shields.io/pypi/v/PY-SIC)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/PY-SIC)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/99f6ed42fe8544caab83f0f8a49d50e0)](https://www.codacy.com/gh/ArvinZJC/PY-SIC/dashboard?utm_source=github.com&utm_medium=referral&utm_content=ArvinZJC/PY-SIC&utm_campaign=Badge_Grade)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/ArvinZJC/PY-SIC)
![GitHub](https://img.shields.io/github/license/ArvinZJC/PY-SIC)

**English** | [简体中文](./README-zhCN.md)

PY-SIC stands for "a simple image converter for Python". It could be seen as a simple wrapper of the popular Python imaging library [Pillow](https://github.com/python-pillow/Pillow), but contains a patch for better GIF conversion quality, thanks to [the workaround](https://gist.github.com/egocarib/ea022799cca8a102d14c54a22c45efe0) provided by [@egocarib](https://github.com/egocarib). The idea of maintaining this repository comes from the process of refactoring the scripts in another repository of mine named [Weibo Emoji](https://github.com/ArvinZJC/WeiboEmoji). The primary purpose is automation, as I found it time-consuming to convert images and keep the original file structure manually. In summary, PY-SIC can mainly help you with:

- Conversion tasks with an image or multiple images for many popular image formats _(TODO: currently supports GIF and PNG in the alpha release)_
- Customisation including but not limited to controlling the alpha threshold for converting images to GIF ones, showing the progress bar, keeping the file structure of the input directory, and specifying the output directory.

Please note that the code is licensed under [the GPL-3.0 License](./LICENSE).

## ❗ ATTENTION

> May I have your attention pls? 🔥

1. By 17 October 2021, everything looks good with PyCharm 2021.2.2 + Python 3.10.0. You could definitely use Visual Studio Code, but you might need to adjust the importing behaviour in some scripts to make them run correctly.
2. PY-SIC should support Python 3.6+, and relies on the packages listed below. To build the package yourself, please refer to [the package requirements for this project](./requirements.txt).

   | Name   | Version  |
   | :----- | :------: |
   | Pillow | ≥ 8.4.0  |
   | tqdm   | ≥ 4.62.2 |

## 📜 Docs

_TODO: This part will have significant changes since PY-SIC is in its super alpha release._

### Installation

```sh
pip install py-sic  # Use pip3 if required.
```

### Sample Usage

```Python
from pysic.engine import SIC
from pysic.errors import EmptyInputError
from pysic.pillow_gif_patch import ALPHA_THRESHOLD

FAIL = "Fail:"
sic = SIC(
    has_pbar=True,  # A flag indicating whether to show the progress bar or not.
    input_path="your/path/to/input"  # The path to an input image or the directory for locating the input image(s).
)

try:
    sic.convert(
        alpha_threshold=ALPHA_THRESHOLD,  # The threshold for the alpha channel.
        has_init_output=False,  # A flag indicating if the output directory should be cleaned up first.
        has_input_structure=True,  # A flag indicating if the file structure of the input directory should be kept.
        output_dir="your/path/to/output"  # The output directory for the converted image(s).
        to_fmt=to_fmt  # The target image format for conversion.
    )
except EmptyInputError as empty_input:
    print(FAIL, empty_input)
except FileExistsError as file_exists:
    print(FAIL, file_exists)
except FileNotFoundError as input_not_found:
    print(FAIL, input_not_found)
except ValueError as value:
    print(FAIL, value)
```

Hope you would find it useful! 💖
