FROM python:3.9-slim-buster
WORKDIR /project
COPY app/conf.d/app.conf /project/app/conf.d/app.conf
RUN mkdir -p /project/dataset/volume1 /project/dataset/volume2 /project/dataset/volume3
COPY requirements.txt .
COPY main.py main.py
COPY pip.conf pip.conf
ENV PIP_CONFIG_FILE pip.conf
RUN pip3 install --upgrade pip 
RUN python3 -m pip install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]

#docker build -t unicorn-server .