""" This pipeline processes the raw data from the scraping.
The input expected are the following:

- scrapers/<corpus_id>/corpus/<corpus_id>/PDF_ORIG
- scrapers/<corpus_id>/<corpus_id>_metadata.jsonl

Optional data:
- scrapers/<corpus_id>/corpus/<corpus_id>/TXT_ORIG


Expected output:

- PDF cover
- Extracted PDF text (TXT_ORIG)
    - EN_TXT_ORIG
    - NON_EN_TXT_ORIG

1. Get metadata

"""

import json

from pathlib import Path

from prefect import task, Flow, Parameter


from wb_nlp import dir_manager
from wb_nlp.types.metadata import MetadataModel
from wb_nlp.processing import document
from wb_nlp.extraction.pdf_cover import DocumentCover
"""
1.
"""
################
# METADATA TASKS
################


@task
def extract_corpus_clean_metadata_ids(corpus_id):
    l_corpus_id = corpus_id.lower()
    clean_metadata_jsonl = Path(dir_manager.get_data_dir(
        "corpus", corpus_id, f"{l_corpus_id}_clean_metadata.jsonl"))
    clean_ids = set()

    if clean_metadata_jsonl.exists():

        with open(clean_metadata_jsonl) as json_file:
            for line in json_file:
                if line.strip():
                    meta = json.loads(line.strip())
                    meta_id = meta["id"]

                    clean_ids.add(meta_id)

    return clean_ids


@task
def extract_corpus_raw_metadata(corpus_id, clean_ids, size=100):
    l_corpus_id = corpus_id.lower()
    corpus_root = Path(dir_manager.get_path_from_root("scrapers", l_corpus_id))

    metadata_jsonl = corpus_root / f"{l_corpus_id}_metadata.jsonl"

    data = []

    seen_ids = clean_ids

    with open(metadata_jsonl) as json_file:
        for line in json_file:
            if line.strip():
                meta = json.loads(line.strip())
                meta_id = meta["id"]

                if meta_id in seen_ids:
                    continue

                pdf_path = corpus_root / "corpus" / \
                    corpus_id / "PDF_ORIG" / f"{meta_id}.pdf"

                if not pdf_path.exists():
                    continue

                data.append(meta)
                seen_ids.add(meta_id)

                if len(seen_ids) >= size:
                    break

    return data


@task
def persist_temp_clean_metadata(metadata):
    """
    Persist a batch of cleaned metadata of a given corpus into a temp file.
    """
    if len(metadata) == 0:
        return

    meta = metadata[0]
    corpus_id = meta["corpus"]
    l_corpus_id = corpus_id.lower()

    tmp_clean_metadata_jsonl = Path(dir_manager.get_data_dir(
        "corpus", corpus_id, f"{l_corpus_id}_clean_metadata.tmp.jsonl"))

    if not tmp_clean_metadata_jsonl.parent.exists():
        tmp_clean_metadata_jsonl.parent.mkdir(parents=True)

    with open(tmp_clean_metadata_jsonl, 'w') as json_outfile:
        for meta in metadata:

            # Write data to temp file
            json.dump(meta, json_outfile)
            json_outfile.write("\n")


@task
def validate_corpus_metadata(meta):
    major_doc_type = meta.get("major_doc_type")
    if not isinstance(major_doc_type, list) and major_doc_type:
        meta["major_doc_type"] = [major_doc_type]

    # Validate based on the metadata schema
    meta = json.loads(MetadataModel(**meta).json())
    return meta

################
# PDF TASKS
################


@task
def get_pdf_paths(meta):
    corpus_id = meta["corpus"]
    meta_id = meta["id"]
    l_corpus_id = corpus_id.lower()

    input_file = Path(dir_manager.get_path_from_root(
        "scrapers", l_corpus_id, "corpus", corpus_id, "PDF_ORIG", f"{meta_id}.pdf"))

    return input_file


@task
def create_corpus_dirs(corpus_id):
    corpus_dir = Path(dir_manager.get_data_dir(
        "corpus", corpus_id))

    for dir_name in ["TXT_ORIG", "COVER", "EN_TXT_ORIG", "NON_EN_TXT_ORIG"]:
        dir_path = corpus_dir / dir_name
        if not dir_path.exists():
            dir_path.mkdir(parents=True)


@task
def convert_pdf_to_text(input_file):
    '''
    Wrapper function for joblib to parallelize the cleaning of the text files.

    input_file: assumes this form /path-to-corpus/corpus/<corpus_id>/PDF_ORIG/<doc_id>.pdf
    '''
    doc_id = input_file.stem
    corpus_id = input_file.parent.parent.name

    output_file = Path(dir_manager.get_data_dir(
        "corpus", corpus_id, "TXT_ORIG", f"{doc_id}.txt"))

    if not output_file.exists():
        pages = document.PDFDoc2Txt().parse(
            source=str(input_file.resolve()), source_type="file")

        with open(output_file, "w") as out_file:
            out_file.write(" ".join(pages))

    return output_file


@task
def extract_pdf_cover(input_file):
    doc_id = input_file.stem
    corpus_id = input_file.parent.parent.name
    cover_dir = Path(dir_manager.get_data_dir(
        "corpus", corpus_id, "COVER"))

    # ret = dict(status='ok', doc_id=doc_id,
    #            corpus_id=corpus_id, pdf_path=str(input_file))

    dc = DocumentCover(
        doc_id=doc_id, cover_dir=cover_dir, pdf_path=input_file)
    r = dc.save()
    dc.cleanup()

    # try:
    # except Exception as e:
    #     ret['status'] = e.__str__()

    # return ret


# def transform_corpus_metadata(metadata):
#     validated_metadata = []
#     for meta in metadata:
#         major_doc_type = meta.get("major_doc_type")
#         if not isinstance(major_doc_type, list) and major_doc_type:
#             meta["major_doc_type"] = [major_doc_type]

#         # Validate based on the metadata schema
#         meta = json.loads(MetadataModel(**meta).json())
#         validated_metadata.append(meta)

#     return validated_metadata


def main():
    with Flow("cleaning") as flow:
        corpus_id = Parameter("corpus_id", default="WB")
        max_process_size = Parameter("size", default=100)

        create_corpus_dirs(corpus_id)

        corpus_clean_ids = extract_corpus_clean_metadata_ids(corpus_id)

        corpus_metadata = extract_corpus_raw_metadata(
            corpus_id, corpus_clean_ids, max_process_size)

        validated_corpus_metadata = validate_corpus_metadata.map(
            corpus_metadata)

        pdf_paths = get_pdf_paths.map(validated_corpus_metadata)

        convert_pdf_to_text.map(pdf_paths)
        extract_pdf_cover.map(pdf_paths)
        persist_temp_clean_metadata(validated_corpus_metadata)

        # reference_data = extract_reference_data()
        # live_data = extract_live_data(airport, radius, reference_data)

        # transformed_live_data = transform(live_data, reference_data)

        # load_reference_data(reference_data)
        # load_live_data(transformed_live_data)

    flow.run(corpus_id="ADB", size=100)


if __name__ == "__main__":
    main()
