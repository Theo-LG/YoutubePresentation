#!/usr/bin/env python
import os
import shutil
import cv2
from skimage import metrics
import logging
from pytube import YouTube


def similarity_score(img1, img2):
    """Measure used to compare frames

    Args:
        img1 : Image to compare
        img2 : Image to compare

    Returns:
        float: Similarity score
    """
    gray_a = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray_b = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    (score, diff) = metrics.structural_similarity(gray_a, gray_b, full=True)
    return score


def get_slides(threshold):
    """Detect slides on the video
    Here it will not write all frames and load them to compare, everything is done on the fly.

    Args:
        threshold (float): Threshold to considere that two images are similar
    """
    logging.info("Going through the video...")
    vid_cap = cv2.VideoCapture("videotoextract.mp4")
    sec = 1
    count = 0
    vid_cap.set(cv2.CAP_PROP_POS_MSEC, 0)
    has_frames, image1 = vid_cap.read()
    image1 = None
    last_was_slide = False
    while has_frames:
        # Read image
        vid_cap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
        has_frames, image2 = vid_cap.read()
        sec += 1

        # Is this image a new slide
        if similarity_score(image1, image2) > 1 - threshold:
            if not last_was_slide:
                cv2.imwrite("Frames/image" + str(count) + ".jpg", image2)
                count += 1
                last_was_slide = True
        else:
            last_was_slide = False
            image1 = image2


def video_to_frames():
    """Cut video to frames and save them to Frame dir

    Returns:
        int: Number of frames saved
    """
    logging.info("Cutting video to frames...")
    vid_cap = cv2.VideoCapture("videotoextract.mp4")
    sec = 0
    count = 0
    has_frames = True
    while has_frames:
        vid_cap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
        has_frames, image = vid_cap.read()
        if has_frames:
            cv2.imwrite("Frames/image" + str(count) + ".jpg", image)
        sec += 1
        count += 1
    cv2.destroyAllWindows()
    logging.info("Frames created.")
    return count


def detect_slides(threshold, count):
    """Compare frames from the youtube video to detect slides
    If two successives frames are identical, we supposed it's a slide

    Args:
        threshold (float): Threshold to considere that two images are similar
        count (int): Number of frame to processs

    Returns:
        Tuple: Two list of indices : indices corresponding to slides.
        And indices corresponding to frames to delete
    """
    logging.info("Detecting Slides...")
    slides_list = []
    delete_list = []
    img1 = cv2.imread("Frames/image0.jpg")
    last_was_slide = False
    for idx in range(1, count - 1):
        img2 = cv2.imread("Frames/image" + str(idx) + ".jpg")
        # Check if frames are similar
        if similarity_score(img1, img2) > 1 - threshold:
            # Previous frame was not detected as a slide
            if not last_was_slide:
                slides_list.append(idx - 1)
                last_was_slide = True
            # Previous frame was detected as a slide, we don't want it cause it's the same
            else:
                delete_list.append(idx)
        else:
            delete_list.append(idx)
            last_was_slide = False
        img1 = img2
    logging.info(f"{len(slides_list)} slides detected")
    return (slides_list, delete_list)
