import logging
import os
import shutil

from pytube import YouTube

from ytpresentation.presentation import save_presentation
from ytpresentation.slidedetector import detect_slides, video_to_frames

URL = "https://www.youtube.com/watch?v=RDZUdRSDOok"
EPSILON = 0.015
FRAMERATE = 1

if __name__=="__main__":

    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO)

    logging.info("Creating temp directories.")
    try:
        os.mkdir('Frames')
    except FileExistsError:
        logging.info("Directories already existing. Overwritting.")

    logging.info("Downloading video.")
    ytvideo = YouTube(URL)
    video = ytvideo.streams.get_highest_resolution().download(filename="videotoextract.mp4")
    logging.info("Video successfully downloaded.")

    frame_count = video_to_frames()

    slides_list, delete = detect_slides(EPSILON, frame_count)
    
    save_presentation(slides_list)

    logging.info("Cleaning directories...")
    shutil.rmtree('Frames')
    os.remove('videotoextract.mp4')
    logging.info("Done.")