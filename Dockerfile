FROM --platform=linux/amd64 ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y git

RUN apt-get install -y wget curl unzip
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb 
    
# install python3.11
RUN apt-get update && apt-get install -y software-properties-common && add-apt-repository -y ppa:deadsnakes/ppa && apt-get update && apt install -y python3.11
RUN apt-get install -y python3-pip

# install python dependencies
RUN pip install --no-cache-dir \
    appdirs==1.4.4 \
    beautifulsoup4==4.12.3 \
    cssutils==2.11.1 \
    html5lib==1.1 \
    Requests==2.32.3 \
    rich==13.7.1 \
    selenium==4.22.0 \
    webdriver_manager==4.0.1

# stay alive
CMD ["tail", "-f", "/dev/null"]
