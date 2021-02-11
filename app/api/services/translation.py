# import services.googletrans_client as gt
import googletrans
from googletrans import client as gt

assert googletrans.__version__ == "3.1.0-alpha"

_trans = gt.Translator()


def translate(text, src='auto', dest='en', with_extra_data=False):
    global _trans

    try:
        result = _trans.translate(text, dest=dest, src=src)
    except:
        # Try to re-aquire new instance.
        _trans = gt.Translator()
        result = _trans.translate(text, dest=dest, src=src)

    payload = dict(
        origin=result.origin,
        translated=result.text,
        src=result.src,
        dest=result.dest,
    )

    if with_extra_data:
        payload['extra_data'] = result.extra_data

    return payload
