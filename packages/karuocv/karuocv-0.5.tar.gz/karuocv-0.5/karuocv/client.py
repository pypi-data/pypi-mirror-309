# _*_ encoding: utf-8 _*_
'''
@文件    :client.py
@说明    :
@时间    :2024/10/15 22:37:26
@作者    :caimmy@hotmail.com
@版本    :0.1
'''

import argparse
from karuocv.utils import logger

def init_command_args():
    parser = argparse.ArgumentParser(description="SACP object train tools")

    parser.add_argument("--task", required=True, help="指定任务 train, inference, mix_datasets, ETC")
    parser.add_argument("--base_model", type=str, help="底座模型的路径")
    parser.add_argument("--device", type=str, help="select one in the list which contains cpu, cuda and mps")
    parser.add_argument("--epochs", type=int, default=30, help="训练迭代周期")
    parser.add_argument("--iterations", type=int, default=10, help="The number of generations to run the evolution for.")
    parser.add_argument("--batch_size", type=int, default=8, help="the batch size of train.")
    parser.add_argument("--path", type=str, help="some path parameter.")
    parser.add_argument("--verbose", default=False, action="store_true", help="show log for inference or not")
    parser.add_argument("--format", default="", help="format parameter")

    parser.add_argument("--source_a", type=str)
    parser.add_argument("--source_b", type=str)
    parser.add_argument("--imshow", type=bool, default=False, action="store_true", help="是否通过cv2显示图片")
    parser.add_argument("--dest", default="", type=str, help="the output files destnation path.")

    args = parser.parse_args()
    return args

def client_command():
    command_line_args = init_command_args()
    print(command_line_args)
    if command_line_args.verbose:
        command_line_args.verbose = True
    match command_line_args.task:
        case "mixdatasets":
            from karuocv.hub.sample_handle import DatasetMixer
            mixer = DatasetMixer(command_line_args.source_a, command_line_args.source_b, command_line_args.dest)
            mixer.mixSamples()
        case "train":
            from karuocv.utils import train
            if command_line_args.path:
                train(command_line_args.path, command_line_args.base_model, command_line_args.epochs, command_line_args.batch_size, command_line_args.device, command_line_args.verbose)
        case "tune":
           from karuocv.utils import tune
           tune(command_line_args.path, command_line_args.base_model, command_line_args.epochs, command_line_args.iterations)
           print("tune completed")
        case "vcd":
            """推理录像"""
            from karuocv.tools.debugtool import vcd_inferenced_video
            video_infor = vcd_inferenced_video(
                command_line_args.base_model, 
                command_line_args.path, 
                command_line_args.dest, 
                command_line_args.format, 
                command_line_args.verbose,
                command_line_args.imshow
            )
            if video_infor:
                print(video_infor)
        case "detect_image":
            from karuocv.tools.debugtool import detect_image
            detect_image(command_line_args.base_model, command_line_args.path, command_line_args.dest)
            logger.info("ok")
        case "regression-annotation":
            """注解回测：生成新的图片，左图打印标注图像，右图打印推理图像"""
            from karuocv.tools.validatortool import RegressionAnnotationTool
            RegressionAnnotationTool(command_line_args.base_model, command_line_args.path, command_line_args.dest).walkCheckDataset()
        case "statistic-labels":
            """标签统计： 对标注框进行截图保存"""
            from karuocv.hub.sample_watch import SampleStatistics
            SampleStatistics(command_line_args.path, command_line_args.dest).CaptureLabels()
        case _:
            logger.info("no matched task command")


if __name__ == "__main__":
    client_command()