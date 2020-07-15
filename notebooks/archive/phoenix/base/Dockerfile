# FROM python:3.6-stretch
FROM continuumio/miniconda3

LABEL Aivin V. Solatorio <asolatorio@worldbank.org>

RUN groupadd -g 999 wb_nlp_user && useradd -g 999 -u 999 -d /phoenix -m wb_nlp_user

RUN apt-get update && \
    apt-get install -y enchant && \
    apt-get clean && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /phoenix

##### Supplanted by conda
# COPY --chown=wb_nlp_user ./requirements.txt .
# RUN pip install --upgrade pip && pip install -r requirements.txt

COPY --chown=wb_nlp_user ./phoenix-wb-nlp.env.yml .
RUN conda env create -f phoenix-wb-nlp.env.yml

# Add wb-nlp environment to PATH to make sure that the correct python installation is used
ENV PATH /opt/conda/envs/wb-nlp/bin:$PATH
RUN echo "conda activate wb-nlp" >> ~/.bashrc

##### Supplanted by conda install -c conda-forge spacy-model-en_core_web_sm nltk_data
# COPY --chown=wb_nlp_user ./install_nltk.py .
# RUN python -m spacy download en && python install_nltk.py

# conda spacy version spacy=2.2.1=py37hc9558a2_0
RUN pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.0/en_core_web_sm-2.2.0.tar.gz
RUN git clone https://github.com/vishnubob/wait-for-it.git /wait-for-it && chown -R wb_nlp_user:wb_nlp_user /wait-for-it

CMD ["/bin/bash"]
