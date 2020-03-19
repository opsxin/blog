FROM python:3.7

WORKDIR /app

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

RUN pip install -U pip -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . /app/

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["uwsgi", "--ini", "/app/uwsgi.ini"]
