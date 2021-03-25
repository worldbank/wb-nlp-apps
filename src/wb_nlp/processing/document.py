import bs4
import pandas as pd
import re
import requests
import subprocess
import tika
from bs4 import BeautifulSoup
from collections import Counter
from tika import parser
from typing import Union, List
# Make sure that a Tika service is running
# If tika is installed on a local machine, then just replace
# this with `http://localhost:9998`
TIKA_SERVER_ENDPOINT = 'http://tika:9998'


class PDFDoc2Txt:
    """
    Flow:
        - Load the PDF content.
        - Parse using Apache Tika with xmlContent=True flag.
        - Parse xml content using BeautifulSoup.
        - Process content per page by using <div class="page">
        - For each page process paragraphs.
        - For each paragraph, normalize the footnote citations.

    """

    def __init__(self):
        # self.nlp = spacy.load('en_core_web_sm')
        # self.sentences = []

        pass

    def _parse(self, parser, content):
        return parser(content, xmlContent=True, serverEndpoint=TIKA_SERVER_ENDPOINT, requestOptions={"timeout": 600})

    def parse(self, source: Union[bytes, str], source_type: str = 'buffer') -> str:
        """Parse a PDF document to text from different source types.

        Args:
            source:
                Source of the PDF that needs to be converted.
                The source could be a url, a path, or a buffer/file-like object
                to the PDF file.
            source_type:
                Specification of which source type is being provided in `source`.

        Returns:
            A string containing the parsed pdf file.

        """
        if source_type == 'url':
            buf = requests.get(source)
            pdf_text = self._parse(parser.from_buffer, buf.content)

        elif source_type == 'file':
            pdf_text = self._parse(parser.from_file, source)

        elif source_type == 'buffer':
            pdf_text = self._parse(parser.from_buffer, source)

        else:
            raise ValueError(f'Unknown source_type: `{source_type}`')

        text_pages = []
        if pdf_text['content']:
            soup = BeautifulSoup(pdf_text['content'], features="html.parser")
            pages = soup.find_all('div', {'class': 'page'})

            for page in pages:
                text_pages.append(PDFDoc2Txt.process_page(page))

        return text_pages

    @staticmethod
    def process_page(page: bs4.element.Tag) -> str:
        paragraphs = []

        for p in page.find_all('p'):
            paragraph = PDFDoc2Txt.consolidate_paragraph(p.text)
            paragraph = PDFDoc2Txt.normalize_footnote_citations(paragraph)
            if not paragraph:
                continue

            prev_paragraph_end = paragraphs[-1][-1] if paragraphs and paragraphs[-1] else ''

            # .isalpha():
            if prev_paragraph_end and (re.search(r'[a-zA-Z\-\,]', prev_paragraph_end) or (paragraph[0].islower())):
                paragraph = paragraphs[-1] + ' ' + paragraph
                paragraphs[-1] = paragraph
            else:
                paragraphs.append(paragraph)

        # for p in paragraphs:
        #     doc = self.nlp(p)
        #     self.sentences.extend(list(doc.sents))

        paragraphs = '\n\n'.join(paragraphs)
        return paragraphs

    @staticmethod
    def consolidate_paragraph(text_paragraph: str, min_fragment_len: int = 3) -> str:
        """Consolidate a `text_paragraph` with possible multiple newlines into one logical paragraph.

        Tika provides access to extracted text by paragraph. These paragraphs, however, may contain
        multiple newlines that break the paragraph arbitrarily. This function implements some heuristics
        to recover a logical representation of the paragraph.

        Args:
            text_paragraph:
                Text corresponding to an extracted paragraph from Tika.

        Returns:
            A string corresponding to a logical paragraph.

        """
        replace_chars = {'’': "'", '“': '"', '”': '"'}
        line_seps = set([' ', '-'])

        text_paragraph = text_paragraph.replace('\r', '')

        lines = []
        for line in re.findall(r'(.+)(?:$|\r?\n)', text_paragraph):
            prev_line = lines[-1] if lines else ''
            prev_line_end = prev_line[-1] if prev_line else ''

            len_prev_line = len(prev_line.split())
            len_line = len(line.split())

            if line.lstrip().startswith('•'):
                lines.append(line)
            elif len_prev_line <= min_fragment_len and len_line > min_fragment_len:
                # We consider joining consecutive lines if the previous line is
                # reasonably long enough to be considered a valid fragment.
                lines.append(line)
            elif prev_line_end in line_seps:
                if '-' == prev_line_end:
                    lines[-1] = prev_line.rstrip('-') + line
                else:
                    lines[-1] = prev_line.strip() + ' ' + line
            elif re.search(r'[^\.\:\?]', prev_line_end):
                lines[-1] = prev_line.rstrip('-').strip() + ' ' + line
            else:
                lines.append(line)

        if lines:
            lines[-1] = lines[-1].strip()

        paragraph = '\n'.join(lines)

        for rc in replace_chars:
            paragraph = paragraph.replace(rc, replace_chars[rc])

        return paragraph

    @staticmethod
    def normalize_footnote_citations(text: str) -> str:
        r"""This method tries to detect footnotes and normalizes them.

        This is essential to improve the accuracy of SpaCy's sentence
        detector. Sometimes footnote citations are connected with sentence
        endings that prevents the detection of proper sentence boundary.

        The transformation handles common footnote citation formats:
            pattern: ((?:[a-zA-Z\)]+[.,]|\)))(\d+)(\s)
                - This is a normalizer.1 We will use this.
                - This is a normalizer (great).2 We will use this.
                - This is a normalizer (great).3\nWe will use this.
                - The normalizer (2020)8 is working.
            transforms to:
                - This is a normalizer. _1 We will use this.
                - This is a normalizer (great). _2 We will use this.
                - This is a normalizer (great). _3\nWe will use this.
                - The normalizer (2020) _8 is working.

        Args:
            text:
                Text that will be checked and normalized for footnote
                citations.

        Returns:
            normalized text

        """
        footnote_patterns = [
            r'((?:[a-zA-Z\)]+[.,]|\)))(\d+)(\s)'
        ]

        footnote_patterns = '|'.join(footnote_patterns)

        return re.sub(footnote_patterns, r'\1 _\2\3', text)

    def combine_paragraphs(self, content):
        soup = BeautifulSoup(content, features="html.parser")

        ps = soup.find_all('p')
        unique_ps = []
        for p in ps:
            p = re.sub(r'([a-z])\s*\n([a-z])', r'\1 \2', p.text.strip())
            if not p:
                continue

            last_char = unique_ps[-1][-1] if unique_ps else ''

            if unique_ps and (last_char.isalpha() or last_char == '-') and p[0].islower():
                p = unique_ps[-1].rstrip('-') + ' ' + p

                if p in unique_ps:
                    # Remove the last group since it's already contained in previous paragraph.
                    unique_ps.pop(-1)
                    continue

                unique_ps[-1] = p
            else:
                if p in unique_ps:
                    continue
                unique_ps.append(p)

        # # Consider removing duplicate paragraphs.
        # # The pdf file below contains example of duplicated sections when the pdf is parsed.
        # # Page 18: Better Loans or Better Borrowers?
        # # https://openknowledge.worldbank.org/bitstream/handle/10986/34013/Designing-a-Credit-Facility-for-Women-Entrepreneurs-Lessons-from-the-Ethiopia-Women-Entrepreneurship-Development-Project.pdf
        #     if p in unique_ps:
        #         continue
        #     unique_ps.append(p)


