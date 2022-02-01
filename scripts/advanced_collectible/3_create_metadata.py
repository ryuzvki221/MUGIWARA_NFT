#!/usr/bin/python3
import os
import requests
import json
from brownie import AdvancedCollectible, network
from metadata import sample_metadata, image_meta, attribute
from scripts.helpful_scripts import get_mugiwara
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

IPFS_URI = "https://ipfs.io/ipfs/{}"

def main():
    print("Working on "+network.show_active())
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
    number_of_tokens = advanced_collectible.tokenCounter()
    print("The number of tokens you've deployed is: "+str(number_of_tokens))
    write_metadata(number_of_tokens, advanced_collectible)

def write_metadata(number_of_tokens, nft_contract):
    for token_id in range(number_of_tokens):
        collectible_metadata = sample_metadata.metadata_template
        mugiwara = get_mugiwara(nft_contract.tokenIdToMugiwara(token_id))
        metadata_file_name = (mugiwara.lower().replace('_', '-')+ ".json")
        # metadata/rinkeby/luffy.json
        if Path(metadata_file_name).exists():
            print("{} already found, delete it to overwrite!".format(metadata_file_name))
        else:
            print("Creating Metadata file: " + metadata_file_name)

            # Directory
            directory = "{}/".format(network.show_active())
  
            # Parent Directory path
            parent_dir = "./metadata/"
  
            # Path
            path = os.path.join(parent_dir, directory)

            # Name
            collectible_metadata["name"] = get_mugiwara(nft_contract.tokenIdToMugiwara(token_id))
            # Description
            collectible_metadata["description"] = "{} of the Straw Hat Pirates.".format(collectible_metadata["name"])
            # Value of attribute
            collectible_metadata["attributes"][0]["value"] = attribute.mugiwara_to_epithet[mugiwara]
            collectible_metadata["attributes"][1]["value"] = attribute.mugiwara_to_birthday[mugiwara]
            collectible_metadata["attributes"][2]["value"] = attribute.mugiwara_to_origin[mugiwara]
            collectible_metadata["attributes"][3]["value"] = attribute.mugiwara_to_bounty[mugiwara]
        
            image_to_upload = None

            if os.getenv("UPLOAD_IPFS") == "true":
                image_path = "./img/{}.png".format(mugiwara.lower().replace('_', '-'))
                image_to_upload = upload_to_ipfs(image_path)
             
            mugiwara_to_image_uri = image_meta.image_uri
            image_to_upload = (mugiwara_to_image_uri[mugiwara] if not image_to_upload else image_to_upload)
            #Image
            collectible_metadata["image"] = image_to_upload
            matadata = os.path.join(path, metadata_file_name)
            with open(matadata, "w") as file:
                json.dump(collectible_metadata, file)
                try:
                    os.mkdir(path)
                    print("Directory ", path, " created")
                except FileExistsError:
                    print("Directory ", path,  " already exists")

            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(matadata)

# curl -X POST -F file=@img/luffy.png http://127.0.0.1:5001/api/v0/add

def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://localhost:5001"
        response = requests.post(ipfs_url + "/api/v0/add", files={"file": image_binary})    
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = "https://ipfs.io/ipfs/{}?filename={}".format(
            ipfs_hash, filename)
        print(image_uri)
    return image_uri

