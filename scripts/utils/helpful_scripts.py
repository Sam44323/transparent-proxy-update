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
