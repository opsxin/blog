FROM debian:10

ARG DB_NAME
ARG DB_USER 
ARG DB_HOST
ARG DB_PASSWORD
ENV DB_NAME $DB_NAME
ENV DB_USER $DB_USER
ENV DB_HOST $DB_HOST
ENV DB_PASSWORD $DB_PASSWORD

WORKDIR /usr/local/

RUN sed -i -e "/security/s/^/#/" \
    -e "s/deb.debian.org/mirrors.aliyun.com/g" /etc/apt/sources.list
RUN apt update && apt install -y \
    git python3 python3-pip python3-dev \
    whois libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/opsxin/blog.git -b compose
RUN pip3 install -r blog/requirements.txt \
    -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN mv blog/blog/blog/local_settings-sample.py blog/blog/blog/local_settings.py
RUN sed -e "s/DB_NAME/${DB_NAME}/" \
    -e "s/DB_USER/${DB_USER}/" \
    -e "s/DB_PASSWORD/${DB_PASSWORD}/" \
    -e "s/DB_HOST/${DB_HOST}/" \
    -i blog/blog/blog/local_settings.py

EXPOSE 8000

CMD ["/usr/local/bin/uwsgi", "--ini", "/usr/local/blog/uwsgi.ini"]
