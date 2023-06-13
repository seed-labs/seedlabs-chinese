#!/usr/bin/env python3
# encoding: utf-8

from seedemu import *
import os, sys

###############################################################################
emu = Emulator()

# Load the pre-built components and merge them
emu.load('./base-component.bin')


hosts_total = 2  # Each AS has 3 hosts.

###############################################################################
# Create the Ethereum layer

eth = EthereumService()
blockchain = eth.createBlockchain(chainName="POA", consensus=ConsensusMechanism.POA)
#blockchain.setGasLimitPerBlock(127000)

asns = [150, 151, 152, 153, 154, 160, 161, 162, 163, 164]
signers = []
i = 0
for asn in asns:
    for id in range(hosts_total):
        vnode = 'eth{}'.format(i)
        e = blockchain.createNode(vnode)

        displayName = 'Ethereum-POA-%.2d'
        e.enableGethHttp()  # Enable HTTP on all nodes
        e.unlockAccounts()
        if i%2  == 0:
            e.startMiner()
            signers.append(vnode)
            e.createAccount(balance= 99 * pow(10,5), password="admin")
            displayName = displayName + '-Signer'
            emu.getVirtualNode(vnode).appendClassName("Signer")
        if i%3 == 0:
            e.setBootNode(True)
            displayName = displayName + '-BootNode'
            emu.getVirtualNode(vnode).appendClassName("BootNode")

        emu.getVirtualNode(vnode).setDisplayName(displayName%(i))
        emu.addBinding(Binding(vnode, filter=Filter(asn=asn, nodeName='host_{}'.format(id))))
        i = i+1



#############################
emu.addLayer(eth)
emu.render()

docker = Docker(internetMapEnabled=True, etherViewEnabled=True)
emu.compile(docker, './emulators/emulator-poa', override = True)

