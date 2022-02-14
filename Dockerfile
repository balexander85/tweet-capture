FROM python:buster
ENV PYTHONPATH "${PYTHONPATH}:/app"
ARG build_dependencies="git aptitude"
ARG app_dependencies="fonts-takao-mincho fonts-deva-extra"
ARG virtualenv_name="tweetcapture-env"
LABEL maintainer="Brian A <brian@dadgumsalsa.com>"
WORKDIR /app
COPY tweetcapture/ \
     setup.py \
     requirements.txt \
     README.md \
     MANIFEST.in ./
RUN apt-get update \
 && apt-get upgrade -y \
 # Install tools for building
 && apt-get install -y --no-install-recommends --no-install-suggests $build_dependencies $app_dependencies \
 # Install chromedriver and chromium with aptitude
 && aptitude install chromium-driver -y \
 # Create python egg
 && python setup.py sdist bdist_wheel \
 # Create Virtual Environment
 && python -m venv /tweetcapture-env \
 # Activate Virtual Environment
 && . /$virtualenv_name/bin/activate \
 && /$virtualenv_name/bin/python -m pip install --upgrade pip \
 && /$virtualenv_name/bin/python -m pip install -e . \
 # Cleanup unnecessary stuff
 && apt-get purge -y --auto-remove \
                  -o APT::AutoRemove::RecommendsImportant=false \
            $build_dependencies \
 && rm -rf /var/lib/apt/lists/* \
           /tmp/*
