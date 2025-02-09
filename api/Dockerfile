FROM python:3.9
WORKDIR /api
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python3", "app/main.py"]