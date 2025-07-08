FROM debian:bookworm-slim
WORKDIR /app
COPY . /app
RUN apt-get -qq update && apt-get -qq install -y git wget ffmpeg wkhtmltopdf python3 python3-pip python3.11-venv \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv --copies /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip3 install --no-cache-dir -r requirements.txt
CMD ["python3", "-m", "app"]