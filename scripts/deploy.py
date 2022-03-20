import os

from brownie import FundMe, config, network, chain
from scripts.helpers import get_account, deploy_mock, LOCAL_DEVELOPMENT_CHAINS


def deploy():
    account = get_account()
    compaignDuration = os.environ.get("duration") or 5
    fundRaiserAddress = os.environ.get("fundRaiserAddress")

    if network.show_active() not in LOCAL_DEVELOPMENT_CHAINS:
        print("Active network", network.show_active())
        price_feed = config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        price_feed = deploy_mock()

    fund_me = FundMe.deploy(
        price_feed,
        compaignDuration,
        {"from": fundRaiserAddress},
        publish_source=config["networks"][network.show_active()]["verify"],
    )

    print("fund_me contract", fund_me)

    return fund_me


def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    while True:
        if (
            chain.time() - fund_me.fundRaiseCreationTime() > fund_me.lockPeriod() * 60
        ):  # Nb of minutes * 60 sec
            print("Account", account)
            print("chain.time", chain.time())
            print("fund_me.fundRaiseCreationTime", fund_me.fundRaiseCreationTime())
            fund_me.withdraw({"from": account})
            break


def main():
    deploy()
    # withdraw()
