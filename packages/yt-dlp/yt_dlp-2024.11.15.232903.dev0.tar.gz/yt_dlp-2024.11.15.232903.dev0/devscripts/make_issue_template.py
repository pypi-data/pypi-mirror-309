#!/usr/bin/env python3

# Allow direct execution
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import re

from devscripts.utils import get_filename_args, read_file, write_file

VERBOSE_TMPL = '''
  - type: checkboxes
    id: verbose
    attributes:
      label: Provide verbose output that clearly demonstrates the problem
      options:
        - label: Run **your** yt-dlp command with **-vU** flag added (`yt-dlp -vU <your command line>`)
          required: true
        - label: "If using API, add `'verbose': True` to `YoutubeDL` params instead"
          required: false
        - label: Copy the WHOLE output (starting with `[debug] Command-line config`) and insert it below
          required: true
  - type: textarea
    id: log
    attributes:
      label: Complete Verbose Output
      description: |
        It should start like this:
      placeholder: |
        [debug] Command-line config: ['-vU', 'https://www.youtube.com/watch?v=BaW_jenozKc']
        [debug] Encodings: locale cp65001, fs utf-8, pref cp65001, out utf-8, error utf-8, screen utf-8
        [debug] yt-dlp version nightly@... from yt-dlp/yt-dlp-nightly-builds [1a176d874] (win_exe)
        [debug] Python 3.10.11 (CPython AMD64 64bit) - Windows-10-10.0.20348-SP0 (OpenSSL 1.1.1t  7 Feb 2023)
        [debug] exe versions: ffmpeg 7.0.2 (setts), ffprobe 7.0.2
        [debug] Optional libraries: Cryptodome-3.21.0, brotli-1.1.0, certifi-2024.08.30, curl_cffi-0.5.10, mutagen-1.47.0, requests-2.32.3, sqlite3-3.40.1, urllib3-2.2.3, websockets-13.1
        [debug] Proxy map: {}
        [debug] Request Handlers: urllib, requests, websockets, curl_cffi
        [debug] Loaded 1838 extractors
        [debug] Fetching release info: https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest
        Latest version: nightly@... from yt-dlp/yt-dlp-nightly-builds
        yt-dlp is up to date (nightly@... from yt-dlp/yt-dlp-nightly-builds)
        [youtube] Extracting URL: https://www.youtube.com/watch?v=BaW_jenozKc
        <more lines>
      render: shell
    validations:
      required: true
  - type: markdown
    attributes:
      value: |
        > [!CAUTION]
        > ### GitHub is experiencing a high volume of malicious spam comments.
        > ### If you receive any replies asking you download a file, do NOT follow the download links!
        >
        > Note that this issue may be temporarily locked as an anti-spam measure after it is opened.
'''.strip()

NO_SKIP = '''
  - type: checkboxes
    attributes:
      label: DO NOT REMOVE OR SKIP THE ISSUE TEMPLATE
      description: Fill all fields even if you think it is irrelevant for the issue
      options:
        - label: I understand that I will be **blocked** if I *intentionally* remove or skip any mandatory\\* field
          required: true
'''.strip()


def main():
    fields = {'no_skip': NO_SKIP}
    fields['verbose'] = VERBOSE_TMPL % fields
    fields['verbose_optional'] = re.sub(r'(\n\s+validations:)?\n\s+required: true', '', fields['verbose'])

    infile, outfile = get_filename_args(has_infile=True)
    write_file(outfile, read_file(infile) % fields)


if __name__ == '__main__':
    main()
