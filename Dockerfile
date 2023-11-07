FROM demartis/matlab-runtime:R2023a

RUN apt-get -q update && apt-get install -y -q --no-install-recommends python3 python3-boto3 && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY ./app /app