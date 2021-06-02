
import os
import requests
import pdf2image
import PIL


class DocumentCover:
    def __init__(self, doc_id, cover_dir, pdf_path=None, pdf_url=None, fixed_width=200, fixed_height=None):
        self.doc_id = doc_id
        self.pdf_path = pdf_path
        self.pdf_url = pdf_url
        self.cover_dir = cover_dir
        self.fixed_width = fixed_width
        self.fixed_height = fixed_height

        # self.fname = os.path.join(self.cover_dir, f'{self.doc_id}.png')
        self.fname = self.cover_dir / f'{self.doc_id}.png'

        self.orig_cover = None
        self.cover = None
        self.resized = None

    def get_content_from_url(self):
        self.resized = False
        res = requests.get(self.pdf_url)

        try:
            pages = pdf2image.convert_from_bytes(res.content, size=(
                self.fixed_width, self.fixed_height), single_file=True)
            self.resized = True
        except:
            pages = pdf2image.convert_from_bytes(res.content)

        self.orig_cover = pages[0]

    def get_content_from_file(self):
        self.resized = False
        with open(self.pdf_path, "rb") as open_file:
            content = open_file.read()
            try:
                pages = pdf2image.convert_from_bytes(content, size=(
                    self.fixed_width, self.fixed_height), single_file=True)
                self.resized = True
            except:
                pages = pdf2image.convert_from_bytes(content)

        self.orig_cover = pages[0]

    def standardize_size(self):
        # Not useful if `size` is set in pdf2image.convert_from_bytes
        c = self.orig_cover

        if c is None:
            if self.pdf_path:
                self.get_content_from_file()
            elif self.pdf_url:
                self.get_content_from_url()
            c = self.orig_cover
            assert(c)

        if not self.resized:
            width = self.fixed_width
            w0, h0 = c.size
            c = c.resize((width, int(h0 * width / w0)),
                         resample=PIL.Image.BICUBIC)

        self.cover = c

    def save(self):
        if not os.path.isfile(self.fname):
            cover = self.cover

            if cover is None:
                self.standardize_size()
                cover = self.cover

            cover.save(self.fname)

        return self.doc_id

    def cleanup(self):
        del(self.orig_cover)
        del(self.cover)

        self.orig_cover = None
        self.cover = None
