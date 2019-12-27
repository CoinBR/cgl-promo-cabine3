FROM python:3.8.1-buster
RUN apt-get update 

RUN apt-get install -y libfbclient2
ENV PATH=$PATH:/opt/firebird/bin:/usr/lib/x86_64-linux-gnu
RUN mkdir /opt/firebird/
RUN ln -s /usr/lib/x86_64-linux-gnu/libfbclient2.so /usr/lib/x86_64-linux-gnu/libfbclient.so && ln -s /usr/lib/x86_64-linux-gnu /opt/firebird/bin

WORKDIR /usr/src/app

COPY ./app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
