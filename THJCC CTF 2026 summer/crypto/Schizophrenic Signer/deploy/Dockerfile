FROM python:3.10-slim

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

RUN useradd -m ctf
WORKDIR /home/ctf

COPY server.py .
RUN chown -R root:root /home/ctf && chmod -R 555 /home/ctf

USER ctf
ENV PYTHONUNBUFFERED=1

CMD ["socat", "TCP-LISTEN:11451,reuseaddr,fork", "EXEC:'python server.py'"]
