import cv2
from skimage import metrics
import logging


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
    score, _ = metrics.structural_similarity(gray_a, gray_b, full=True)
    return score


def get_slides(threshold):
    """Detect slides on the video
    Here it will not write all frames and load them to compare, everything is done on the fly.

    Args:
        threshold (float): Threshold to considere that two images are similar
    """
    logging.info("Extracting slides...")
    vid_cap = cv2.VideoCapture("videotoextract.mp4")

    sec = 1
    count = 0
    timestamp_list = []

    vid_cap.set(cv2.CAP_PROP_POS_MSEC, 0)
    has_frames, image1 = vid_cap.read()
    last_was_slide = False
    while has_frames:
        # Read image
        vid_cap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
        has_frames, image2 = vid_cap.read()
        # Is this image a new slide
        if has_frames:
            if similarity_score(image1, image2) > 1 - threshold:
                if not last_was_slide:
                    cv2.imwrite("Frames/image" + str(count) + ".jpg", image2)
                    count += 1
                    timestamp_list.append(sec - 1)
                    last_was_slide = True
            else:
                last_was_slide = False
                image1 = image2
        sec += 1
    cv2.destroyAllWindows()
    return count, timestamp_list
