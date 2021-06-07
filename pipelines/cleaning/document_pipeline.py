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
from collections import Counter
import html
import json
import shutil
from pathlib import Path
from polyglot.detect import Detector

from prefect import task, Flow, Parameter, flatten, Task
from prefect.executors import DaskExecutor
from prefect.triggers import all_finished
from prefect.tasks.shell import ShellTask

from wb_nlp import dir_manager
from wb_nlp.types.metadata import MetadataModel
from wb_nlp.processing import document
from wb_nlp.extraction.pdf_cover import DocumentCover
from wb_nlp.extraction.english_content_extractor import filter_document_by_language
"""
1.
"""
###########
# FUNCTIONS
###########

MAX_LINES = 500

shell_task = ShellTask(helper_script=f"cd {dir_manager.get_path_from_root()}")


def get_clean_metadata_file(corpus_id):
    l_corpus_id = corpus_id.lower()

    return Path(dir_manager.get_data_dir(
        "corpus", corpus_id, f"{l_corpus_id}_clean_metadata.jsonl"))


def raw_pdf_file_exists(corpus_id, doc_id, scraper_root=None):
    if scraper_root is None:
        l_corpus_id = corpus_id.lower()
    else:
        l_corpus_id = scraper_root.lower()

    pdf_path = Path(
        dir_manager.get_path_from_root(
            "scrapers", l_corpus_id,
            "corpus", corpus_id, "PDF_ORIG", f"{doc_id}.pdf"
        )
    )

    return pdf_path.exists()

################
# METADATA TASKS
################


@task
def extract_corpus_clean_metadata(corpus_id):
    clean_metadata_jsonl = get_clean_metadata_file(corpus_id)

    metadata = []

    if clean_metadata_jsonl.exists():
        with open(clean_metadata_jsonl) as json_file:
            metadata = [json.loads(line.strip())
                        for line in json_file if line.strip()]

    return metadata


@task
def extract_corpus_clean_metadata_ids(clean_metadata):
    return {m["id"] for m in clean_metadata}


@task
def build_split_corpus_raw_metadata_file_command(corpus_id, scraper_root=None):
    if scraper_root is None:
        l_corpus_id = corpus_id.lower()
    else:
        l_corpus_id = scraper_root.lower()

    # Make sure no data in /tmp/<corpus_id> is present.
    tmp_dirpath = Path('/tmp') / corpus_id
    if tmp_dirpath.exists() and tmp_dirpath.is_dir():
        shutil.rmtree(tmp_dirpath)
        tmp_dirpath.mkdir(parents=True)

    corpus_root = Path(dir_manager.get_path_from_root("scrapers", l_corpus_id))

    metadata_jsonl = corpus_root / f"{l_corpus_id}_metadata.jsonl"
    split_files_command = f"split -a 5 -d -l {MAX_LINES} {metadata_jsonl} /tmp/{corpus_id}/raw_metadata.jsonl"

    print(split_files_command)

    return split_files_command


