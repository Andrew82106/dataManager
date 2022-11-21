FROM python:3.8
WORKDIR /Project/dataManager

COPY requirements.txt ./
RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

CMD ["mkdir", "localSources"]
CMD ["gunicorn", "app:app", "-c", "./gunicorn.conf.py"]