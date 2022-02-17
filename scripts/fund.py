from brownie import FundMe
from scripts.helpers import get_account


def fund():
    fund_me = FundMe[-1]
    account = get_account()
    print("Funder's account ***", account)
    entrance_fee = fund_me.getEntranceFee()
    fund_me.fund({"from": account, "value": entrance_fee})


def main():
    fund()
