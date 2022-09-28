from pptx import Presentation
from pptx.util import Inches
import logging

def save_presentation(img_to_keep):
    logging.info("Creating powerpoint...")
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    blank_slide_layout = prs.slide_layouts[6]

    left = top = 0
    for i in range(0, len(img_to_keep)):
        slide = prs.slides.add_slide(blank_slide_layout)
        slide.shapes.add_picture("Frames/image" + str(img_to_keep[i]) + ".jpg", left, top, height=prs.slide_height)
    
    prs.save('YouTubeSlides.pptx')
    logging.info("PowerPoint saved")