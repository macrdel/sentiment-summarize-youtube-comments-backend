FROM python:3.10.5

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

COPY --chown=user . .

ENV PYTHONPATH=/home/user/app

# CMD ["sh", "-c", "service nginx start && uvicorn app.api:app --host 0.0.0.0 --port 8000"]