
FROM python:3
ENV PYTHONUNBUFFERED 1
WORKDIR /web/web
# Copy the requirements file first to leverage Docker cache

COPY requirements.txt /web/web/requirements.txt
RUN pip install -r requirements.txt
# Copy the rest of the application code
ENV PYTHONPATH=/web/web
ADD . /web/web
EXPOSE 8000
CMD ["gunicorn","--workers","4","--threads","4","--bind", "0.0.0.0:8000","--worker-class","gthread","--timeout", "60","web.wsgi:application"]
