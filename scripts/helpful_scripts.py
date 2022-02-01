from brownie import accounts, config, interface, network


def fund(nft_contract, amount=1):
    dev = accounts.add(config["wallets"]["from_key"])
    # Get the most recent PriceFeed Object
    networks= config["networks"][network.show_active()]
    link_token = interface.LinkTokenInterface(networks["link_token"])
    link_token.transfer(nft_contract, networks["fee"] * amount, {"from": dev})

# get member of the Straw Hat Pirates
def get_mugiwara(mugiwara_number):
    switch = {
        0:"Luffy", 
        1:"Zoro", 
        2:"Nami", 
        3:"Usopp", 
        4:"Chopper", 
        5:"Sanji", 
        6:"Franky", 
        7:"Brook", 
        8:"Robin", 
        9:"Jinbei"}
    return switch[mugiwara_number]
