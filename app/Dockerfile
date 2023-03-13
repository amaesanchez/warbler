FROM python:3.8
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install psycopg2==2.9.3
COPY . .
CMD [ "python3", "-m" , "flask", "run", "-p", "5000", "--host=0.0.0.0"]
