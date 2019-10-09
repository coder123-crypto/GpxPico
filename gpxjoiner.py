#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gpxpico
import sys

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python gpxjoiner.py filename_1 filename_2 filename_3... destination_filename")
        sys.exit(1)

    tracks = [gpxpico.import_track(file_name) for file_name in sys.argv[1:-1]]

    if all(track is not None for track in tracks):
        dest = ('trk', tracks[0][1], [segments for track in tracks for segments in track[2]])
        gpxpico.export_track(dest, sys.argv[-1])