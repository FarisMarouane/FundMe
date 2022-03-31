import os
from brownie import FundMe, MockV3Aggregator, config, network
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


def main():
    account = create_account()
    compaignDuration = os.environ.get("duration") or 2
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        fundRaiserAddress = account
    else:
        fundRaiserAddress = (
            os.environ.get("fundRaiserAddress")
            or "0x925c261aD8912bFB8364F352D26887370c21e521"
        )

    deploy(compaignDuration, fundRaiserAddress)
