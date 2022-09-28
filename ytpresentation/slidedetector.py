#!/usr/bin/env python
import os
import shutil
import cv2
from skimage import metrics
import logging
from pytube import YouTube

def similarity_score(img1, img2):
    """_summary_

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


def delete_image(index):
    """Remove an image given the index

    Args:
        index (_type_): index of the image to remove
    """
    filename = 'image' + index + ".jpg"
    file_path = os.path.join("Frames", filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

    """
    
    :param seconds: Second in the video to start cutting into frames
    :return: boolean
    """


def video_to_frames():
    logging.info("Cutting video to frames...")
    vid_cap = cv2.VideoCapture('videotoextract.mp4')
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
    img1 =  cv2.imread("Frames/image0.jpg")
    last_was_slide = False
    for idx in range(1, count-1):
        img2 = cv2.imread("Frames/image" + str(idx) + ".jpg")
        # Check if frames are similar 
        if similarity_score(img1, img2) > 1 - threshold:
            # Previous frame was not detected as a slide 
            if not last_was_slide:
                slides_list.append(idx-1)
                last_was_slide = True
            # Previous frame was detected as a slide, we don't want it cause it's the same
            else : 
                delete_list.append(idx)
        else : 
            delete_list.append(idx)
            last_was_slide = False
        img1 = img2
    logging.info(f"{len(slides_list)} slides detected")
    return (slides_list, delete_list)


def video_to_frame(seconds):
    """Cut the current video into frames and export frames in Frames dir

    Args:
        seconds (int): Second in the video to start cutting into frames

    Returns:
        boolean: ???????????????
    """
    global count
    vid_cap.set(cv2.CAP_PROP_POS_MSEC, seconds * 1000)
    has_frames, image = vid_cap.read()
    if has_frames:
        cv2.imwrite("Frames/image" + str(count) + ".jpg", image)  # save frame as JPG file
        if count > 1:
            if compare_img("image" + str(count - 1) + ".jpg", "image" + str(count) + ".jpg") > 1 - epsilon:
                delete_image(str(count))
                count = count - 1
                if count not in pdfImg:
                    if len(pdfImg) > 0:
                        bool = 0
                        for i in range(len(pdfImg)):
                            if (compare_img("image" + str(pdfImg[i]) + ".jpg",
                                            "image" + str(count) + ".jpg") > 1 - epsilon):
                                bool = 1
                        if bool == 0:
                            pdfImg.append(count)
                    elif len(pdfImg) == 0:
                        pdfImg.append(count)

    return has_frames

