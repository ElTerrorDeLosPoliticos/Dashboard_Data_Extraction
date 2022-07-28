#Installing streamlit image
FROM python:3.8

ENV PYTHONUNBUFFERED True

RUN apt-get update
RUN systemctl restart postgresql
RUN pip install --upgrade pip

EXPOSE 8080

WORKDIR /app
COPY . ./

RUN pip install -r /app/requirements.txt

CMD streamlit run --server.port 8080 --server.enableCORS false streamlit_app.py