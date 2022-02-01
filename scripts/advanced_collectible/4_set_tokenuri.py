from brownie import AdvancedCollectible, network, accounts, config
from scripts.helpful_scripts import get_mugiwara
from metadata import dictionnary_meta
from dotenv import load_dotenv

load_dotenv()

OPENSEA_FORMAT = "https://testnets.opensea.io/assets/{}/{}"


def main():
    print("Working on " + network.show_active())
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
    number_of_tokens = advanced_collectible.tokenCounter()
    print("The number of tokens you've deployed is: " + str(number_of_tokens))
    for token_id in range(number_of_tokens):
        mugiwara = get_mugiwara(advanced_collectible.tokenIdToMugiwara(token_id))
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            print("Setting tokenURI of {}".format(token_id))
            matadata = dictionnary_meta.json_uri
            set_tokenURI(token_id, advanced_collectible, matadata[mugiwara])
        else:
            print("Skipping {}, we already set that tokenURI!".format(token_id))

def set_tokenURI(token_id, nft_contract, tokenURI):
    dev = accounts.add(config["wallets"]["from_key"])
    nft_contract.setTokenURI(token_id, tokenURI, {"from": dev})
    print("Awesome! You can view your NFT at {}".format(OPENSEA_FORMAT.format(nft_contract.address, token_id)))
    print('Please give up to 20 minutes, and hit the "refresh metadata" button')
