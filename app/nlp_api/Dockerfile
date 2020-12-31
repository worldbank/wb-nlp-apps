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
    # Install gcc
    && apt-get install -y gcc g++ 2>&1 \
    #
    # Clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=dialog

ARG ENV_ID=nlp_api
ARG ENV_PROD_FILE=environment.nlp_api.yml

ENV ENV_ID=$ENV_ID
ENV ENV_PROD_FILE=$ENV_PROD_FILE

COPY ./app/nlp_api/${ENV_PROD_FILE} /tmp/${ENV_PROD_FILE}
RUN conda init bash && conda env create -f /tmp/${ENV_PROD_FILE}

WORKDIR /workspace
COPY . .

RUN /opt/conda/envs/${ENV_ID}/bin/python setup.py develop \
    && /opt/conda/envs/${ENV_ID}/bin/python -m nltk.downloader popular \
    && /opt/conda/envs/${ENV_ID}/bin/python -m spacy download en_core_web_sm

# # Always try to install the latest prod env file.
# # This is useful when you installed new packages and updated the env file with
# # conda env export -n ${ENV_ID} --no-builds | grep -v "prefix" > /workspace/${ENV_DEV_FILE}
# RUN conda env update -n ${ENV_ID} --file /tmp/conda-tmp/${ENV_DEV_FILE}  --prune && rm -rf /opt/conda/pkg/*

# Start the server
ARG PORT=8919
ENV PORT=$PORT

CMD /opt/conda/envs/prod/bin/uvicorn app.nlp_api.main:app  --reload --timeout-keep-alive 1200 --port ${PORT}
