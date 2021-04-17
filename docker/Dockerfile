FROM espressif/idf:latest
LABEL author="Lucas orsi <lorsi@gmail.com>"

ARG USER_ID
ARG GROUP_ID

# Install dependencies.
RUN apt-get update && apt-get install -y time sed

#Install pymaketool.

RUN pip3 install git+https://github.com/ericsonj/pymaketool.git@develop#egg=pymaketool

RUN addgroup --gid $GROUP_ID user
RUN adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID user

USER user

# Example project
WORKDIR /app




