#!/usr/bin/env python3
# encoding: utf-8

from seedemu import *
import os 
import platform as sys_platform

emu = Makers.makeEmulatorBaseWith10StubASAndHosts(1)

# Create the Ethereum layer
eth = EthereumService()

# blockchain is a POA based blockchain 
blockchain = eth.createBlockchain(chainName="POA", consensus=ConsensusMechanism.POA)

# Create blockchain nodes (POA Ethereum)
e1 = blockchain.createNode("poa-eth1")
e2 = blockchain.createNode("poa-eth2")
e3 = blockchain.createNode("poa-eth3")
e4 = blockchain.createNode("poa-eth4")
e5 = blockchain.createNode("poa-eth5")

e1.setBootNode(True).unlockAccounts().startMiner()
e1.enableGethWs().setGethWsPort(8541)
e1.enableGethHttp()

e2.importAccount(keyfilePath='./resources/keyfile_to_import', password="admin", balance=10)
e2.unlockAccounts().startMiner()
e3.createAccounts(total=3, balance=30, unit=EthUnit.ETHER, password="admin")
e4.unlockAccounts().startMiner()
e5.setNoDiscover()

emu.getVirtualNode('poa-eth1').setDisplayName('Ethereum-POA-1')
emu.getVirtualNode('poa-eth2').setDisplayName('Ethereum-POA-2')
emu.getVirtualNode('poa-eth3').setDisplayName('Ethereum-POA-3')
emu.getVirtualNode('poa-eth4').setDisplayName('Ethereum-POA-4')
emu.getVirtualNode('poa-eth5').setDisplayName('Ethereum-POA-5')


# Binding virtual nodes to physical nodes
emu.addBinding(Binding('poa-eth1', filter = Filter(asn = 150, nodeName='host_0')))
emu.addBinding(Binding('poa-eth2', filter = Filter(asn = 151, nodeName='host_0')))
emu.addBinding(Binding('poa-eth3', filter = Filter(asn = 152, nodeName='host_0')))
emu.addBinding(Binding('poa-eth4', filter = Filter(asn = 153, nodeName='host_0')))
emu.addBinding(Binding('poa-eth5', filter = Filter(asn = 154, nodeName='host_0')))

faucet:FaucetServer = blockchain.createFaucetServer(vnode='faucet',
                                                    port=80,
                                                    linked_eth_node="poa-eth1",
                                                    balance=1000)

faucet.fund('0x40e38EF94ab2bC9506167D478821ffd55ff2d88d',2)
emu.addBinding(Binding('faucet', filter=Filter(asn=160, nodeName='host_0')))


# Add the layer
emu.addLayer(eth)

emu.render()

platform_env = os.environ.get("platform")

platform_mapping = {
    "amd": Platform.AMD64,
    "arm": Platform.ARM64
}

def detect_platform():
    machine = sys_platform.machine().lower()
    if machine in ("x86_64", "amd64", "i386", "i686", "x86"):
        return Platform.AMD64
    elif machine in ("aarch64", "arm64") or machine.startswith("arm"):
        return Platform.ARM64
    else:
        raise RuntimeError(f"Unsupported platform: {machine}")

if platform_env and platform_env.lower() in platform_mapping:
    detected_platform = platform_mapping[platform_env.lower()]
else:
    detected_platform = detect_platform()

docker = Docker(platform=detected_platform)

emu.compile(docker, './output')
