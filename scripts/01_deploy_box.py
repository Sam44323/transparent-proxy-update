from brownie import Box, network
from scripts.utils.helpful_scripts import get_account


def main():
    account = get_account()
    print(f"Deploying to network {network.show_active()}")
    box = Box.deploy({"from": account})
    print(box.retreive())
