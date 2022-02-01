from brownie import AdvancedCollectible, accounts, config
from scripts.helpful_scripts import get_mugiwara, fund
import time

STATIC_SEED = 123


def main():
    dev = accounts.add(config['wallets']['from_key'])
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
    fund(advanced_collectible.address)
    transaction = advanced_collectible.createCollectible(STATIC_SEED, "None", {"from": dev})
    print("Waiting on second transaction...")
    # wait for the 2nd transaction
    transaction.wait(1)
    request_id = transaction.events["RequestedCollectible"]["requestId"]
    token_id = advanced_collectible.requestIdToTokenId(request_id)
    time.sleep(60)

    mugiwara = get_mugiwara(advanced_collectible.tokenIdToMugiwara(token_id))

    print("Mugiwara of tokenId {} is {}".format(token_id, mugiwara))
