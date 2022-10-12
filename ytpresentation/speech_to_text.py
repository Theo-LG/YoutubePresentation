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
    parsed_xml_list = parse_xml(ytvideo)

    subtitles_list = []
    current_idx = 0
    for ts in timestamp_list[1:10]:
        text = ""
        max_ts = ts * 1000
        while parsed_xml_list[current_idx][0] < max_ts:
            if len(parsed_xml_list[current_idx][1]) > 0:
                text += parsed_xml_list[current_idx][1] + " "
            current_idx += 1
        subtitles_list.append(text.strip())
    subtitles_list
    return subtitles_list
