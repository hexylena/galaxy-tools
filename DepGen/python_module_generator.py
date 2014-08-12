#!/usr/bin/env python
import yaml
import sys

__doc__ = """

    Run with:

        python python_module_generator.py biopython 1.64 biopy-1.64-requirements.txt > biopython.yaml

    This will generate a yaml file for DepGen to make use of.
"""

PACKAGE_NAME = sys.argv[1]
PACKAGE_VERS = sys.argv[2]

d = {
    'meta': {
        'name': PACKAGE_NAME,
        'vers': PACKAGE_VERS,
        'readme': '',
    }
}

try:
    import xmlrpclib
except ImportError:
    import xmlrpc.client as xmlrpclib
client = xmlrpclib.ServerProxy('https://pypi.python.org/pypi')
releases = client.package_releases(PACKAGE_NAME)
if PACKAGE_VERS not in releases:
    raise Exception("Release not listed on PyPi: " + ','.join(releases))

release_info = client.release_urls(PACKAGE_NAME, PACKAGE_VERS)
complete_release_information = client.release_data(PACKAGE_NAME, PACKAGE_VERS)
d['meta']['readme'] = complete_release_information['description']

interesting_release = [i for i in release_info if i['packagetype'] == 'sdist']
release_choice = interesting_release[0]
#print release_choice
d['source'] = {
    'archive_url': release_choice['url']
}
d['build'] = {
    'actions': [
        {'mkdir': "$INSTALL_DIR/lib/python"},
        {'shell_command': 'export PYTHONPATH=$PYTHONPATH:$INSTALL_DIR/lib/python\n' + 'python setup.py install --install-lib $INSTALL_DIR/lib/python --install-scripts $INSTALL_DIR/bin'}
    ],
    'env': [
        {'action': 'prepend', 'name': 'PYTHONPATH', 'value': '$INSTALL_DIR/lib/python'},
        {'action': 'prepend', 'name': 'PATH', 'value': '$INSTALL_DIR/bin'},
    ]
}

print yaml.dump(d, default_flow_style=False, width=5000)
