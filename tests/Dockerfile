FROM balexander85/tweetcapture
LABEL maintainer="Brian A <brian@dadgumsalsa.com>"
WORKDIR /usr/src
COPY config.py \
     pytest.ini \
     test_tweet_capture.py ./
RUN /wrapped-driver-env/bin/python -m pip install pytest