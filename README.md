# YoutubePresentation
This project aims to create a powerpoint version of any course video available on YouTube. Subtitles (generated by YouTube are available on slides notes)

# Setup
## Install
You just have to install requirements.txt :
```
pip install -r requirements.txt 
```


OpenCV library can lead to some issues, this can be necessary : 
```
apt-get install ffmpeg libsm6 libxext6  -y 
```

Environment is also available with docker

## Run 
Just use the following command after setting up the environment 
```
python ytpresentation/main.py -u "youtube_video_url"
```

# How it works
It will download the youtube video and compare successives frames (1 frame per second) to detect powerpoint slides.
Thanks to Pytube, we can also get the video's subtitles so we can add them to each slide. 
