from scripts.utils.helpful_scripts import encode_function_data, get_account
from brownie import BoxV2, ProxyAdmin, TransparentUpgradeableProxy, Contract


def test_proxy_delegate_calls():
    account = get_account()
