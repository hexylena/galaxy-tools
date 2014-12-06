#!/usr/bin/env python
import urllib, urllib2
import sys
import subprocess
import json
import hashlib
import os
import logging
logging.basicConfig()
log = logging.getLogger()

try:
    os.makedirs("output")
except:
    #TODO
    pass

try:
    URL = sys.argv[1]
except:
    log.error("Must provide a url as the only argument")

req = urllib2.urlopen(URL)
page = req.read()
comments = [x.strip() for x in page.split('\n') if x.strip().startswith('<!--')]

prefix = '<!--gsafjson'
suffix = '-->'
gsafjson_data = [x[len(prefix): -len(suffix)].strip() for x in comments if 'gsafjson' in x]
print "Found %s files" % len(gsafjson_data)
for gsafjson in gsafjson_data:
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
    file_md5 = hashlib.md5(open(file_path).read()).hexdigest()
    log.debug("Hashed to %s" % file_md5)

    if file_md5 != data['md5']:
        log.warning('md5sum mismatch: %s != %s' % (file_md5, data['md5']))

    try:
        subprocess.check_call(['gunzip', file_path])
    except:
        log.error("Couldn't extract %s" % data['filename'])
