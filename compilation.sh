#!/bin/sh
# Concat into a compilation
ffmpeg \
-i ./videos/2017-01-25/wdpkp-2017-01-25.mp4 \
-i ./videos/2017-01-27/wdpkp-2017-01-27.mp4 \
-i ./videos/2017-01-28/wdpkp-2017-01-28.mp4 \
-i ./videos/2017-01-29/wdpkp-2017-01-29.mp4 \
-i ./videos/2017-01-30/wdpkp-2017-01-30.mp4 \
-i ./videos/2017-01-31/wdpkp-2017-01-31.mp4 \
-i ./videos/2017-02-01/wdpkp-2017-02-01.mp4 \
-i ./videos/2017-02-02/wdpkp-2017-02-02.mp4 \
-i ./videos/2017-02-03/wdpkp-2017-02-03.mp4 \
-i ./videos/2017-02-04/wdpkp-2017-02-04.mp4 \
-filter_complex "[0:v][1:v][2:v]concat=n=3:v=1[v2]" -map "[v2]" \
./videos/compilations/wdpkp-comp-2017-01-25_02-04.mp4