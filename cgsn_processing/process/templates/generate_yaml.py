#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package cgsn_processing.process.templates.generate_yaml
@file cgsn_processing/process/templates/generate_yaml.py
@author Christopher Wingard
@brief Generate a YAML file from a Jinja2 template file and a set of keyword
    arguments to populate the template with mooring and deployment specific
    configuration information.
"""
import argparse
import netrc
import os
import requests
import sys
import yaml

from jinja2 import Environment, FileSystemLoader
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

# load the access credentials from the .netrc file and set the RDB API token
RDB_HOST = "ooi-rdb.whoi.edu"
try:
    nrc = netrc.netrc()
    AUTH = nrc.authenticators(RDB_HOST)
    if AUTH is None:
        raise RuntimeError(f'No entry found for machine {RDB_HOST} in the .netrc file')
except FileNotFoundError as e:
    raise OSError(e, os.strerror(e.errno), os.path.expanduser('~'))
API_TOKEN = f"Token {AUTH[2]}"

# set up and configure the requests session object (used for all requests)
SESSION = requests.Session()
retry = Retry(connect=5, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
SESSION.mount('https://', adapter)
SESSION.trust_env = False


class YamlDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(YamlDumper, self).increase_indent(flow, False)


def request_url(url):
    print(f'requesting {url}')
    return SESSION.get(url, headers={"Authorization": API_TOKEN}).json()


def request_endpoint(endpoint):
    url = f'https://{RDB_HOST}/api/v1/{endpoint}'
    return request_url(url)


def inputs(args=None):
    """
    Command line argument parser for the mooring name, deployment name (e.g.
    D00021) and template file. All three inputs are required and the deployment
    name must be a string following the common formats used with the MIOs (e.g.
    'D0001' or 'R00021'). The number of leading zeros does not matter.
    Additionally, the template file (jinja2) may be provided as an absolute or
    relative file path.
    """
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(description='Construct a deployment configuration record by pulling data '
                                                 'from the OOI RDB system and populating a Jinja2 template file.')
    parser.add_argument('mooring', '--mooring', type=str, help='The mooring name', required=True)
    parser.add_argument('deployment', '--deploy', type=str, help='The deployment number to process', required=True)
    parser.add_argument('template', '--template', type=str, help='The template file to use', required=True)
    parser.add_argument('outfile', '--outfile', type=str, help='The output file to write the configuration to',
                        required=True)

    # parse the input arguments and create a parser object
    return parser.parse_args(args)


def build_configuration(mooring, deployment_name, template):
    """
    Construct the deployment configuration record by pulling data from the OOI
    RDB system and populating a Jinja2 template file.

    :param mooring: str, the mooring name
    :param deployment_name: str, the deployment number to process
    :param template: str, the template file to use
    """
    # construct the deployment number and the deployment url from the deployment name
    deployment = int(''.join([s for s in deployment_name if s.isdigit()]))
    deployment_number = f'{mooring.upper()}-{deployment:05d}'
    deployment_url = request_endpoint(f'deployments/?deployment_number={deployment_number}&fields=url')[0]['url']

    # download the build record for a specific site-deployment and assemble a list of the deployed inventory
    build = request_url(deployment_url)
    # inventory = build['inventory_deployments']

    # pull out relevant deployment metadata from the build record
    integration_start = build['deployment_start_date']
    burn_in_start = build['deployment_burnin_date']
    deployment_start = build['deployment_to_field_date']
    deployment_end = build['deployment_recovery_date']
    latitude = build['latitude']
    longitude = build['longitude']
    site_depth = build['depth']

    # pull out the cruise numbers for the deployment and recovery cruises
    if build['cruise_deployed']:
        cruise = request_url(build['cruise_deployed'])
        deployment_cruise = cruise['CUID']
    else:
        deployment_cruise = None

    if build['cruise_recovered']:
        cruise = request_url(build['cruise_recovered'])
        recovery_cruise = cruise['CUID']
    else:
        recovery_cruise = None

    # set the disposition of the deployment based on burn-in, deployment, and recovery dates
    disposition = 'UNKNOWN_DISPOSITION'
    if integration_start is not None:
        disposition = 'burn-in'
    if burn_in_start is not None:
        disposition = 'burn-in'
    if deployment_start is not None:
        disposition = 'deployed'
    if deployment_end is not None:
        disposition = 'recovered'

    # index through the inventory items to develop a listing of the deployed assets used in the deployment
    # assets = [request_url(f'{url}?expand=part,assembly_parts') for url in inventory]

    # TODO: for each inventory item, pull out the configuration values
    # these will be in a list obtained by making the request for the deployment specific build
    # for each item, 1 or more requests will be needed to get the configuration values using different urls and
    # options. Will want to filter on part names, serial numbers, and maybe the friendly name?

    # construct the context dictionary to pass to the template
    context = {
        'mooring': mooring,
        'deployment': deployment,
        'deployment_name': deployment_name,
        'disposition': disposition,
        'deployment_start': deployment_start,
        'latitude': latitude,
        'longitude': longitude,
        'site_depth': site_depth,
        'deployment_cruise': deployment_cruise,
        'recovery_cruise': recovery_cruise,
        'deployment_end': deployment_end,
    }

    # load the template from the yaml template file (skipping the first line)
    env = Environment(loader=FileSystemLoader(os.path.dirname(template)))
    template = env.get_template(os.path.basename(template))
    config = yaml.safe_load(template.render(**context))
    return config


def main(argv=None):
    """
    Main function to parse the command line arguments, request the deployment
    information from the OOI RDB system, and generate a YAML file using the
    Jinja2 template file and the deployment information.
    """
    # Parse the command line arguments
    args = inputs(argv)
    mooring = args.mooring
    deployment_name = args.deployment
    template_file = os.path.abspath(args.template)
    outfile = os.path.abspath(args.outfile)

    config = build_configuration(mooring, deployment_name, template_file)
    with open(outfile, 'w') as f:
        yaml.dump(config,  f, Dumper=YamlDumper, default_flow_style=False, sort_keys=False)


if __name__ == '__main__':
    main()
