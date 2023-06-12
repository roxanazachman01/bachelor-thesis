FROM python:3

WORKDIR /usr/src/app

COPY ./server/requirements.txt ./
RUN pip install --no-cache-dir -r ./server/requirements.txt

COPY . .

CMD [ "python", "./server/main.py" ]