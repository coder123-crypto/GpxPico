#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os.path
from xml.dom import minidom
from xml.dom.minidom import Document

def import_track(file_name):
    if (os.path.isfile(file_name)):
        if os.path.splitext(file_name)[1].lower() == '.gpx':
            document = minidom.parse(file_name)
            if len(document.getElementsByTagName('trkseg')) > 0:
                return _import_trk(document)
            elif len(document.getElementsByTagName('rte')) > 0:
                return _import_rte(document)
            else:
                print('Warning: {} is not valid GPX file'.format(file_name))
        else:
           print('Warning: {} is not GPX file'.format(file_name))
    else:
        print('Warning: {} is not file'.format(file_name))

def export_track(track, file_name):
    document = Document()
    gpx = document.createElement('gpx')
    gpx.setAttribute('version', '1.1')
    gpx.setAttribute('xmlns', 'http://www.topografix.com/GPX/1/1')
    gpx.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    gpx.setAttribute('xsi:schemaLocation', 'http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd')
    gpx.setAttribute('creator', 'gpxtrimmer')
    document.appendChild(gpx)

    (mode, name, segments) = track

    if mode == 'trk':
        child = _export_trk(document, name, segments)
    elif mode == 'rte':
        child = _export_rte(document, name, segments)
    else:
        child = None
    
    if child is not None:
        gpx.appendChild(child)
        with codecs.open(file_name, 'w', 'utf-8') as out:
            document.writexml(out, ' ', ' ', '\n', 'utf-8')
    else:
        print('Waring: {} is not valid track mode'.format(mode))

def _import_trk(document):
    name = _get_child_value(document, 'name')
    return ('trk', name, [[_parse_trkpt(trkpt) for trkpt in trkseg.getElementsByTagName('trkpt')] for trkseg in document.getElementsByTagName('trkseg')])

def _import_rte(document):
    name = _get_child_value(document, 'name')
    return ('rte', name, [_parse_rtept(rtept) for rtept in document.getElementsByTagName('rtept')])

def _export_trk(document, name, segments):
    trk = document.createElement('trk')
    if name is not None:
        trk.appendChild(_create_text_node(document, 'name', name))

    for segment in segments:
        trkseg = document.createElement('trkseg')
        [trkseg.appendChild(_create_trkpt(document, point)) for point in segment]
        trk.appendChild(trkseg)

    return trk

def _export_rte(document, name, points):
    rte = document.createElement('rte')
    if name is not None:
        rte.appendChild(_create_text_node(document, 'name', name))

    [rte.appendChild(_create_rtept(document, point)) for point in points]

    return rte

def _parse_trkpt(trkpt):
    track_point = {}
    track_point['latitude'] = trkpt.attributes['lat'].value
    track_point['longitude'] = trkpt.attributes['lon'].value
    time = _get_child_value(trkpt, 'time')
    if time is not None:
        track_point['time'] = time
    ele = _get_child_value(trkpt, 'ele')
    if ele is not None:
        track_point['elevation'] = ele
    return track_point

def _parse_rtept(rtept):
    return _parse_trkpt(rtept)

def _create_trkpt(document, track_point):
    return _create_gpx_track_point(document, track_point, 'trkpt')

def _create_rtept(document, track_point):
    return _create_gpx_track_point(document, track_point, 'rtept')

def _create_gpx_track_point(document, track_point, element_name):
    gpx_track_point = document.createElement(element_name)
    gpx_track_point.setAttribute('lat', track_point['latitude'])
    gpx_track_point.setAttribute('lon', track_point['longitude'])
    if 'time' in track_point:
        gpx_track_point.appendChild(_create_text_node(document, 'time', track_point['time']))
    if 'elevation' in track_point:
        gpx_track_point.appendChild(_create_text_node(document, 'ele', track_point['elevation']))
    return gpx_track_point

def _get_child_value(trkpt_xml_element, child_name):
    childs = trkpt_xml_element.getElementsByTagName(child_name)
    return childs[0].firstChild.nodeValue if len(childs) > 0 else None

def _create_text_node(document, child_name, child_value):
    element = document.createElement(child_name)
    node = document.createTextNode(child_value)
    element.appendChild(node)
    return element