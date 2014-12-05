#!/usr/bin/env python
import urllib, urllib2
import sys
import subprocess
import json
import hashlib
import os
import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

try:
    os.makedirs("output")
except:
    #TODO
    pass

URL = sys.argv[1]
DATASET_ID = sys.argv[2]

req = urllib2.urlopen(URL)
page = req.read()
comments = [x.strip() for x in page.split('\n') if x.strip().startswith('<!--')]

gx_json = open('galaxy.json', 'w')

prefix = '<!--gsafjson'
suffix = '-->'
for gsafjson in [x[len(prefix): -len(suffix)].strip() for x in comments if 'gsafjson' in x]:
    #{"file_type":"fastq.gz",
    # "JA":"****",
    # "sample_name":"Sample10",
    # "user_data":{"description":{} } ,
    # "md5":"2ea00f4eef8f6a2344b80fbe12ab2eb7",
    # "url":"http://gsaf.s3.amazonaws.com/****",
    # "size_in_mb":45,
    # "filename":"Sample10_S8_L001_R1_001.fastq.gz",
    # "reads":["Sample10_S8_L001_R1_001.fastq.gz","Sample10_S8_L001_R2_001.fastq.gz"],
    # "SA":"***"}
    data = json.loads(gsafjson)
    log.info("Fetching %s" % data['filename'])
    file_path = os.path.join('output', data['filename'])
    urllib.urlretrieve(data['url'], file_path)
    log.info("Hashing file")
    file_md5 = hashlib.md5(open(file_path).read()).hexdigest()
    log.debug("Hashed to %s" % file_md5)

    stderr = ''
    if file_md5 != data['md5']:
        stderr = 'md5sum mismatch: %s != %s' % (file_md5, data['md5'])

    # Galaxy.json
    # {"name": "lambda.fa", "stdout": "uploaded fasta file", "line_count": 811, "ext": "fasta", "dataset_id": 16220, "type": "dataset"}
    line_count = subprocess.check_output(['wc', '-l', file_path]).strip()
    line_count = line_count[0:line_count.index(' ')]

    galaxy_json = {
        'name': data['filename'].strip(data['file_type']),
        'stdout': None,
        'stderr': stderr,
        'line_count': int(line_count),
        # TODO, check that data is really .gz
        'ext': data['file_type'].strip('.gz'),
        'dataset_id': DATASET_ID,
        'type': 'dataset'
    }

    try:
        subprocess.check_call(['gunzip', file_path])
    except:
        log.error("Couldn't extract %s" % data['filename'])

    gx_json.write(json.dumps(galaxy_json) + "\n")

