FROM wb-nlp-base:latest

LABEL Aivin V. Solatorio <asolatorio@worldbank.org>
WORKDIR /phoenix

COPY --chown=wb_nlp_user . .

RUN python setup.py install

RUN chown -R wb_nlp_user:wb_nlp_user /phoenix
