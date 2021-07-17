FROM ubuntu:20.04


ENV TZ=Asia/Shanghai
# set location
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list && apt-get update --fix-missing \
# RUN apt-get update \
    # Install packages
    && apt-get install -y dialog apt-utils iproute2 net-tools curl wget vim openssh-server git make cmake \
    && apt-get install -y python3 python3-pip libbz2-dev python3-tk tk-dev \
    # Clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*
    
RUN pip install -i https://pypi.douban.com/simple/ --upgrade pip \
    && pip install -i https://pypi.douban.com/simple/ websocket-client==0.59.0 \
    && pip install -i https://pypi.douban.com/simple/ kafka==1.3.5 kafka-python==2.0.2 docker==4.1.0 docker-compose==1.25.0 \
    && pip install -i https://pypi.douban.com/simple/ redis==3.5.3 kubernetes==17.17.0 requests==2.22.0 urllib3==1.25.8

ENV PYTHONPATH=/
ENV TERM=xterm-256color
COPY ./ /phystats
WORKDIR /phystats

ENTRYPOINT [ "/usr/bin/python3", "main.py" ]

CMD [ "--role=collector", "--kafka_host=localhost", "--kafka_port=9092" ]