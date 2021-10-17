from brownie import Box, ProxyAdmin, TransparentUpgradeableProxy, network
from scripts.utils.helpful_scripts import encode_function_data, get_account


def main():
    account = get_account()
    print(f"Deploying to network {network.show_active()}")
    box = Box.deploy({"from": account})  # the Box implementation contract
    print(box.retreive())

    proxy_admin = ProxyAdmin.deploy({"from": account})
    # hooking up an implementation contract to a proxy

    # as of now we are not using any initializer function. See the definition for encode_function_data in the helpful scripts
    box_encoded_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address, proxy_admin.address, box_encoded_initializer_function, {"from": account, "gas_limit": 1000000})

    print(f"Proxy upload to {proxy}, you can now update to v2!")
