# -*- encoding: utf-8 -*-

import os
import sys
from glob import glob
from tokenization import convert_to_unicode, _is_control, _is_whitespace, _clean_text

from blingfire import text_to_sentences

file_dir = sys.argv[1]
save_dir = sys.argv[2]

def convert_into_sentences(lines):
    stack = []
    sent_L = []
    n_sent = 0
    for chunk in lines[300:-100]:
        if not chunk.strip():
            if stack:
                sents = text_to_sentences(
                    " ".join(stack).strip().replace('\n', ' ')).split('\n')
                sent_L.extend(sents)
                n_sent += len(sents)
                sent_L.append('\n')
                stack = []
            continue
        stack.append(chunk.strip())

    if stack:
        sents = text_to_sentences(
            " ".join(stack).strip().replace('\n', ' ')).split('\n')
        sent_L.extend(sents)
        n_sent += len(sents)
    return sent_L, n_sent

if __name__ == "__main__":
    file_list = list(sorted(glob(os.path.join(file_dir, '*.txt'))))
    out = open(save_dir, 'w', encoding='utf8')

    for i, file_path in enumerate(file_list):
        sents, n_sent = convert_into_sentences(open(file_path, encoding='utf8').readlines())

        sent_a = ''
        for sent in sents:
            sent = convert_to_unicode(sent)
            sent = _clean_text(sent.lower())
            if len(sent) < 35:
                sent_a = ''
                continue
            elif sent_a:
                sent_b = sent
                out.write(sent_a + '\t' + sent_b + '\n')
                sent_a = ''
            else:
                sent_a = sent

        sys.stderr.write(
            '{}/{}\t{}\t{}\n'.format(i, len(file_list), n_sent, file_path))
    out.close()
