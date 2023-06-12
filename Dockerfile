FROM python:3.11

WORKDIR /usr/src/app

COPY server/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./server/main.py" ]