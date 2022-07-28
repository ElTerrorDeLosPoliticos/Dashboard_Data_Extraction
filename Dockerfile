#Installing streamlit image
FROM tomerlevi/streamlit-docker:0.49.0

RUN apt-get update
RUN pip install --upgrade pip
ENV PYTHONUNBUFFERED True
WORKDIR /app
COPY . ./
RUN chmod -R 777 /app
RUN pip install -r /app/requirements.txt
CMD streamlit run --server.port 8080 --server.enableCORS false streamlit_app.py