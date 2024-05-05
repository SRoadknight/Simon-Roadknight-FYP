# Dockerfile
FROM python:3.12.1

WORKDIR /app/backend

COPY ../../backend/requirements.txt .
RUN pip install -r requirements.txt

RUN python -m nltk.downloader stopwords punkt wordnet averaged_perceptron_tagger

COPY ../../backend/src /backend/src


CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--reload"]
