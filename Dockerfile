#Installing streamlit image
FROM python:3.8

ENV PYTHONUNBUFFERED True

RUN apt-get update
RUN apt-get install postgresql -y
RUN chmod 700 -R /var/lib/postgresql/10/main
RUN -i -u postgres
RUN /usr/lib/postgresql/10/bin/pg_ctl restart -D /var/lib/postgresql/10/main
RUN pip install --upgrade pip

EXPOSE 8080

WORKDIR /app
COPY . ./

RUN pip install -r /app/requirements.txt

CMD streamlit run --server.port 8080 --server.enableCORS false streamlit_app.py