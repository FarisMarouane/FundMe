from brownie import FundMe, config, network
from scripts.helpers import get_account, deploy_mock

def deploy():
    account = get_account()
    print("Acount", account)

    if network.show_active() != "development":
      print("Active network", network.show_active())
      price_feed = config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
      price_feed = deploy_mock()

    fund_me =  FundMe.deploy(price_feed, { "from": account }, publish_source=True)
    print(fund_me.address)
    return fund_me

def main():
    deploy()