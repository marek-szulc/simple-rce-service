FROM python:3.9

WORKDIR /service

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# RUN sed -i 's/os\.popen(cmd)\.read()/"RCE Disabled"/' service.py # one of the ways to patch it

EXPOSE 5000

CMD ["python", "service.py"]
