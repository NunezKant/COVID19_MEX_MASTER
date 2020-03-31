FROM ubuntu:bionic

RUN apt-get install -y tzdata

RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    curl unzip wget python3-tk

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONUNBUFFERED=1

ENV APP_HOME /usr/src/app
WORKDIR /$APP_HOME

COPY . $APP_HOME/
RUN pip3 install -r requirements.txt

CMD tail -f /dev/null
CMD streamlit run app.py --server.address 0.0.0.0
