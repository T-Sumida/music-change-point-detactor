FROM python:3.7

RUN apt-get update -y
RUN apt-get install -y libsndfile1
RUN mkdir /work
RUN pip install chainer==7.2.0 \
    jupyterlab librosa matplotlib==3.1.3 \
    pandas==1.0.1 pyyaml==5.3 scipy==1.4.1 \
    seaborn==0.10.0 sounddevice==0.3.15 \
    tqdm==4.42.1 numba==0.48 changefinder

WORKDIR /work
CMD [ "jupyter", "lab", "--port", "8888", "--ip=0.0.0.0", "--allow-root" ]