@task
def get_split_raw_metadata_files(corpus_id, size=None):
    p = Path(f"/tmp/{corpus_id}")
    files = sorted(p.glob("raw_metadata.jsonl*"))
    if size:
        num_files = (size // MAX_LINES) + 1
        files = files[:num_files]

    return files


def _meta_normalization(meta):

    list_fields = [
        "adm_region", "author", "country", "doc_type", "geo_region",
        "keywords", "major_doc_type", "project_id", "topics_src",
        "wb_lending_instrument", "wb_major_theme",
        "wb_project_id", "wb_sector", "wb_subtopic_src", "wb_theme"]

    for field in list_fields:
        if field in meta:
            field_value = meta.get(field)
            if field_value:
                if not isinstance(field_value, list):
                    meta[field] = [field_value]

            else:
                # Assuming field_value is an empty string, empty list, etc.
                meta[field] = None

    date_published = meta.get("date_published")
    if not date_published:
        # This handles the initial empty string values in the WB scraper
        meta["date_published"] = None

    meta["title"] = html.unescape(meta.get("title", ""))

    return meta


class ExtractCorpusRawMetadataFromPart(Task):
    def run(self, part_file, clean_metadata_ids, scraper_root=None):
        corpus_id = part_file.parent.name
        data = []

        seen_ids = clean_metadata_ids

        with open(part_file) as json_file:
            for line in json_file:
                if line.strip():
                    meta = json.loads(line.strip())
                    doc_id = meta["id"]

                    if doc_id in seen_ids:
                        continue

                    if not raw_pdf_file_exists(corpus_id, doc_id, scraper_root):
                        continue

                    data.append(meta)
                    seen_ids.add(doc_id)

        return data


@task
def extract_corpus_raw_metadata(corpus_id, clean_metadata_ids, size=None, scraper_root=None):
    l_corpus_id = corpus_id.lower()
    corpus_root = Path(dir_manager.get_path_from_root("scrapers", l_corpus_id))

    metadata_jsonl = corpus_root / f"{l_corpus_id}_metadata.jsonl"

    data = []

    seen_ids = clean_metadata_ids

    with open(metadata_jsonl) as json_file:
        for line in json_file:
            if line.strip():
                meta = json.loads(line.strip())
                doc_id = meta["id"]

                if doc_id in seen_ids:
                    continue

                if not raw_pdf_file_exists(corpus_id, doc_id, scraper_root):
                    continue

                data.append(meta)
                seen_ids.add(doc_id)

                if size and len(seen_ids) >= size:
                    break

    return data


def _persist_clean_metadata(metadata, clean_metadata_ids):
    """
    Persist a batch of cleaned metadata of a given corpus into a temp file.
    """
    invalid_metadata = [i["meta"] for i in metadata if not i["ok"]]

    if invalid_metadata:
        corpus_id = invalid_metadata[0]["corpus"]
        with open(Path(dir_manager.get_data_dir("corpus", corpus_id, "invalid_metadata.json")), "w") as json_file:
            json.dump(invalid_metadata, json_file)

    metadata = [i["meta"] for i in metadata if i["ok"]]

    if len(metadata) == 0:
        return clean_metadata_ids

    final_data = []
    meta = metadata[0]
    corpus_id = meta["corpus"]

    clean_metadata_jsonl = get_clean_metadata_file(corpus_id)

    processed_ids = clean_metadata_ids

    if not clean_metadata_jsonl.parent.exists():
        clean_metadata_jsonl.parent.mkdir(parents=True)

    with open(clean_metadata_jsonl, 'a+') as json_outfile:
        for meta in metadata:

            if meta["id"] in processed_ids:
                continue

            # Write data to temp file
            json.dump(meta, json_outfile)
            json_outfile.write("\n")

            processed_ids.add(meta["id"])

            final_data.append(meta)

    return processed_ids


@task
def persist_clean_metadata(metadata, clean_metadata_ids):
    return _persist_clean_metadata(metadata, clean_metadata_ids)


@task
def persist_batched_clean_metadata(batched_metadata, clean_metadata_ids):
    return _persist_clean_metadata(
        [meta for batch in batched_metadata for meta in batch],
        clean_metadata_ids)


@task
def validate_corpus_metadata_part(metadata):
    data = []
    for meta in metadata:
        is_ok = True
        meta = _meta_normalization(meta)

        # Validate based on the metadata schema
        try:
            meta = json.loads(MetadataModel(**meta).json())
        except Exception as e:
            is_ok = False
        data.append(dict(meta=meta, ok=is_ok))

    return data


@task
def validate_corpus_metadata(meta):
    is_ok = True
    meta = _meta_normalization(meta)

    # Validate based on the metadata schema
    try:
        meta = json.loads(MetadataModel(**meta).json())
    except Exception as e:
        is_ok = False
    return dict(meta=meta, ok=is_ok)


@task
def aggregate_metadata(old_metadata, new_metadata):
    return old_metadata + new_metadata


################
# PDF TASKS
################

def _get_pdf_paths(corpus_id, metadata_ids, scraper_root=None):
    if scraper_root is None:
        l_corpus_id = corpus_id.lower()
    else:
        l_corpus_id = scraper_root.lower()

    base = Path(dir_manager.get_path_from_root(
        "scrapers", l_corpus_id, "corpus", corpus_id, "PDF_ORIG"))

    return [base / f"{doc_id}.pdf" for doc_id in metadata_ids]


@task
def get_pdf_paths(corpus_id, metadata_ids, scraper_root=None):
    return _get_pdf_paths(corpus_id, metadata_ids, scraper_root)


@task
def get_batched_pdf_paths(corpus_id, metadata_ids, scraper_root=None):
    batch_size = 50
    pdf_paths = _get_pdf_paths(corpus_id, metadata_ids, scraper_root)

    batched_pdf_paths = [pdf_paths[i: i+batch_size]
                         for i in range(0, len(pdf_paths), batch_size)]

    return batched_pdf_paths


@task
def create_corpus_dirs(corpus_id):
    corpus_dir = Path(dir_manager.get_data_dir(
        "corpus", corpus_id))

    for dir_name in ["TXT_ORIG", "COVER", "EN_TXT_ORIG", "NON_EN_TXT_ORIG"]:
        dir_path = corpus_dir / dir_name
        if not dir_path.exists():
            dir_path.mkdir(parents=True)

    tmp_path = Path(f"/tmp/{corpus_id}")
    if not tmp_path.exists():
        tmp_path.mkdir()

    return corpus_id


def _convert_pdf_to_text(input_file):
    '''
    Wrapper function for joblib to parallelize the cleaning of the text files.

    input_file: assumes this form /path-to-corpus/corpus/<corpus_id>/PDF_ORIG/<doc_id>.pdf
    '''
    doc_id = input_file.stem
    corpus_id = input_file.parent.parent.name

    output_file = Path(dir_manager.get_data_dir(
        "corpus", corpus_id, "TXT_ORIG", f"{doc_id}.txt"))

    scraped_txt_file = input_file.parent.parent / "TXT_ORIG" / f"{doc_id}.txt"

    if not output_file.exists():
        if not scraped_txt_file.exists():
            pages = document.PDFDoc2Txt().parse(
                source=str(input_file.resolve()), source_type="file")

            with open(output_file, "w") as out_file:
                out_file.write(" ".join(pages))
        else:
            shutil.copy(scraped_txt_file, output_file)

    return output_file


@task
def convert_pdf_to_text(input_file):
    return _convert_pdf_to_text(input_file)


@task
def convert_batched_pdf_to_text(input_files):
    return [_convert_pdf_to_text(input_file) for input_file in input_files]


def _extract_pdf_cover(input_file):
    doc_id = input_file.stem
    corpus_id = input_file.parent.parent.name
    cover_dir = Path(dir_manager.get_data_dir(
        "corpus", corpus_id, "COVER"))

    dc = DocumentCover(
        doc_id=doc_id, cover_dir=cover_dir, pdf_path=input_file)

    try:
        r = dc.save()
    except Exception as e:
        # Gracefully handle cover extraction error.
        # Example: pdf2image.exceptions.PDFPageCountError: Unable to get page count.
        print(e)

    dc.cleanup()


@task
def extract_pdf_cover(input_file):
    return _extract_pdf_cover(input_file)


@task
def extract_batched_pdf_cover(input_files):
    for input_file in input_files:
        _extract_pdf_cover(input_file)


#######################
# TEXT PROCESSING TASKS
#######################

def _extract_valid_language_lines(input_file):
    doc_id = input_file.stem
    corpus_id = input_file.parent.parent.name

    output_file = Path(dir_manager.get_data_dir(
        "corpus", corpus_id, "EN_TXT_ORIG", f"{doc_id}.txt"))

    non_en_output_file = Path(dir_manager.get_data_dir(
        "corpus", corpus_id, "NON_EN_TXT_ORIG", f"{doc_id}.txt"))

    is_ok = True
    message = "OK"

    if not output_file.exists():
        with open(input_file, "rb") as open_file:
            text = open_file.read().decode("utf-8", errors="ignore").strip()

            # Only process texts that mainly contain English content.
            if text and (len(text.split()) >= 10):
                d = Detector(
                    "".join(x for x in text if x.isprintable()), quiet=True)
                if d.language.code == "en" and d.language.confidence > 50:
                    pval = 0.05
                    non_en_spell_df = filter_document_by_language(
                        text, return_df=True)

                    if non_en_spell_df is not None:
                        en_txt = "\n".join(
                            non_en_spell_df[non_en_spell_df["pval"] > pval]["sent"])
                        non_en_txt = "\n".join(
                            non_en_spell_df[non_en_spell_df["pval"] <= pval]["sent"])

                        with open(output_file, "w") as out_file:
                            out_file.write(en_txt)

                        with open(non_en_output_file, "w") as non_en_out_file:
                            non_en_out_file.write(non_en_txt)
                    else:
                        is_ok = False
                        message = "non_en_spell_df is None"
                else:
                    is_ok = False
                    message = "Document language not primarily in English."
            else:
                is_ok = False
                message = "Raw text has less that 10 tokens."

    return dict(is_ok=is_ok, output_file=output_file, message=message)


@task
def extract_valid_language_lines(input_file):
    return _extract_valid_language_lines(input_file)


@task
def extract_batched_valid_language_lines(input_files):
    return [_extract_valid_language_lines(input_file) for input_file in input_files]


def _end_task_report(valid_text_files):
    print("Summary")
    for k, v in Counter([v["message"] for v in valid_text_files]).most_common():
        print(f"\t{k: <70}={v}")


@task
def end_task_report(valid_text_files):
    _end_task_report(valid_text_files)

    # success = 0
    # not_success = 0
    # for p in valid_text_files:
    #     if p["is_ok"]:
    #         success += 1
    #     else:
    #         not_success += 1

    # print(f"Summary: success={success} not_success={not_success}")


@task
def end_batched_task_report(batched_valid_text_files):
    valid_text_files = [
        tf for batch in batched_valid_text_files for tf in batch]
    _end_task_report(valid_text_files)


@task(trigger=all_finished)
def remove_corpus_tmp_dir(corpus_id):

    tmp_dirpath = Path('/tmp') / corpus_id
    if tmp_dirpath.exists() and tmp_dirpath.is_dir():
        shutil.rmtree(tmp_dirpath)


# def dump_final_metadata(corpus_id, valid_text_files):
#     l_corpus_id = corpus_id.lower()

#     tmp_clean_metadata_jsonl = Path(dir_manager.get_data_dir(
#         "corpus", corpus_id, f"{l_corpus_id}_clean_metadata.tmp.jsonl"))
#     pass


def main(corpus_id, scraper_root=None, size=None):
    assert corpus_id, "Please specify the corpus_id to be processed with the --corpus-id=<corpus_id> parameter..."

    with Flow("cleaning") as flow:
        flow_corpus_id = Parameter("corpus_id", default="WB")
        flow_scraper_root = Parameter("scraper_root", default=None)
        max_process_size = Parameter("size", default=None)

        flow_corpus_id = create_corpus_dirs(flow_corpus_id)

        split_files_command = build_split_corpus_raw_metadata_file_command(
            flow_corpus_id, flow_scraper_root)

        command_result = shell_task(command=split_files_command)

        corpus_clean_metadata = extract_corpus_clean_metadata(flow_corpus_id)
        corpus_clean_metadata_ids = extract_corpus_clean_metadata_ids(
            corpus_clean_metadata)

        split_raw_metadata_files = get_split_raw_metadata_files(
            flow_corpus_id, max_process_size)

        split_raw_metadata_files.set_upstream(command_result)

        corpus_metadata_part = ExtractCorpusRawMetadataFromPart()

        corpus_metadata_part.set_upstream(
            split_raw_metadata_files, key="part_file", mapped=True)  # , flow=flow)
        corpus_metadata_part.set_upstream(
            corpus_clean_metadata_ids, key="clean_metadata_ids", mapped=False)  # , flow=flow)
        corpus_metadata_part.set_upstream(
            flow_scraper_root, key="scraper_root", mapped=False)  # , flow=flow)

        validated_corpus_metadata_part = validate_corpus_metadata_part.map(
            corpus_metadata_part)

        # corpus_metadata = extract_corpus_raw_metadata(
        #     flow_corpus_id, corpus_clean_metadata_ids, max_process_size, flow_scraper_root)

        # validated_corpus_metadata = validate_corpus_metadata.map(
        #     corpus_metadata)

        persisted_clean_metadata_ids = persist_batched_clean_metadata(
            validated_corpus_metadata_part, corpus_clean_metadata_ids)

        # persisted_clean_metadata_ids = persist_clean_metadata(
        #     flatten(validated_corpus_metadata_part), corpus_clean_metadata_ids)

        batched_pdf_paths = get_batched_pdf_paths(
            flow_corpus_id, persisted_clean_metadata_ids, flow_scraper_root)

        # pdf_paths = get_pdf_paths(flow_corpus_id, persisted_clean_metadata_ids, flow_scraper_root)

        # full_clean_metadata = aggregate_metadata(
        #     corpus_clean_metadata, persisted_clean_metadata)
        # pdf_paths = get_pdf_paths.map(full_clean_metadata)

        # extract_pdf_cover.map(pdf_paths)
        # corpus_text_files = convert_pdf_to_text.map(pdf_paths)
        # valid_text_files = extract_valid_language_lines.map(corpus_text_files)
        # end_report = end_task_report(valid_text_files)

        extract_batched_pdf_cover.map(batched_pdf_paths)

        batched_corpus_text_files = convert_batched_pdf_to_text.map(
            batched_pdf_paths)

        batched_valid_text_files = extract_batched_valid_language_lines.map(
            batched_corpus_text_files)

        end_report = end_batched_task_report(
            batched_valid_text_files)
        cleanup_task = remove_corpus_tmp_dir(flow_corpus_id)
        cleanup_task.set_upstream(end_report)

        # end_batched_task_report(
        #     batched_valid_text_files)
        # remove_corpus_tmp_dir(flow_corpus_id)

    flow.run(corpus_id=corpus_id, size=size, executor=DaskExecutor(
        adapt_kwargs={"maximum": 128}))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('--corpus-id', dest='corpus_id', type=str)
    parser.add_argument(
        '--scraper-root', dest='scraper_root', type=str, default=None)
    parser.add_argument('--size', dest='size', type=int, default=None)
    args = parser.parse_args()

    main(**vars(args))

    # python document_pipeline.py --corpus-id=WB --size=100
