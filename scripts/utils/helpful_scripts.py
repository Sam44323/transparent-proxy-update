from brownie import accounts, network, config
import eth_utils

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["hardhat",
                                 "development", "ganache", "mainnet-fork"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id)
    return accounts.add(config["wallets"]["from_key"])

# encoding the initializer function into bytes so that our proxy smart contract knows what function to call when initiated


def encode_function_data(initializer=None, *args):
    """Encodes the function call so we can work with an initializer.
    Args:
        initializer ([brownie.network.contract.ContractTx], optional):
        The initializer function we want to call. Example: `box.store`.
        Defaults to None.
        args (Any, optional):
        The arguments to pass to the initializer function
    Returns:
        [bytes]: Return the encoded bytes.
    """
    if len(args) == 0 or not initializer:
        # if no initializer or args is blank, we return an empty hex string
        return eth_utils.to_bytes(hexstr="0x")
    return initializer.encode_input(*args)


def upgrade(account, proxy, new_implementation_address, proxy_admin_contract=None, initializer=None, *args):
    transaction = None
    if proxy_admin_contract:
        if initializer:
            encode_function_call = encode_function_data(initializer, *args)
            transaction = proxy_admin_contract.upgradeAndCall(
                proxy.address, new_implementation_address, encode_function_call, {"from": account})
        else:
            transaction = proxy_admin_contract.update(
                proxy.address, new_implementation_address, {"from": account})
    else:
        if initializer:
            encode_function_call = encode_function_data(initializer, *args)
            # if no admin, then upgrade the implementation directly from the proxy itself
            transaction = proxy.upgradeToAndCall(
                new_implementation_address, encode_function_call, {"from": account})
        else:
            transaction = proxy_admin_contract.update(
                new_implementation_address, {"from": account})
    return transaction
