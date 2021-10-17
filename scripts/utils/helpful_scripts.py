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
    if len(args) == 0 or not initializer:
        # if no initializer or args is blank, we return an empty hex string
        return eth_utils.to_bytes(hexstr="0x")
    return initializer.encode_input(*args)
