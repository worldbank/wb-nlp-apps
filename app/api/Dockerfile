FROM continuumio/miniconda3:latest

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Configure apt and install packages
RUN apt-get update \
    && apt-get -y install --no-install-recommends software-properties-common apt-utils dialog wget ca-certificates 2>&1 \
    && apt-get update \
    #
    #
    # Install enchant libraries for pyenchant
    && apt-get install -y enchant 2>&1 \
    #
    #
    # Clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=dialog

ARG ENV_ID=prod
ARG ENV_PROD_FILE=environment.prod.api.yml

ENV ENV_ID=$ENV_ID
ENV ENV_PROD_FILE=$ENV_PROD_FILE

COPY ./app/api/${ENV_PROD_FILE} /tmp/${ENV_PROD_FILE}
RUN conda init bash && conda env create -f /tmp/${ENV_PROD_FILE}

WORKDIR /workspace

COPY ./setup.py .
COPY ./src ./src
COPY ./app/api ./app/api

RUN /opt/conda/envs/${ENV_ID}/bin/python setup.py develop

# # Always try to install the latest prod env file.
# # This is useful when you installed new packages and updated the env file with
# # conda env export -n ${ENV_ID} --no-builds | grep -v "prefix" > /workspace/${ENV_DEV_FILE}
# RUN conda env update -n ${ENV_ID} --file /tmp/conda-tmp/${ENV_DEV_FILE}  --prune && rm -rf /opt/conda/pkg/*

# Add this so that the container doesn't exit prematurely
CMD ["tail", "-f", "/dev/null"]


