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
    # # Install libxi6 (libXi.so.6) for graph-tool
    # && apt-get install -y libxi6 libxtst6 libxfixes3 libxcursor1 libgtk-3-dev 2>&1 \
    # Install poppler-utils for pdftotext
    && apt-get install -y poppler-utils 2>&1 \
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
ENV CONDA_PATH=/opt/conda/envs/${ENV_ID}

COPY ./app/nlp_api/${ENV_PROD_FILE} /tmp/${ENV_PROD_FILE}
RUN conda init bash && conda env create -f /tmp/${ENV_PROD_FILE}

RUN ${CONDA_PATH}/bin/python -m nltk.downloader popular
    # \
    # && /opt/conda/envs/${ENV_ID}/bin/python -m spacy download en_core_web_sm

WORKDIR /workspace
COPY . .
# data/ and models/ must be volume mounted!
# COPY ./setup.py ./setup.cfg ./
# COPY ./notebooks .
# COPY ./scripts .
# COPY ./model_runs .
# COPY ./configs .
# COPY ./app/nlp_api ./app/nlp_api
# COPY ./src .

RUN ${CONDA_PATH}/bin/python setup.py develop

# # Always try to install the latest prod env file.
# # This is useful when you installed new packages and updated the env file with
# # conda env export -n ${ENV_ID} --no-builds | grep -v "prefix" > /workspace/${ENV_DEV_FILE}
# RUN conda env update -n ${ENV_ID} --file /tmp/conda-tmp/${ENV_DEV_FILE}  --prune && rm -rf /opt/conda/pkg/*

# Start the server
ARG PORT=8919
ENV PORT=$PORT

CMD ${CONDA_PATH}/bin/uvicorn app.nlp_api.main:app  --reload --timeout-keep-alive 1200 --host 0.0.0.0 --port ${PORT}
# CMD ["tail", "-f", "/dev/null"]
# CMD ${CONDA_PATH}/bin/gunicorn -w 4 --log-level info --timeout 1200 -k uvicorn.workers.UvicornWorker app.nlp_api.main:app -b 0.0.0.0:${PORT}

#   - conda-forge/linux-64::gensim==3.8.3=py38h950e882_2
#   - conda-forge/noarch::google-cloud-storage==1.31.0=pyh9f0ad1d_0
#   - conda-forge/noarch::smart_open==2.1.1=pyh9f0ad1d_0
#   - conda-forge/noarch::google-cloud-core==1.4.1=pyh9f0ad1d_0
# doney