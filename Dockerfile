FROM python:3.6-alpine3.6

LABEL maintainer="hello@dotburo.org"

ENV FFMPEG_VERSION=3.0.2

WORKDIR /tmp/ffmpeg

RUN apk add --update \
  build-base \
  curl \
  nasm \
  tar \
  bzip2 \
  zlib-dev \
  openssl-dev \
  yasm-dev \
  x264-dev \
  freetype-dev \
  libass-dev && \
\
  DIR=$(mktemp -d) && cd ${DIR} && \
\
  curl -s http://ffmpeg.org/releases/ffmpeg-${FFMPEG_VERSION}.tar.gz | tar zxvf - -C . && \
  cd ffmpeg-${FFMPEG_VERSION} && \
  ./configure \
  --enable-version3 --enable-gpl --enable-nonfree --enable-small --enable-libx264 --enable-libass --enable-postproc --enable-libfreetype --enable-libfontconfig --disable-debug && \
  make && \
  make install && \
  make distclean && \
\
  rm -rf ${DIR} && \
\
  apk add openssh && \
\
  apk del build-base curl tar bzip2 x264 openssl nasm && rm -rf /var/cache/apk/*

RUN pip install --no-cache-dir oauth2 python-dotenv \
  && mkdir -p /root/wdpkp

WORKDIR /root/wdpkp

ADD . ./

RUN chmod 755 ./docker-entry.sh ./main.py ./check.py \
  && /usr/bin/crontab ./crontabs.txt \
  && mkdir ./.ssh

CMD ["./docker-entry.sh"]
