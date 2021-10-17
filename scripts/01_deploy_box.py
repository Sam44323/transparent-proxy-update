from brownie import Box, ProxyAdmin, network
from scripts.utils.helpful_scripts import get_account


def main():
    account = get_account()
    print(f"Deploying to network {network.show_active()}")
    box = Box.deploy({"from": account})  # the Box implementation contract
    print(box.retreive())

    proxy_admin = ProxyAdmin.deploy({"from": account})
    # hooking up an implementation contract to a proxy

    # encoding the initializer function of the implementation contract
    initializer = box.store, 1
