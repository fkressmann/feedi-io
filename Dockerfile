FROM python:3.9-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY run.sh .
COPY src .
RUN chown -R 1001:0 /app && \
    chmod -R g=u /app && \
    chmod +x /app/run.sh
USER 1001
EXPOSE 8080
CMD ["./run.sh"]