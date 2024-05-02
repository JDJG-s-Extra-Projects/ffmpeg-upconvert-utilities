FROM debian:bookworm-slim AS base
WORKDIR /workspace

RUN ["apt", "update"]
RUN ["apt", "upgrade", "-y"]
RUN ["apt", "install", "-y", "ffmpeg"]
