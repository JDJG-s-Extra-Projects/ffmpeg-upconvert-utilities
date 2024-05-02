FROM debian:bookworm-slim AS base
WORKDIR /workspace

RUN ["apt", "update"]
RUN ["apt", "upgrade", "-y"]
RUN apt install -y git build-essential yasm cmake libtool libc6 libc6-dev unzip wget libnuma1 libnuma-dev

FROM base AS ffnvcodec
RUN git clone https://git.videolan.org/git/ffmpeg/nv-codec-headers.git

FROM ffnvcodec AS ffnvcodec-install
WORKDIR /workspace/nv-codec-headers
RUN ["make", "install"]

FROM ffnvcodec-install AS ffmpeg
WORKDIR /workspace
RUN git clone https://git.ffmpeg.org/ffmpeg.git ffmpeg/

FROM ffmpeg AS ffmpeg-configure
WORKDIR /workspace/ffmpeg
RUN ./configure --enable-nonfree --enable-cuda-nvcc --enable-libnpp --extra-cflags=-I/usr/local/cuda/include --extra-ldflags=-L/usr/local/cuda/lib64 --disable-static --enable-shared

FROM ffmpeg-configure AS ffmpeg-compile
RUN make

FROM ffmpeg-compile AS ffmpeg-install
RUN make install
