from git import Repo
import os
import sys
import subprocess
import warnings

__doc__ = """
Generate DepGen's yaml files from a git repository, without doing any work!
For the repetitive process of porting python modules in github repositories
to toolshed packages, this should make it a breeze!

    python from_git_repo.py <PACKAGE NAME> <REPO URL> > package.yaml

First the tool checks out the repo, inspects it for information, and then
generates a .yaml file for you to use. Please be sure to remove the example
dependency that is added automatically to yaml files.
"""

if len(sys.argv) != 3:
    print "Not enough arguments\n" + __doc__
    sys.exit(1)


REMOTE_REPO = sys.argv[2]
NAME = sys.argv[1]
VERS = "0.0.0"
README = ""
HEAD = "00000000"
ACTIONS = []

try:
    repo = Repo.clone_from(REMOTE_REPO, 'tmp')
except:
    # Probably already cloned
    repo = Repo('tmp')


def sniff_repo_type():
    if os.path.isfile('tmp/setup.py'):
        return 'python'
    else:
        warnings.warn("Unknown repository type. You will need to define actions yourself", RuntimeWarning)


if os.path.isfile('tmp/README.md'):
    # Convert to RST via pandoc
    README = subprocess.check_output(['pandoc', '-t', 'rst', 'tmp/README.md'])
elif os.path.isfile('tmp/README.rst'):
    with open('tmp/README.rst', 'r') as handle:
        README = ''.join(handle.readlines())


HEAD = repo.heads.master.commit.hexsha
import datetime
committed_date = datetime.datetime.fromtimestamp(repo.heads.master.commit.committed_date)
VERS = committed_date.strftime('%Y.%m.%d')


repo_type = sniff_repo_type()
if repo_type == 'python':
    ACTIONS = [
        {'mkdir': '$INSTALL_DIR/lib/python'},
        {'shell_command': 'export PYTHONPATH=$PYTHONPATH:$INSTALL_DIR/lib/python\n' +
            'python setup.py install --install-lib $INSTALL_DIR/lib/python --install-scripts $INSTALL_DIR/bin'},
    ]


data = {
    'meta': {
        'name': NAME,
        'vers': VERS,
        'readme': README,
    },
    'source': {
        'git_repo': {
            'url': REMOTE_REPO,
            'rev': HEAD,
        }
    },
    'build': {
        'actions': ACTIONS
    },
    'depends': [
        {'repo_name': 'package_example_1_0', 'repo_owner': 'iuc', 'repo_rev':
         '0f9f634dec8a', 'name': 'example', 'vers': '1.0', 'build_req':
         'True'}
    ]
}

import yaml
print yaml.dump(data, default_flow_style=False, width=5000)
# Clean up after ourselves
subprocess.check_output(['rm', '-rf', 'tmp'])
