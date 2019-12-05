From registry.opensource.zalan.do/stups/ubuntu:16.04.3-8
MAINTAINER "Ahmed.Elbakry@zalando.de"

# Install python tools and dev packages
RUN apt-get update \
    && apt-get install -q -y --no-install-recommends  python3-pip python3-setuptools python3-wheel gcc \
    && apt-get clean \ 
    && rm -rf /var/lib/apt/lists/*

# set python 3 as the default python version
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1 \
    && update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1
RUN pip3 install kubernetes

COPY /event-exporter.py /

ENTRYPOINT ["/event-exporter.py"]
