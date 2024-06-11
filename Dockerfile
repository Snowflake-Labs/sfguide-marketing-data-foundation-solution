FROM python:3.8

ENV RELEASE True
WORKDIR /app
EXPOSE 8080
EXPOSE 443

COPY ./data_harmonization_nativeapp/streamlit  ./src/streamlit
COPY ./requirements.txt .

RUN pip install -r requirements.txt && \
    pip install -I git+https://github.com/wbond/oscrypto.git

RUN apt-get remove -y gcc python3-dev libssl-dev && \
    apt-get autoremove -y && \
    pip uninstall pipenv

ENTRYPOINT ["streamlit", "run", "./src/streamlit/home.py", "--server.port=8080", "--server.address=0.0.0.0"]
