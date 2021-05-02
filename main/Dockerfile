FROM joyzoursky/python-chromedriver:3.8-selenium
WORKDIR "/home"
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
