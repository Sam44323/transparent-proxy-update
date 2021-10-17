from brownie import Box, ProxyAdmin, TransparentUpgradeableProxy, network, Contract
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

    # assigning the Box ABI to proxy contract so that it can delegate to the box contract once called instead of throwing an error(which is a default usecase when you assign an ABI to a contract that doesn't contain any functions related to the abi)

    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    print(proxy_box.retreive())
