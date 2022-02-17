from brownie import MockV3Aggregator, network, config, accounts
from web3 import Web3

LOCAL_DEVELOPMENT_CHAINS = ["development", "ganache-local"]


def get_account():
    if network.show_active() in LOCAL_DEVELOPMENT_CHAINS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["primary_key"])


def deploy_mock():
    if len(MockV3Aggregator) > 0:
        mock_aggregator = MockV3Aggregator[-1]
    else:
        mock_aggregator = MockV3Aggregator.deploy(
            18, Web3.toWei(2000, "ether"), {"from": get_account()}
        )

    return mock_aggregator.address
