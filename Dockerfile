FROM python:3.9.1
WORKDIR /html
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT [ "python"]
CMD ["test.py"]

# FROM python:3.8.1
# WORKDIR /app
# RUN pip install --upgrade pip
# COPY . .
# RUN pip install -r requirements.txt
# CMD [ "python3", "main.py" ]