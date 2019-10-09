#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import glob
import gpxpico
from shutil import copyfile

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python gpxtrimmer.py filename")
        sys.exit(1)

    for file_name in glob.glob(sys.argv[1]):
        print('Starting trim {}...'.format(file_name))

        print('\tStarting import points...')
        track = gpxpico.import_track(file_name)
        print('\tFinished import points')

        if track is not None:
            print('\tStarted export points...')
            copyfile(file_name, '{}.bak'.format(file_name))
            gpxpico.export_track(track, file_name)
            print('\tFinished export points')

        print('Finished trim {}'.format(file_name))