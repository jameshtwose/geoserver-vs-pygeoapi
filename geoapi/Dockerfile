FROM python:3.10-slim
COPY ./requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . /usr/app
WORKDIR /usr/app
EXPOSE 8090

CMD ["python", "main.py"]
# CMD ["uvicorn", "api:app", "--port", "8090"]
# CMD ["fastapi", "run", "api:app", "--port", "8090"]