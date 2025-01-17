#!/usr/bin/env python
# -*- coding: utf-8 -*-
import netrc
import os
import re
import requests

from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from cgsn_processing.process.templates.keys import *

# load the access credentials
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


class Build(object):
    def __init__(self, deployment_number):
        self.assembly_parts = {}
        self.ancestors = {}
        record = request_endpoint(f'deployments/?deployment_number={deployment_number}')[0]
        assembly_part_records = record[ASSEMBLY_PARTS]
        for assembly_part_record in assembly_part_records:
            assembly_part = AssemblyPart(assembly_part_record)
            self.assembly_parts[assembly_part.url] = assembly_part
            assembly_part.walk_parent(self.ancestors)


class AssemblyPart(object):
    def __init__(self, record):
        self.url = record[ASSEMBLY_PART_URL]
        self.name = record[PART_NAME]
        # populate configuration values
        config_values_list = record[CONFIGURATION_VALUES]
        config_values = {}
        for cv in config_values_list:
            config_values[cv['name']] = cv['value']
        self.config = config_values
        self.component_name = self.config.get(COMPONENT_NAME)
        self.parent_cpu = self.config.get(PARENT_CPU)
        self.instance_on_subassembly = self.config.get(INSTANCE_ON_SUBASSEMBLY)
        self.data_source_log_identifier = self.config.get(DATA_SOURCE_LOG_IDENTIFIER)
        self.component_basename = component_basename(self.component_name)
        # parent (does not fetch)
        self.parent = None
        self.parent_url = record[PARENT_ASSEMBLY_PART_URL]

    @property
    def is_cpu(self):
        return self.component_basename in CPUS

    def walk_parent(self, cache):
        if self.parent_url not in cache:
            part = Part(self.parent_url)
            cache[self.parent_url] = part
        else:
            part = cache[self.parent_url]
        self.parent = part
        part.walk_ancestors(cache)

    @property
    def subassembly(self):
        parent = self.parent
        while parent is not None:
            if parent.parent is None:
                return parent
            parent = parent.parent
        # unreachable

    def __str__(self):
        return f'{self.name} ({self.component_name})'


class Part(object):
    def __init__(self, url):
        expanded_url = f'{url}?expand=config_default_events.config_defaults.config_name'
        record = request_url(url)
        self.url = url
        self.parent_url = record.get(PARENT)
        self.parent = None
        self.name = record[PART_NAME]
        self.config = {}

    def walk_ancestors(self, cache):
        if self.parent_url is not None:
            if self.parent_url not in cache:
                self.parent = Part(self.parent_url)
                cache[self.parent_url] = self.parent
            else:
                self.parent = cache[self.parent_url]
            self.parent.walk_ancestors(cache)

    @property
    def subassembly_component_name(self):
        name = self.name.lower()
        for sa_name in SUBASSEMBLIES:
            if sa_name in name:
                return sa_name

    def __str__(self):
        return self.name


def request_url(url):
    print(f'requesting {url}')
    return SESSION.get(url, headers={"Authorization": API_TOKEN}).json()


def request_endpoint(endpoint):
    url = f'https://{RDB_HOST}/api/v1/{endpoint}'
    return request_url(url)


def component_basename(component_name):
    # remove trailing numbers from component names as appropriate
    if component_name is None:
        return ''
    return re.sub(r'[0-9]+$', '', component_name)
    # FIXME add support for 3dmgx3, fb250


def main():
    # download the build record for a specific site-deployment and assemble a list of the deployed inventory
    deployment = 1
    deploy_name = deployment_number = f'CP10CNSM-{deployment:05d}'
    deployment_url = request_endpoint(f'deployments/?deployment_number={deployment_number}&fields=url')[0]['url']
    build = request_url(deployment_url)
    inventory = build['inventory_deployments']

    # pull out relevant deployment metadata from the build record
    integration_start = build['deployment_start_date']
    burn_in_start = build['deployment_burnin_date']
    deployment_start = build['deployment_to_field_date']
    deployment_end = build['deployment_recovery_date']
    latitude = build['latitude']
    longitude = build['longitude']

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
    if burn_in_start is not None:
        disposition = 'burn-in'
    if deployment_start is not None:
        disposition = 'deployed'
    if deployment_end is not None:
        disposition = 'recovered'

    # indexing through the inventory items to develop a listing of the deployed assets
    assets = [request_url(f'{url}?expand=part,assembly_parts') for url in inventory]


if __name__ == '__main__':
    main()

    # TODO: first step is to get the deployment URL for a specific site-deployment
    # e.g. https://ooi-rdb.whoi.edu/api/v1/deployments/?deployment_number=CP10CNSM-00001&fields=url
    # TODO: second step is to pull out the metadata (dates, lat, lon, depth) for each deployment
    # these values would come from the response body, although a separate request will be needed for the cruise metadata
    # TODO: third step is to pull out the inventory items for each deployment
    # these will be in a list obtained by making a request for the build associated with the deployment
    # TODO: for each inventory item, pull out the configuration values
    # these will be in a list obtained by making the request for the deployment specific build
    # for each item, 1 or more requests will be needed to get the configuration values using different urls and
    # options. Will want to filter on part names, serial numbers, and maybe the friendly name?
