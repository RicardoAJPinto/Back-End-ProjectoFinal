from app import *
from flask_restful import Resource, Api
from json import dumps
from flask import jsonify, url_for

DetectOS = [
    {
        'id': 1,
        "system": "Windows",
        "node": "Mr-Sequeira",
        "release": "10",
        "version": "10.0.17134",
        "machine": "AMD64",
        "processor": "Intel64 Family 6 Model 69 Stepping 1, GenuineIntel"
    },
    {
        'id': 2,
        "system": "Linux",
        "node": "xxxxxx",
        "release": "xxxxx",
        "version": "xxxx",
        "machine": "xxxxx",
        "processor": "Intel64 Family 6 Model 69 Stepping 1, GenuineIntel"
    }
]

def make_public_DetectOS(scan):
    new_scan = {}
    for field in scan:
        if field == 'id':
            new_scan['uri'] = url_for('get_scans', scan_id=scan['id'], _external=True)
        else:
            new_scan[field] = scan[field]
    return new_scan

