FROM python:3.9

WORKDIR /service

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLAG="CTF{super_secret_flag}"

CMD ["python", "service.py"]
