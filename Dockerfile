FROM python:3.8

COPY . /app
WORKDIR /app
RUN pip3 install --no-cache-dir -r requirements.txt
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
