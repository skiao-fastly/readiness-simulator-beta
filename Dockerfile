# app/Dockerfile

FROM python:3.9-slim

EXPOSE 8505

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY * /app/
RUN pip3 install -r requirements.txt
RUN pip3 install --upgrade pip
RUN mkdir -p /app/.streamlit
RUN mv secrets.toml .streamlit
COPY vegeta /usr/bin/
RUN chmod +x /usr/bin/vegeta
ENTRYPOINT ["streamlit", "run", "simulation.py", "--server.port=8501", "--server.address=0.0.0.0"]
