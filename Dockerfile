FROM python:3.9
ADD main.py .
RUN pip install yfinance
CMD ["python3", "main.py"] 