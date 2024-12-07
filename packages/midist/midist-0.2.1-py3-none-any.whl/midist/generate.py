# SPDX-FileCopyrightText: 2024 AmaseCocoa
# SPDX-License-Identifier: MIT

import hashlib

def process_file(file_path):
    with open(file_path, 'rb') as f:
        content = f.read()
    text_content = content.decode('utf-8', errors='ignore')
    processed_content = text_content.replace('\r\n', '\n').replace('\r', '\n')
    hash_md5 = hashlib.sha512(processed_content.encode('utf-8', errors='ignore')).hexdigest()
    single_line_content = processed_content.replace('\n', '\n')

    return single_line_content, hash_md5