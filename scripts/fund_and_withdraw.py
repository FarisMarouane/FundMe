from brownie import FundMe
from scripts.helpers import get_account

def fund():
  fund_me = FundMe[-1]
  account = get_account()
  entrance_fee = fund_me.getEntranceFee()
  print("Entrance fee", entrance_fee)
  fund_me.fund({ 'from': account, 'value': entrance_fee * 5 })

def withdraw():
  fund_me = FundMe[-1]
  account = get_account()
  fund_me.withdraw({ 'from': account })


def main():
#   fund()
  withdraw()