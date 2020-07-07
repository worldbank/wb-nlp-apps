import bs4
import pandas as pd
import re
import requests
import tika
from bs4 import BeautifulSoup
from tika import parser
from typing import Union


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

    def tika_parse_buffer():
        pass

    def tika_parse_file():
        pass

    def parse(self, source: Union[bytes, str], source_type: str='buffer') -> str:
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
            pdf_text = parser.from_buffer(buf.content, xmlContent=True)

        elif source_type == 'file':
            pdf_text = parser.from_file(source, xmlContent=True)

        elif source_type == 'buffer':
            pdf_text = parser.from_buffer(source, xmlContent=True)

        else:
            raise ValueError(f'Unknown source_type: `{source_type}`')

        soup = BeautifulSoup(pdf_text['content'])
        pages = soup.find_all('div', {'class':'page'})

        text_pages = []
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

            if prev_paragraph_end and (re.search(r'[a-zA-Z\-\,]', prev_paragraph_end) or (paragraph[0].islower())):  # .isalpha():
                paragraph = paragraphs[-1] + ' ' + paragraph
                paragraphs[-1] = paragraph
            else:
                paragraphs.append(paragraph)

#         for p in paragraphs:
#             doc = self.nlp(p)
#             self.sentences.extend(list(doc.sents))

        paragraphs = '\n\n'.join(paragraphs)
        return paragraphs

    @staticmethod
    def consolidate_paragraph(text_paragraph: str, min_fragment_len: int=3) -> str:
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
        line_groups = [[]]

        text_paragraph = text_paragraph.replace('\r', '')

        lines = []
        for line in re.findall(r'(.+)(?:$|\r?\n)', text_paragraph):
            prev_line = lines[-1] if lines else ''
            prev_line_end = prev_line[-1] if prev_line else ''

            len_prev_line = len(prev_line.split())
            len_line = len(line.split())

            # prev_line_end = lines[-1][-1] if lines and lines[-1] else ''

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

#         for line in re.findall(r'(.+)(?:$|\n)', text_paragraph):
#             lines = line_groups[-1]
#             prev_line = lines[-1] if lines else ''
#             prev_line_end = prev_line[-1] if prev_line else ''

#             if prev_line and len(line.split()) > (0.5 * len(prev_line.split())):
#                 if prev_line_end in line_seps:
#                     lines.append(line)
#                     lines[-1] = lines[-1].rstrip('-') + line
#                 elif re.search(r'[^\.\:]', prev_line_end):
#                     lines[-1] = lines[-1].rstrip('-') + ' ' + line
#                 else:
#                     lines.append(line)
#                     line_groups.append([])
#             else:
#                 lines.append(line)
#                 # line_groups.append([])

#         lines = []
#         for lg in line_groups:
#             lines.extend(lg)

        if lines:
            lines[-1] = lines[-1].strip()

        paragraph = '\n'.join(lines)

        for rc in replace_chars:
            paragraph = paragraph.replace(rc, replace_chars[rc])

        return paragraph

    @staticmethod
    def normalize_footnote_citations(text: str) -> str:
        """This method tries to detect footnotes and normalizes them.

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

    def combine_paragraphs(self):

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

        #     if p in unique_ps:
        #         continue
        #     unique_ps.append(p)

        pass
