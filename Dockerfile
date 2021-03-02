
FROM python:3.8

LABEL maintainer="precredito"

# Arguments that can be set with docker build
ARG AIRFLOW_VERSION=1.10.12

ARG AIRFLOW_HOME=/usr/local/airflow



# Export the environment variable AIRFLOW_HOME where airflow will be installed
ENV AIRFLOW_HOME=${AIRFLOW_HOME}


# Install dependencies and tools
RUN apt-get update -yqq && \
    apt-get upgrade -yqq && \
    apt-get install -yqq --no-install-recommends \
    build-essential \ 
    wget \
    libczmq-dev \
    curl \
    libssl-dev \
    git \
    inetutils-telnet \
    bind9utils freetds-dev \
    libkrb5-dev \
    libsasl2-dev \
    libffi-dev libpq-dev \
    freetds-bin build-essential \
    default-libmysqlclient-dev \
    apt-utils \
    rsync \
    zip \
    unzip \
    gcc \
    vim \
    locales \
    unixodbc-dev \
    unixodbc \
    python3-rpy2 \
    && apt-get clean

RUN apt-get update -y

RUN apt-get install -y python3-mysqldb

RUN pip3 install mysql-connector-python

RUN pip install psutil==5.7.3
RUN pip install python-dev-tools==2020.9.10


## Driver odbc 
RUN apt-get update \
 && apt-get install unixodbc -y \
 && apt-get install unixodbc-dev -y \
 && apt-get install unixodbc-bin -y \
 && apt-get install freetds-dev -y \
 && apt-get install freetds-bin -y \
 && apt-get install freetds-common -y \
 && apt-get install tdsodbc -y \
 && apt-get install libdbd-odbc-perl -y \
 && apt-get install liblocal-lib-perl -y \
 && apt-get install --reinstall build-essential -y

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

#Ubuntu 18.04
RUN curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install msodbcsql17
# optional: for bcp and sqlcmd
RUN ACCEPT_EULA=Y apt-get install mssql-tools
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

### fim da instalação do driver ODBC da Microsoft

RUN python3.8 -m pip install pyodbc==4.0.30


COPY ./requirements-python3.8.txt /requirements-python3.8.txt


RUN python3.8 -m pip install azure-storage-blob --upgrade --force-reinstall
RUN python3.8 -m pip install azure-storage-blob --user

#RUN python3.8 -m pip install azure-storage-blob --upgrade --force-reinstall
#RUN python3.8 -c "from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient"

RUN python3.8 -m pip install azure-storage-file-datalake --upgrade --force-reinstall
RUN python3.8 -m pip install azure-storage-file-datalake --user

# Upgrade pip
# Create airflow user 
# Install apache airflow with subpackages
RUN pip install --upgrade pip && \
    useradd -ms /bin/bash -d ${AIRFLOW_HOME} airflow && \
    pip install apache-airflow[all_dbs,postgres,docker]==${AIRFLOW_VERSION} --constraint /requirements-python3.8.txt





# Copy the entrypoint.sh from host to container (at path AIRFLOW_HOME)
COPY ./entrypoint.sh /entrypoint.sh
# COPY config/airflow.cfg ${AIRFLOW_USER_HOME}/airflow.cfg

# Set the entrypoint.sh file to be executable
RUN chmod +x /entrypoint.sh

# Set the owner of the files in AIRFLOW_HOME to the user airflow
RUN chown -R airflow: ${AIRFLOW_HOME}

# Set the username to use
USER airflow

# Set workdir (it's like a cd inside the container)
WORKDIR ${AIRFLOW_HOME}

# Create the dags folder which will contain the DAGs
RUN mkdir dags

# Expose ports (just to indicate that this container needs to map port)
EXPOSE 8080

# Execute the entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
