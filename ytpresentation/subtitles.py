from re import sub
from pytube import YouTube
import xml.etree.ElementTree as ET

# /!\ need to check if english subtitles are available
def parse_xml(ytvideo):
    """Get xml captions given a yt video and parse it
    to get subtitles

    Args:
        ytvideo (pytube.Youtube): Pytube video
    Returns:
        list: List of tuple : (timestamp, text)
    """
    xml_data = ytvideo.captions["a.en"].xml_captions
    mytree = ET.fromstring(xml_data)

    parsed_xml_list = []
    for data in mytree[1]:
        timestamp = data.attrib["t"]
        text = ""
        for i in data:
            text += i.text
        parsed_xml_list.append((int(timestamp), text))

    return parsed_xml_list


def get_text(timestamp_list, ytvideo):
    """Get subtitles corresponding to slides

    Args:
        timestamp_list (list): list of timestamps corresponding to the slides
        ytvideo (pytube.Youtube): Pytube video

    Returns:
        list: List of subtitles
    """
    parsed_xml_list = parse_xml(ytvideo)

    subtitles_list = []
    current_idx = 0
    for ts in timestamp_list[1:]:
        text = ""
        max_ts = ts * 1000
        while parsed_xml_list[current_idx][0] < max_ts:
            if len(parsed_xml_list[current_idx][1]) > 0:
                text += parsed_xml_list[current_idx][1] + " "
            current_idx += 1
        subtitles_list.append(text.strip())
    # Add last frame
    text = " ".join(
        [i[1] for i in parsed_xml_list[current_idx:] if len(i[1]) > 1]
    ).strip()
    subtitles_list.append(text)
    return subtitles_list
