FROM python:3.10

WORKDIR /app

COPY . .
 
RUN pip3 install -r requirements.txt

EXPOSE 5001

CMD [ "flask", "run", "--host=0.0.0.0", "--port=5001" ] 