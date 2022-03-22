from brownie import config, accounts
from web3 import Web3


def create_account():
    return accounts.add(config["wallets"]["primary_key"])
