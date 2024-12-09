#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.templates.generate_yaml
"""
import os
import json
import yaml

from jinja2 import Environment, BaseLoader, TemplateNotFound
from typing import Any, IO


class TemplateLoader(BaseLoader):
    """
    Jinja2 template loader for loading templates, skipping the first line,
    which uses an '!include' statement to  utilize values found in other yaml
    files. Built off the Jinja2 BaseLoader class per the Jinja2 documentation.
    """
    def __init__(self, path):
        self.path = path

    def get_source(self, environment, template):
        path = os.path.join(self.path, template)
        if not os.path.exists(path):
            raise TemplateNotFound(template)
        with open(path) as f:
            lines = f.readlines()
            source = '\n'.join(lines[1:])  # Skip the first line

        return source, path


class YamlLoader(yaml.SafeLoader):
    """
    YAML Loader with to use with the `!include` constructor defined below.
    """
    def __init__(self, stream: IO) -> None:
        try:
            self._root = os.path.split(stream.name)[0]
        except AttributeError:
            self._root = os.path.curdir

        super().__init__(stream)

    @property
    def root(self):
        return self._root


def construct_include(loader: YamlLoader, node: yaml.ScalarNode) -> Any:
    """
    Include file referenced at node
    """
    filename = os.path.abspath(os.path.join(loader.root, loader.construct_scalar(node)))
    extension = os.path.splitext(filename)[1].lstrip('.')

    with open(filename, 'r') as f:
        if extension in ('yaml', 'yml'):
            return yaml.load(f, YamlLoader)
        elif extension in ('json', ):
            return json.load(f)
        else:
            return ''.join(f.readlines())


def populate_template(template_file: str, output_file: str, **kwargs) -> None:
    """
    Populate a Jinja2 template with the given keyword arguments and write the
    output to a file.

    Args:
        template_file: Path to the Jinja2 template file (formatted as yaml).
        output_file: Path to the output file.
        **kwargs: Keyword arguments to pass to the Jinja2 template.
    """
    # load the yaml template file and add the config values from the included file
    YamlLoader.add_constructor('!include', construct_include)
    with open(template_file, 'r') as f:
        data = yaml.load(f, YamlLoader)

    # load the template from the yaml template file (skipping the first line)
    env = Environment(loader=TemplateLoader(os.path.dirname(template_file)), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(os.path.basename(template_file))

    # Render the template with the given keyword arguments
    config = yaml.safe_load(template.render(**data, **kwargs))

    # Write the output to a file
    yaml.SafeDumper.ignore_aliases = lambda *args: True
    with open(output_file, 'w') as f:
        yaml.safe_dump(config, f, sort_keys=False, default_flow_style=False)


def main():
    YamlLoader.add_constructor('!include', construct_include)

    # Load the yaml template file and add the config values from the included file
    YAML_FILE = os.path.abspath('cgsn_processing\\process\\templates\\cp10cnsm_oms_template.yaml')
    with open(YAML_FILE, 'r') as f:
        data = yaml.load(f, YamlLoader)

    env = Environment(loader=TemplateLoader(os.path.dirname(YAML_FILE)), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(os.path.basename(YAML_FILE))

    config = yaml.safe_load(template.render(**data))
    print(config)


if __name__ == '__main__':
    main()
