import requests
import cv2
import numpy as np
import sys
from PIL import Image
import argparse
import secrets
import os
import glob
import subprocess
import shutil

DEFAULT_FRAME_RATE = 5
SUPPORTED_TYPES = ["gif", "avi", "mp4"]

URL = "https://thisanimedoesnotexist.ai/results/psi-{:}/seed{:}.png"


def randomHex(len: int):
    """Returns a random hex string at the given length."""
    byteArray = []
    for foo in range(len):
        byteArray.append(secrets.randbelow(255).to_bytes(1, "little"))
    return b"".join(byteArray).hex()


def getImage(creativity: float, seed: int):
    """Get a image with a given seed and a given creativity."""
    if creativity < 0.3 or creativity > 2.0:
        return
    creativity_str = str(round(creativity, 1))
    seed_str = str(seed).rjust(5, "0")
    img_url = URL.format(creativity_str, seed_str)
    url_response = requests.get(img_url)
    path_str = "test_" + seed_str + "_" + creativity_str + ".png"
    data = []
    for chunk in url_response:
        data.extend(chunk)
    img_array = np.array(bytearray(data), dtype=np.uint8)
    return cv2.imdecode(img_array, -1)


def getAllImages(seed: int):
    """Gets a list of images at all creativity levels."""
    all_img = []
    for num in range(3, 21):
        all_img.append(getImage(num / 10, seed))
    return all_img


def imageToAvi(imgs: list, fps: int, output: str):
    """Converds a list of cv2 images to an avi file."""
    frameSize = (512, 512)
    out = cv2.VideoWriter(
        output,
        cv2.VideoWriter_fourcc(*"DIVX"),
        fps,
        frameSize,
    )
    for img in imgs:
        out.write(img)


def imageToMp4(imgs: list, fps: int, output: str):
    """Converds a list of cv2 images to an avi file."""
    frameSize = (512, 512)
    out = cv2.VideoWriter(
        output,
        cv2.VideoWriter_fourcc(*"X264"),
        fps,
        frameSize,
    )
    for img in imgs:
        out.write(img)


def imageToGif(imgs: list, fps: int, output: str):
    """Converds a list of cv2 images to gif."""
    PIL_images = []
    for img in imgs:
        temp = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        PIL_images.append(Image.fromarray(temp))
    PIL_images[0].save(
        fp=output,
        format="GIF",
        append_images=PIL_images[1:],
        save_all=True,
        duration=1000 / fps,
        loop=0,
    )


def imageToPng(imgs: list, output: str):
    """Saves an image array to a folder with the gievn output namve"""
    for num, img in enumerate(imgs):
        cv2.imwrite(output + "/" + str(num).rjust(8, "0") + ".png", img)


def imageAddReversed(imgs: list):
    """Make a loop by adding a reverst set of images to the back of the input list."""
    temp = imgs.copy()
    temp.reverse()
    imgs_reversed = imgs.copy()
    imgs_reversed.extend(temp)
    return imgs_reversed


def handleArguments(args, parser: argparse.ArgumentParser):
    """Handles to set default arguments."""
    if args.random == False and ("Seed" not in dir(args) or args.Seed is None):
        parser.print_usage()
        print(
            "gififyThisAnimeDoesNotExist.py: error: the following arguments are required: seed"
        )
        exit(1)
    elif args.random == True:
        args.Seed = secrets.randbelow(100000)
    if not args.output is None:
        if args.fileType is None:
            outputSplit = args.output.split(".")
            if len(outputSplit) <= 1:
                args.output += ".gif"
                args.fileType = "gif"
            else:
                args.fileType = outputSplit[-1]
            if not args.fileType in SUPPORTED_TYPES:
                args.fileType = "gif"
        else:
            outputSplit = args.output.split(".")
            if len(outputSplit) <= 1:
                args.output += "." + args.fileType

    else:
        if args.fileType is None:
            args.fileType = "gif"
    if args.fileType == "gif":
        if args.output is None:
            seed_str = str(args.Seed).rjust(5, "0")
            args.output = "output_gif_" + seed_str + ".gif"
    elif args.fileType == "avi":
        if args.output is None:
            seed_str = str(args.Seed).rjust(5, "0")
            args.output = "output_video_" + seed_str + ".avi"
    elif args.fileType == "mp4":
        if args.output is None:
            seed_str = str(args.Seed).rjust(5, "0")
            args.output = "output_video_" + seed_str + ".mp4"


