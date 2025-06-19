FROM python:3.12.10

WORKDIR /usr/src/app

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

COPY ./restaurant ./restaurant

EXPOSE 8000

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]