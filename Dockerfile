FROM python:3.11
WORKDIR /code
COPY . /code/
RUN pip install -r requirements.txt
ENV PYTHONPATH /code
CMD [ "python", "-m", "unittest", "/code/tests/test_solution.py" ]
CMD [ "python", "/code/main.py" ]