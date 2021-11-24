FROM balexander85/wrapped_driver:slim-buster
LABEL maintainer="Brian A <brian@dadgumsalsa.com>"
WORKDIR /usr/src
COPY tweet_capture ./
RUN apt-get update \
 && apt-get upgrade -y \
 # Install tools for building
 && toolDeps="git aptitude" \
 && apt-get install -y --no-install-recommends --no-install-suggests $toolDeps fonts-takao-mincho \
 # Install chromedriver and chromium with aptitude
 && aptitude install chromium-driver -y \
 # Activate Virtual Environment
 && . /wrapped-driver-env/bin/activate \
 && python -m pip install -r requirements.txt \
 # Cleanup unnecessary stuff
 && apt-get purge -y --auto-remove \
                  -o APT::AutoRemove::RecommendsImportant=false \
            $toolDeps \
 && rm -rf /var/lib/apt/lists/* \
           /tmp/*
