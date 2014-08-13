#!/usr/bin/env python
import xml.etree.ElementTree as ET
import sys
import warnings
import glob

ROOT_WORKFLOW = sys.argv[1]
tree = ET.parse(ROOT_WORKFLOW)
root = tree.getroot()


class GalaxyWorkflow(object):

    def __init__(self, workflow_name, workflow_annotation):
        self.data = {
            'a_galaxy_workflow': 'true',
            'annotation': workflow_annotation,
            'format-version': '0.1',
            'name': workflow_name,
            'steps': {}
        }
        self.id_num = 0

    def add_step(self, annotation, input_connections, inputs, name, outputs,
                 tool_id):
        # Grab a copy
        local_id = self.id_num + 0
        # Increment our step ID number counter
        self.id_num += 1
        self.data['steps'][str(local_id)] = {
            'annotation': annotation,
            'id': local_id,
            'input_connections': input_connections,
            'inputs': inputs,
            'name': name,
            'outputs': outputs,
            # TODO: auto layout, force directed.
            'position': {
                'left': 0,
                'top': 0
            },
            'post_job_actions': {},
            'tool_errors': None,
            'tool_id': tool_id,
        }
        return local_id


workflow_id = root[0].attrib['id']
workflow_version = root[0].attrib['version']


def identify_steps(root_node):
    # Track which params are module stages and require further parsing
    modulestages = []
    for child in root_node[1:]:
        modulestages.append(child.attrib['name'])

    steps = []
    name = ''
    annotation = ''
    for child in root_node[0]:
        if child.tag == 'param':
            if child.attrib['name'] == 'name':
                name = child.find('value').text
            elif child.attrib['name'] == 'description':
                annotation = child.find('value').text
            elif child.attrib['name'] in modulestages:
                # This module is used in processing
                for sub_step in child.findall('value'):
                    steps.append(sub_step.text)
                additional_steps = child.find('select')
                if child.find('select') is not None:
                    if 'multiple' in additional_steps.attrib:
                        multiple_allowed = additional_steps.attrib['multiple'] == 'true'
                    else:
                        multiple_allowed = False
                    directory = additional_steps.find('import')
                    if directory is not None and directory.attrib['contentType'] == 'text/directory':
                        extra_possible_steps = glob.glob("%s/*" % directory.text)
                        steps.append({
                            'multiple_allowed': multiple_allowed,
                            'choices': extra_possible_steps
                        })
                    else:
                        warnings.warn("Found a select but couldn't access the import")
    return (steps, name, annotation)


def parse_workflow_step(xml_file):
    wf_tree = ET.parse(xml_file)
    wf_root = wf_tree.getroot()


(steps, name, annotation) = identify_steps(root)
for step in steps:
    if isinstance(step, dict):
        pass
    else:
        parse_workflow_step(step)
