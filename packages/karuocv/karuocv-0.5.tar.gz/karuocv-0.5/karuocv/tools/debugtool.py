# _*_ encoding: utf-8 _*_
'''
@File    :debugtool.py
@Desc    :
@Time    :2024/10/20 22:19:22
@Author  :caimmy@hotmail.com
@Version :0.1
'''
import logging
from typing import Union
from math import ceil
import supervision as sv
import tqdm
import cv2
import imageio
import matplotlib.pyplot as plt
from karuocv.hub.inference import ImageAnnotator

logger = logging.getLogger(__file__)

def group_watch_images(matimg: dict, colsize: int=8):
    _imgsize = len(matimg)
    if _imgsize > colsize:
        rowsize = ceil(_imgsize / colsize)
    else:
        rowsize = 1
        colsize = _imgsize
    
    index = 1
    for _title in matimg:
        plt.subplot(rowsize, colsize, index)
        plt.imshow(matimg[_title])
        plt.title(_title)

        index += 1
    plt.show()


def vcd_inferenced_video(weight_file: str, source_video: str, output_video: str, recorder: str = "imageio", verbose: bool = False, imshow=False) -> Union[None | sv.VideoInfo]:
    """
    推理录像
    Args:
        weight_file str 模型文件
        source_video str 被推理视频文件
        output_video str 推理录像的保存地址
    """
    def _inference_frame(generator, total, annotator, box, labels):
        for frame in tqdm.tqdm(generator, total=total):
            yield annotator.fullAnnotateImage(frame, box, labels)


    ret_info = None
    try:
        annotator = ImageAnnotator(weight_file, verbose=verbose)
        video_info = sv.VideoInfo.from_video_path(source_video)
        frames_generator = sv.get_video_frames_generator(source_video)

        _box_annotator = sv.BoundingBoxAnnotator()
        _label_annotator = sv.LabelAnnotator()
        if recorder == "imageio":
            logger.debug("use imageio to record video.")
            _video_saver = imageio.get_writer(output_video, fps=video_info.fps)
            for annotated_frame in _inference_frame(frames_generator, video_info.total_frames, annotator, _box_annotator, _label_annotator):
                annotated_frame = annotator.fullAnnotateImage(annotated_frame, _box_annotator, _label_annotator)
                _video_saver.append_data(cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB))
                if imshow:
                    cv2.imshow("", annotated_frame)
                    cv2.waitKey(1)
            _video_saver.close()
            ret_info = video_info
        else:
            logger.debug("use videosink to record video.")
            with sv.VideoSink(target_path=output_video, video_info=video_info) as sink:
                for annotated_frame in _inference_frame(frames_generator, video_info.total_frames, annotator, _box_annotator, _label_annotator):
                    annotated_frame = annotator.fullAnnotateImage(annotated_frame, _box_annotator, _label_annotator)
                    sink.write_frame(frame=annotated_frame)
                    if imshow:
                        cv2.imshow("", annotated_frame)
                        cv2.waitKey(1)
                ret_info = video_info
    except Exception as e:
        logger.error(e)
    finally:
        if imshow:
            cv2.destroyAllWindows()
    return ret_info

def detect_image(weight_file: str, image_uri: str, output_file: str = None):
    ia = ImageAnnotator(weight_file)
    img = cv2.imread(image_uri)
    img_mat = ia.fullAnnotateImage(img)
    if output_file:
        cv2.imwrite(output_file, img_mat)
    else:
        cv2.imshow("detect_image", img_mat)