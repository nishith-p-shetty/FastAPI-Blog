FROM python:latest

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

CMD ["uvicorn", "blog.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
#CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]