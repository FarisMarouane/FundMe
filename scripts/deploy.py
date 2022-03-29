import os
from brownie import FundMe, MockV3Aggregator, config, network, chain
from scripts.helpers import create_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS, deploy_mocks


def deploy(compaignDuration, fundRaiserAddress):

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed = config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        deploy_mocks()
        price_feed = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed,
        compaignDuration,
        {"from": fundRaiserAddress},
        publish_source=config["networks"][network.show_active()]["verify"],
    )

    print("fund_me contract", fund_me)
    return


def withdraw(fundRaiserAddress):
    fund_me = FundMe[-1]
    while True:
        if (
            chain.time() - fund_me.fundRaiseCreationTime() > fund_me.lockPeriod() * 60
        ):  # Nb of minutes * 60 sec
            print("chain.time***", chain.time())
            print("fund_me.fundRaiseCreationTime***", fund_me.fundRaiseCreationTime())
            print("lockPeriod***", fund_me.lockPeriod())
            fund_me.withdraw({"from": fundRaiserAddress})
            break


def main():
    account = create_account()
    compaignDuration = os.environ.get("duration") or 2
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        fundRaiserAddress = account
    else:
        fundRaiserAddress = os.environ.get("fundRaiserAddress")

    deploy(compaignDuration, fundRaiserAddress)
    withdraw(fundRaiserAddress)
