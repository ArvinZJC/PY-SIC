![banner.png](./banner.png)

# PY-SIC

![PyPI](https://img.shields.io/pypi/v/PY-SIC)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/PY-SIC)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/99f6ed42fe8544caab83f0f8a49d50e0)](https://www.codacy.com/gh/ArvinZJC/PY-SIC/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ArvinZJC/PY-SIC&amp;utm_campaign=Badge_Grade)
![GitHub](https://img.shields.io/github/license/ArvinZJC/PY-SIC)

[English](./README.md) | **简体中文**

PY-SIC 是一个简易的 Python 图像转换器。它可以看作是对知名 Python 图形库 [Pillow](https://github.com/python-pillow/Pillow) 的包装，不过包含了一个小补丁以使转换得到的 GIF 图片的质量更好更可控。这还要感谢 [@egocarib](https://github.com/egocarib) 所提供的[变通之法](https://gist.github.com/egocarib/ea022799cca8a102d14c54a22c45efe0)。维护此仓库的想法来自对我的另一个仓库 [微博 Emoji](https://github.com/ArvinZJC/WeiboEmoji) 中的脚本进行重构时的新需求。其核心目的是为了增加自动化程度，从而减少转换图片并同时保留文件结构的人工成本。总而言之，PY-SIC 主要可以在以下方面有所作为：

- 单/多图片转换，支持许多主流图片格式 *(TODO：alpha 版本暂只支持 GIF 和 PNG)*
- 用户自定义，包括但不限于控制转换成 GIF 图片时的透明度、展示进度条、保留目录结构和指定输出路径

请注意此项目使用 [GPL-3.0 协议](./LICENSE)。

## ❗ 注意

> 敲黑板了！敲黑板了！🔥

1. 截至2021年10月17日，使用 PyCharm 2021.2.2 + Python 3.10.0 开发表现良好。您当然可以使用 Visual Studio Code，但是包引用的部分可能需要做相应的调整来保证功能正确执行。
2. PY-SIC 应支持 Python 3.6+，并依赖下面所列的包。关于自己构建 PY-SIC 包，请参考[项目包依赖](./requirements.txt)。

    | 名称 | 版本 |
    | :-- | :--: |
    | Pillow | ≥ 8.4.0 |
    | tqdm | ≥ 4.62.2 |

## 📜 文档

*TODO: 由于 PY-SIC 正处于起步阶段，此部分在将来会有很大改动。*

### 安装

```sh
pip install py-sic  # 必要时用 pip3。
```

### 参考用法

```Python
from pysic.engine import SIC
from pysic.errors import EmptyInputError
from pysic.pillow_gif_patch import ALPHA_THRESHOLD

FAIL = "Fail:"
sic = SIC(
    has_pbar=True,  # 是否展示进度条。
    input_path="your/path/to/input"  # 要转换的图片路径或所在目录。
)

try:
    sic.convert(
        alpha_threshold=ALPHA_THRESHOLD,  # 透明度。
        has_init_output=False,  # 是否在转换前清空输出路径。
        has_input_structure=True,  # 是否保留目录结构。
        output_dir="your/path/to/output"  # 输出路径。
        to_fmt=to_fmt  # 要转换的格式。
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

希望您觉得有帮助！💖
