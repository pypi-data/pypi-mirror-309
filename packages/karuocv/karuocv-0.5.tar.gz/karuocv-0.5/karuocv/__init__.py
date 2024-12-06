# _*_ encoding: utf-8 _*_
'''
@文件    :__init__.py
@说明    :
@时间    :2024/10/15 14:53:15
@作者    :caimmy@hotmail.com
@版本    :0.1
'''

"""
@version 0.1 [2024-10-15] start project
@version 0.3 [2024-10-30] 加入标注统计截图功能 task=statistic-labels
@version 0.5 [2024-11-18] 优化录像功能，增加对imageio压缩的支持。
"""

__version__ = "0.5"

from karuocv.utils import (train)
from karuocv.hub.inference import ImageAnalyser
from karuocv.tools.debugtool import (vcd_inferenced_video, detect_image)

all = (
    __version__,
    train,
    ImageAnalyser,
    vcd_inferenced_video,
    detect_image
)