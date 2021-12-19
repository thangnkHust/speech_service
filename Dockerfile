FROM --platform=arm64 continuumio/anaconda3

RUN apt-get update -qq \
    && apt-get install --no-install-recommends -y \
        graphviz \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN apt update && apt-get install libsndfile1 -y

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN conda update --all
RUN conda install tensorflow \
    && conda install pyaudio
# RUN conda install -c anaconda tensorflow

CMD ["python3", "app.py"]
