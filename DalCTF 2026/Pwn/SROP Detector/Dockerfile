FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y gcc make socat patchelf && rm -rf /var/lib/apt/lists/*
WORKDIR /
COPY dist/slop_detector /
COPY flag.txt /
RUN useradd -m -s /bin/bash ctfuser && \
    chown ctfuser:ctfuser /slop_detector /flag.txt
EXPOSE 9999
CMD ["socat", "TCP-LISTEN:9999,reuseaddr,fork", \
     "EXEC:/slop_detector,stderr,user=ctfuser"]