def interpolate(imgs: list, interpolate: int):
    """ Do interpolation of images """
    temp_folders = []
    if interpolate != 0:
        paths = glob.glob("cain-ncnn-vulkan*")
        if len(paths) < 1:
            print(
                "Please download cain-ncnn-vulkan from https://github.com/nihui/cain-ncnn-vulkan/releases/latest and place the cain-ncnn-vulkan-YYYYDDMM-OS folder in the same folder as this."
            )
            exit(1)
        temp_folders.append("__gifify_temp_" + randomHex(10))
        os.makedirs(temp_folders[0])
        imageToPng(imgs, temp_folders[0])
        for num in range(1, interpolate + 1):
            temp_folders.append("__gifify_temp_" + randomHex(10))
            os.makedirs(temp_folders[num])
            print(
                subprocess.check_output(
                    paths[0]
                    + "/cain-ncnn-vulkan -i "
                    + temp_folders[num - 1]
                    + " -o "
                    + temp_folders[num]
                ).decode("utf-8")
            )

        imgs = []
        for file in glob.glob(temp_folders[-1] + "/*.png"):
            imgs.append(cv2.imread(file))
    for folder in temp_folders:
        shutil.rmtree(folder)
    return imgs


def saveImagesOfType(imgs: list, *, fileType: str, fps: int, output: str):
    """Saves an array of cv2 images to video or gif, depending on the type."""

    if fileType == "gif":
        imageToGif(imgs, fps, output)
    elif fileType == "avi":
        imageToAvi(imgs, fps, output)
    elif fileType == "mp4":
        imageToAvi(imgs, fps, output)


if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(
        description="Downloads images from thisanimedoesnotexist.ai at all creativity levels and makes them to a gif  or video."
    )
    my_parser.add_argument(
        "Seed",
        metavar="seed",
        type=int,
        help="The seed from thisanimedoesnotexist.ai",
        choices=range(0, 100000),
        nargs="?",
    )

    my_parser.add_argument(
        "--output",
        "-o",
        action="store",
        metavar="output",
        type=str,
        help="The output file name. Default is output_gif_<seed>.gif",
    )

    my_parser.add_argument(
        "--type",
        "-t",
        action="store",
        metavar="type",
        type=str,
        dest="fileType",
        help="The output type. (gif, avi or mp4). Default is gif. If this is set the defualt output string is changed acordingly.",
        choices=SUPPORTED_TYPES,
    )

    my_parser.add_argument(
        "--reverse",
        "--loop",
        "-l",
        action="store_true",
        help="Adds the reverse version of the pictures to the en of the video/gif to make a perfect loop.",
    )

    my_parser.add_argument(
        "--fps",
        "-f",
        action="store",
        metavar="fps",
        type=int,
        default=8,
        help="Sets the fps to export with.",
    )

    my_parser.add_argument(
        "--random",
        "-r",
        action="store_true",
        help="Overwrites seed with a random seed. When this is set, seed is not needed.",
    )

    my_parser.add_argument(
        "--interpolate",
        "-i",
        action="store",
        type=int,
        default=0,
        help="Specifies the number of interpolations should run on the frame. Please note that this is exponential. A value of 3 e.g. means 8 times the frames. 0-3 is therefore recomended",
    )
    args = my_parser.parse_args()
    handleArguments(args, my_parser)
    all_imgs = getAllImages(args.Seed)
    if args.reverse:
        all_imgs = imageAddReversed(all_imgs)
    all_imgs = interpolate(all_imgs, args.interpolate)
    saveImagesOfType(
        all_imgs,
        fileType=args.fileType,
        fps=args.fps,
        output=args.output,
    )
