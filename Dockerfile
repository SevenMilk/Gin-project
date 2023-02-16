FROM python:3.10.2
COPY --chown=root:root "default.txt" /root/default.txt
RUN apt-get update &&\
    groupadd -g 3000 ericjiang && \
    useradd -l -u 3001 -g 3000 -m ericjiang && echo "ericjiang:ericjiang" | chpasswd && adduser ericjiang sudo &&\
    apt-get install -y --no-install-recommends tzdata &&\
    TZ=Asia/Taipei &&\
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime &&\
    echo $TZ > /etc/timezone &&\
    dpkg-reconfigure -f noninteractive tzdata &&\
    rm -rf /var/lib/apt/lists/* &&\
    pip install --no-cache-dir --ignore-installed -r /root/default.txt

USER 3001:3000
WORKDIR /home/ericjiang
COPY --chown=ericjiang:ericjiang "python" /home/ericjiang/python
COPY --chown=ericjiang:ericjiang "golang"  /home/ericjiang/golang
#docker build --force-rm --no-cache -t moonlight165/gin_project:0.0.1 .
