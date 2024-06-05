## Base image:
FROM demartis/matlab-runtime:R2023a

LABEL name="trace4harmonization"
LABEL version="1.0"
LABEL authorization="This Dockerfile is intended to build a container image that will be publicly accessible in the CHAIMELEON images repository."


############## Things done by the root user ##############
USER root
# Installation of tools and requirements:
RUN apt-get -q update && apt-get install -y -q --no-install-recommends python3 python3-boto3 && apt-get clean && rm -rf /var/lib/apt/lists/*

# create the user (and group) "chaimeleon"
RUN groupadd -g 1000 chaimeleon && \
    useradd --create-home --shell /bin/bash --uid 1000 --gid 1000 chaimeleon 
# Default password "chaimeleon" for chaimeleon user. 
RUN echo "chaimeleon:chaimeleon" | chpasswd

############### Now change to normal user ################
USER chaimeleon:chaimeleon

# create the directories where some volumes will be mounted
RUN mkdir -p /home/chaimeleon/datasets && \
    mkdir -p /home/chaimeleon/persistent-home && \
    mkdir -p /home/chaimeleon/persistent-shared-folder
    
# Copy of the application files into the container:
COPY ./app /app

WORKDIR /home/chaimeleon
ENTRYPOINT ["python3", "/app/startup.py"]
