FROM balexander85/tweetcapture
ARG test_dependencies="chromium-driver git"
ARG virtualenv_name="tweetcapture-env"
LABEL maintainer="Brian A <brian@dadgumsalsa.com>"
WORKDIR /test-app
COPY config.py \
     pytest.ini \
     requirements.txt \
     test_tweet_capture.py ./
RUN apt-get update \
 && apt-get upgrade -y \
 # Install tools for building and testing
 && apt-get install -y --no-install-recommends --no-install-suggests $test_dependencies \
 # Create Virtual Environment
 && python -m venv /$virtualenv_name \
 # Activate Virtual Environment
 && . /$virtualenv_name/bin/activate \
 && /$virtualenv_name/bin/python -m pip install --upgrade pip \
 && /$virtualenv_name/bin/python -m pip install -r requirements.txt \
 # Cleanup unnecessary stuff
 && apt-get purge -y --auto-remove \
                  -o APT::AutoRemove::RecommendsImportant=false \
 && rm -rf /var/lib/apt/lists/* /tmp/*