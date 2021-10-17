from brownie import Box, BoxV2, ProxyAdmin, TransparentUpgradeableProxy, network, Contract
from scripts.utils.helpful_scripts import encode_function_data, get_account, upgrade


def main():
    account = get_account()
    print(f"Deploying to {network.show_active()}")
    box = Box.deploy(
        {"from": account},
        publish_source=True,
    )  # the Box implementation contract

    # Optional, deploy the ProxyAdmin and use that as the admin contract
    proxy_admin = ProxyAdmin.deploy(
        {"from": account},
        publish_source=True
    )

    proxy_admin = ProxyAdmin.deploy(
        {"from": account}, publish_source=True)
    # hooking up an implementation contract to a proxy

    # as of now we are not using any initializer function. See the definition for encode_function_data in the helpful scripts
    box_encoded_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address, proxy_admin.address, box_encoded_initializer_function, {"from": account}, publish_source=True)

    print(f"Proxy upload to {proxy}, you can now update to v2!")

    # assigning the Box ABI to proxy contract so that it can delegate to the box contract once called instead of throwing an error(which is a default usecase when you assign an ABI to a contract that doesn't contain any functions related to the abi)

    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    print(proxy_box.retrieve({"from": account}))

    # upgrading the implementation contract
    box_v2 = BoxV2.deploy({"from": account}, publish_source=True)
    upgrade_transaction = upgrade(
        account, proxy, box_v2.address, proxy_admin)
    upgrade_transaction.wait(1)
    print("Proxy has been updated!")
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    proxy_box.increment({"from": account})
    print(proxy_box.retreive({"from": account}))
