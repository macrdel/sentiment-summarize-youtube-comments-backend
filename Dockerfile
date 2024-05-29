FROM python:3.10.5

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN apt-get update && apt-get install -y nginx && apt-get clean && pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

COPY --chown=user . $HOME/app

CMD ["sh", "-c", "service nginx start && uvicorn app.api:app --host 0.0.0.0 --port 8000"]