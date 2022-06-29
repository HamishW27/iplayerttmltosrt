#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from xml.dom import minidom
import re


class ttml2srt():

    def __init__(self, filepath) -> None:

        self.filepath = filepath
        altered_file = self.replace_multi()
        self.ttml_file = minidom.parseString(altered_file)
        self.subs = []
        self.times = []
        self.srt = ''
        self.getText()
        self.getTimes()
        self.format_srt()

    def replace_multi(self):
        textfile = open(self.filepath, 'r')
        filetext = textfile.read()
        textfile.close()
        new_text = re.sub('</span><br/><span style="S[0-9]">',
                          ' ', filetext)
        new_text = re.sub('</span><span style="S[0-9]">',
                          ' ', new_text)
        return new_text

    def getText(self):
        texts = self.ttml_file.getElementsByTagName('span')
        for text in texts:
            self.subs.append(text.firstChild.data)

    def getTimes(self):
        times = self.ttml_file.getElementsByTagName('p')
        for time in times:
            self.times.append([time.attributes['begin'].value,
                              time.attributes['end'].value])

    def format_srt(self):
        for no, sub, time in zip(range(1, len(
                self.subs) + 1), self.subs, self.times):
            self.srt += (f'{no}\n{time[0]} -- > {time[1]}\n{sub}\n\n')
        return self.srt

    def write_srt(self):
        new_filename = self.filepath.replace('.ttml', '.srt')
        text_file = open(new_filename, 'wt')
        text_file.write(self.srt)
        text_file.close()


if __name__ == '__main__':

    import argparse

    argparser = argparse.ArgumentParser(
        description='Convert TTML document to SubRip (SRT).')
    argparser.add_argument('ttml-file',
                           help='TTML subtitle file',
                           action='store')
    args = argparser.parse_args()

    ttml = ttml2srt(getattr(args, 'ttml-file'))
    ttml.write_srt()
