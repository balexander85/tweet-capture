FROM balexander85/tweet_capture:latest
ARG test_dependencies="pytest"
LABEL maintainer="Brian A <brian@dadgumsalsa.com>"
WORKDIR /usr/src
COPY . ./
RUN /wrapped-driver-env/bin/python -m pip install $test_dependencies
