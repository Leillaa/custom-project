FROM python:3.9-slim
WORKDIR /app
COPY /bot/requirements.txt .
RUN pip3 install -r /app/requirements.txt --no-cache-dir
CMD ["python3", "bot.py"]
