#!/usr/bin/env python3
# encoding: utf-8
# Copy the key files from each geth node to the keystore folder

from web3 import Web3
import docker
import os, subprocess, json

NAME_PATTERN = 'Ethereum-POA'
DIR_NAME = "emulator_info"
client = docker.from_env()
all_containers = client.containers.list()

mapping_all = {}


os.system("mkdir -p {}".format(DIR_NAME))
for container in all_containers:
  if NAME_PATTERN in container.name:
      print("Get information from {}".format(container.name))
      cmd = ['docker', 'inspect', "--format='{{json .Config.Labels}}'", container.short_id]
      # remove the training space, and the leading/trailing single quote 
      info = subprocess.check_output(cmd).decode("utf-8").rstrip().rstrip("'").lstrip("'")
      info_json = json.loads(info)
      info_map = {}
      info_map["container_id"] = container.short_id
      info_map["displayname"] = info_json["org.seedsecuritylabs.seedemu.meta.displayname"] 
      ip = info_json["org.seedsecuritylabs.seedemu.meta.net.0.address"] 
      info_map["ip"] = ip.replace("/24", "") # remove the network mask
      info_map["node_id"] = info_json["org.seedsecuritylabs.seedemu.meta.ethereum.node_id"]
      info_map["chain_id"] = info_json["org.seedsecuritylabs.seedemu.meta.ethereum.chain_id"]

      mapping_all[container.name] = info_map

#print(json.dumps(mapping_all, indent=4))

filename = "{}/_index.json".format(DIR_NAME)
with open(filename, 'w') as json_file:
  json.dump(mapping_all, json_file, indent = 4)
