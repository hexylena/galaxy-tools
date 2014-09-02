#!/usr/bin/env python
import xml.etree.ElementTree as ET
import sys
import warnings
import glob
import os
import subprocess

MODULE_ID = sys.argv[1]
module_xml_files = subprocess.check_output(["grep", '-Rl', 'id="%s"' % MODULE_ID, 'common/'])
"""
So here's the theory:

Their XML files of a given module id all cover different invocations of the same tool. Thus we can use this to collect a "complete" version of all parameters available to a tool, as well as "individualized" versions of the tool in order to accomodate special needs.

"""

complete_parameter_list = {}
local_parameter_list = {}


class Parameter(object):

    def __init__(self, node):
        self.name = node.attrib['name']
        if 'hidden' in node.attrib:
            self.hidden = node.attrib['hidden']

    def update(self, other_param):
        pass


class GalaxyTool(object):

    def __init__(self, path, parameter_list):
        self.params = parameter_list
        self.path = path

    def generate_xml(self):
        print self.path
        return ""

for xml_file in module_xml_files.strip().split('\n'):
    tree = ET.parse(xml_file)
    local_parameter_list[xml_file] = {}
    root = tree.getroot()
    print "Parsing %s" % xml_file
    label = root[0].attrib['label']
    for param in root[0].findall('param'):
        parsed_param = Parameter(param)
        if parsed_param.name in complete_parameter_list:
            param_to_update = complete_parameter_list[parsed_param.name]
            param_to_update.update(parsed_param)
            complete_parameter_list[parsed_param.name] = param_to_update
        else:
            complete_parameter_list[parsed_param.name] = parsed_param
        local_parameter_list[xml_file][parsed_param.name] = parsed_param
    #with open(xml_file.replace('/', '.') + '.xml', 'w') as handle:
    passed_params = local_parameter_list[xml_file].values
    galaxy_tool = GalaxyTool(xml_file, passed_params)
    galaxy_tool.generate_xml()
        #handle.write(galaxy_tool.generate_xml())

#import pprint
#pprint.pprint(local_parameter_list)
