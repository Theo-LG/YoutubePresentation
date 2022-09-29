import argparse
import logging
import os
import shutil

from pytube import YouTube

from ytpresentation.presentation import save_presentation
from ytpresentation.slidedetector import detect_slides, video_to_frames, get_slides


def get_parser():
    EPSILON = 0.015

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-u", "--url", help="Url of the youtube video", type=str, required=True
    )
    parser.add_argument(
        "-t",
        "--threshold",
        help="Threshold used by the similarity measure. "
        "Because of noise in video, similarity score can be < 1.0 for similar frames. "
        f"Default to {EPSILON}",
        type=float,
        default=EPSILON,
    )
    return parser


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO)
    logging.info("Creating temp directories.")
    try:
        os.mkdir("Frames")
    except FileExistsError:
        logging.info("Directories already existing. Overwritting.")

    logging.info("Downloading video.")
    ytvideo = YouTube(args.url)
    video = ytvideo.streams.get_highest_resolution().download(
        filename="videotoextract.mp4"
    )
    logging.info("Video successfully downloaded.")

    # frame_count = video_to_frames()

    # slides_list, delete = detect_slides(args.threshold, frame_count)
    get_slides(args.threshold)
    """
    save_presentation(slides_list)

    logging.info("Cleaning directories...")
    shutil.rmtree("Frames")
    os.remove("videotoextract.mp4")
    logging.info("Done.")
"""
