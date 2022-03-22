import os

from brownie import FundMe, config, network, chain
from scripts.helpers import create_account


def deploy():
    create_account()
    compaignDuration = os.environ.get("duration") or 5
    fundRaiserAddress = os.environ.get("fundRaiserAddress")
    price_feed = config["networks"][network.show_active()]["eth_usd_price_feed"]

    print("fundRaiserAddress***", fundRaiserAddress)

    fund_me = FundMe.deploy(
        price_feed,
        compaignDuration,
        {"from": fundRaiserAddress},
        publish_source=config["networks"][network.show_active()]["verify"],
    )

    print("fund_me contract", fund_me)

    return fund_me


def withdraw(contract):
    fund_me = FundMe[-1]
    while True:
        if (
            chain.time() - fund_me.fundRaiseCreationTime() > fund_me.lockPeriod() * 60
        ):  # Nb of minutes * 60 sec
            print("chain.time", chain.time())
            print("fund_me.fundRaiseCreationTime", fund_me.fundRaiseCreationTime())
            fund_me.withdraw({"from": contract})
            break


def main():
    contract = deploy()
    # withdraw(contract)
