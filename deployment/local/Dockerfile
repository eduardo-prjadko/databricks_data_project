ARG IMAGE
ARG TAG

FROM $IMAGE:$TAG

ARG BUILD_PATH
ARG USER_NAME
ARG USER_ID

# create container user
USER root
RUN adduser --shell /bin/bash --uid ${USER_ID} --disabled-login ${USER_NAME}

# update apt-get and install basic apps
RUN apt-get update; \
    apt-get install --no-install-recommends -y wget git unzip openssh-client curl less gnupg ca-certificates lsb-release
RUN pip install --upgrade pip

WORKDIR /tmp

# install python requirements
COPY ${BUILD_PATH}/requirements.txt ./pip/${BUILD_PATH}/requirements.txt
RUN pip install -r ./pip/${BUILD_PATH}/requirements.txt

# install terraform
RUN wget -O - https://apt.releases.hashicorp.com/gpg | gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(grep -oP '(?<=UBUNTU_CODENAME=).*' /etc/os-release || lsb_release -cs) main" | tee /etc/apt/sources.list.d/hashicorp.list
RUN apt update && apt install terraform

# install azure cli
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash

USER ${USER_NAME}

CMD ["sleep", "infinity"]