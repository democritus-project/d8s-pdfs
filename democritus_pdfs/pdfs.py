#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from typing import Iterable

import PyPDF2

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
from files import file_write
from networking import get
from temp_directories import temp_dir_create
from urls import is_url, url_file_name


# TODO: from my experience, this function uses a lot of memory
def pdf_read(pdf_path: str) -> Iterable[str]:
    """Get the string from the PDF at the given path/URL."""
    # check if the pdf_path is a url
    if is_url(pdf_path):
        temp_dir = temp_dir_create()
        # TODO: there should be a function to return a file point to a temporary function if there is not already
        temp_pdf_path = os.path.join(temp_dir.name, url_file_name(pdf_path))
        file_write(temp_pdf_path, get(pdf_path, handle_response_as_bytes=True))
        pdf_path = temp_pdf_path

    with open(pdf_path, 'rb') as f:
        try:
            pdf = PyPDF2.PdfFileReader(f)
        except PyPDF2.utils.PdfReadError as e:
            message = 'Unable to read the pdf at {}: {}'.format(pdf_path, e)
            print(message)
        else:
            for i in range(0, pdf.numPages):
                page = pdf.getPage(i)
                page_content = page.extractText().replace('\n', ' ')
                yield page_content
            # TODO: delete the file if it is stored as a temp file?
