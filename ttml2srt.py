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
                          '\n', filetext)
        new_text = re.sub('</span><span style="S[0-9]">',
                          '\n', new_text)
        return new_text

    def getText(self):
        texts = self.ttml_file.getElementsByTagName('span')
        for text in texts:
            self.subs.append(text.firstChild.data)

    def getTimes(self):
        times = self.ttml_file.getElementsByTagName('p')
        for time in times:
            begin_time = time.attributes['begin'].value.replace('.', ',')
            ''' Fixes an error where the microseconds are omitted from
            the start or end times resulting in an invalid srt file'''
            if len(begin_time) == 8:
                begin_time = begin_time + ",000"
            end_time = time.attributes['end'].value.replace('.', ',')
            if len(end_time) == 8:
                end_time = end_time + ",000"
            self.times.append([begin_time,
                              end_time])

    def format_srt(self):
        for no, sub, time in zip(range(1, len(
                self.subs) + 1), self.subs, self.times):
            self.srt += (f'{no}\n{time[0]} --> {time[1]}\n{sub}\n\n')
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
                           action='store',
                           nargs='+')
    args = argparser.parse_args()

    for arg in vars(args)['ttml-file']:
        ttml = ttml2srt(arg)
        ttml.write_srt()
