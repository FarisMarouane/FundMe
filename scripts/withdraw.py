import os
from brownie import FundMe, chain, network
from scripts.helpers import create_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS


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
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        fundRaiserAddress = account
    else:
        fundRaiserAddress = (
            os.environ.get("fundRaiserAddress")
            or "0x925c261aD8912bFB8364F352D26887370c21e521"
        )
    withdraw(fundRaiserAddress)