class PDFToTextProcessor:
    def __init__(self):
        pass

    @staticmethod
    def normalize_footnote_citations(text: str) -> str:
        r"""This method tries to detect footnotes and normalizes them.

        This is essential to improve the accuracy of SpaCy's sentence
        detector. Sometimes footnote citations are connected with sentence
        endings that prevents the detection of proper sentence boundary.

        The transformation handles common footnote citation formats:
            pattern: ((?:[a-zA-Z\)]+[.,]|\)))(\d+)(\s)
                - This is a normalizer.1 We will use this.
                - This is a normalizer (great).2 We will use this.
                - This is a normalizer (great).3\nWe will use this.
                - The normalizer (2020)8 is working.
            transforms to:
                - This is a normalizer. _1 We will use this.
                - This is a normalizer (great). _2 We will use this.
                - This is a normalizer (great). _3\nWe will use this.
                - The normalizer (2020) _8 is working.

        Args:
            text:
                Text that will be checked and normalized for footnote
                citations.

        Returns:
            normalized text

        """
        footnote_patterns = [
            r'((?:[a-zA-Z\)]+[.,]|\)))(\d+)(\s)'
        ]

        footnote_patterns = '|'.join(footnote_patterns)

        return re.sub(footnote_patterns, r'\1 _\2\3', text)

    @staticmethod
    def process_for_header(s):
        s = re.sub(r'([^\s])(\n+)', r'\1 \2', s)
        return s

    @staticmethod
    def read_pdf(fname: str, use_stream: bool = True) -> List[str]:
        command = ["pdftotext", str(fname), "-"]
        if use_stream:
            command.append('-raw')
        output = subprocess.run(
            command, stdout=subprocess.PIPE, shell=False)
        pages = output.stdout.decode(errors="ignore").split("\f")
        pages = pages[:-1]  # the last page in the split is always empty.

        return pages

    @staticmethod
    def pdf_to_text(fname: str, common_p_val: float = 0.01, joiner: str = ' ') -> str:
        pages = PDFToTextProcessor.read_pdf(fname)

        return joiner.join(PDFToTextProcessor.remove_headers(pages, common_p_val))

    @staticmethod
    def remove_headers(pages, common_p_val=0.01):
        n_pages = len(pages)
        pages_copy = list(pages)
        page_thresh = max(int(n_pages * common_p_val), 4)
        n_words = 50

        sep = ' '
        potential_headers = [PDFToTextProcessor.process_for_header(
            i).split(sep)[:n_words] for i in pages if len(i.split())]

        for p in potential_headers:
            if p[0].strip().isdigit():
                p.pop(0)

        idx = 2
        common_list = []

        while True:
            pg = pd.Series(dict(Counter([sep.join(i[:idx])
                                         for i in potential_headers if len(sep.join(i[:idx]))]).most_common()))
            pg = pg[pg >= page_thresh]
            if pg.empty:
                break
            common_list.append(pg)
            idx += 1

            if idx > n_words:
                raise ValueError(
                    f'The `idx` value exceeded `n_word` out of `{n_pages}`. Check potential_headers data.')

        len(common_list)

        common_list_df = pd.concat(common_list[::-1])
        common_list_df.head()
        common_list_df.tail()

        comms = [i.split(sep) for i in common_list_df.index]

        for ix, l in enumerate(pages):
            ll = PDFToTextProcessor.process_for_header(l).split(sep)
            if ll[0].strip().isdigit():
                ll.pop(0)

            # if ix and ix % 10 == 0:
            #     print(ix)
            for c in comms:
                ixl = len(c)
                if ll[:ixl] == c:
                    pages_copy[ix] = sep.join(ll[ixl:]).replace(' \n', '\n')
                    break

        return pages_copy


# pdftp = PDFToTextProcessor()
# %time ee = pdftp.pdf_to_text('WDR 2013 low res.pdf', joiner='\f')
# %time e_sents = nltk.sent_tokenize(normalize_footnote_citations(ee))
# proc = [re.sub('\s+', ' ', s.replace('\f', '$$$$$')).strip().replace('$$$$$', '\f') for s in e_sents]
# with open('processed-wdr.txt', 'w') as fl:
#     for p in proc:
#         fl.write(p.replace('\f', '\n\n----page break----\n\n') + '\n\n')
