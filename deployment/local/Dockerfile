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
    apt-get install --no-install-recommends -y \
        wget \
        git \
        unzip \
        openssh-client \
        curl \
        less \
        gnupg \
        ca-certificates \
        lsb-release \
        make \
        libicu67
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

# install azure functions core tool
RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
RUN mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg
RUN sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/debian/$(lsb_release -rs 2>/dev/null | cut -d'.' -f 1)/prod $(lsb_release -cs 2>/dev/null) main" > /etc/apt/sources.list.d/dotnetdev.list'
RUN apt update && apt install azure-functions-core-tools-4

USER ${USER_NAME}

CMD ["sleep", "infinity"]