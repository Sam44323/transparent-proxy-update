from brownie import Box, ProxyAdmin, network
from scripts.utils.helpful_scripts import get_account


def main():
    account = get_account()
    print(f"Deploying to network {network.show_active()}")
    box = Box.deploy({"from": account})  # the starting implementation contract
    print(box.retreive())

    # hooking up an implementation contract to a proxy
    proxy_admin = ProxyAdmin.deploy({"from": account})
