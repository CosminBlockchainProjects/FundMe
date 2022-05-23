from brownie import FundMe, network, config, MockV3Aggregator
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIROMENTS,
)
from web3 import Web3


def deploy_fund_me():
    account = get_account()
    # We would like to publish our source code, verified by Etherscan
    # Pass the price feed address to our fundme contract
    # If we are on a persistent network like Rinkey, use the associated address, otherwise deploy mocks
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    # Contract deployed to 0x44b175Dac0f1D714D252e7c9eb9172ee2DDdD501
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
