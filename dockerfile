FROM python:3.8-slim-buster
ARG GIT_USER_MAIL
ARG GIT_USER_NAME

WORKDIR /app
COPY requirements.txt requirements.txt

RUN apt-get -y update
RUN apt-get -y install git
# For cv2 
RUN apt-get install ffmpeg libsm6 libxext6  -y 

# Remove this later 
RUN git config --global user.email ${GIT_USER_MAIL} \
    && git config --global user.name ${GIT_USER_NAME}


RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir black