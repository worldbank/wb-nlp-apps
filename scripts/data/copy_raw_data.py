'''This script is used to sync data from the sandbox server into the gw1 server.
'''
import os
import subprocess as sub
# from pathlib import Path

org_ids = ["adb", "afdb", "eclac", "epdc", "escap", "fame", "fao", "iadb", "iiep", "ilo",
           "oecd", "uneca", "unece", "unescwa", "unhcr", "unido", "unodc", "unpd", "wfp", "who"]

# base = Path("/decfile2/Modeling/NLP/ihsn_scrapers/scrapers")
base = "/decfile2/Modeling/NLP/ihsn_scrapers/scrapers"

SOURCE_SERVER = "w0lxsnlp01"
# TARGET = Path("/Documentum/Aivin/corpus")
TARGET = "/Documentum/Aivin/corpus"


def get_source(source, target_dir):
    return ["rsync", "-avP", SOURCE_SERVER + ":" + source + "/*.pdf", target_dir + "/"]


for org_id in org_ids:
    # source1 = base / org_id / f"{org_id}_files" / "full"
    # source2 = base / org_id / org_id / "full"

    # source1 = f"{base}/{org_id}/{org_id}_files/full"
    # source2 = f"{base}/{org_id}/{org_id }/full"

    source1 = base + "/" + org_id + "/" + org_id + "_files/full"
    source2 = base + "/" + org_id + "/" + org_id + "/full"

    # target = TARGET / org_id.upper() / "PDF_ORIG"
    # target = f"{TARGET}/{org_id.upper()}/PDF_ORIG"
    target = TARGET + "/" + org_id.upper() + "/PDF_ORIG"

    # if not target.exists():
    #     target.mkdir(parents=True)

    if not os.path.isdir(target):
        os.makedirs(target)

    source1_cmd = get_source(source1, target)
    source2_cmd = get_source(source2, target)

    sub.call(source1_cmd)
    sub.call(source2_cmd)
