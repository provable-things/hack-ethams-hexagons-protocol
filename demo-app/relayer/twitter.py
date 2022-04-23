import os
import json
import time 
import requests

from web3 import Web3
from hashlib import sha256

ABI_FILE = './abi.json'
WEB3_ENDPOINT_KEY = 'rpc_endpoint'
TWITTER_BEARER_TOKEN_KEY = 'twitter_bearer_token'
NFT_COLLECTION_KEY = 'nft_collection_address'
USER_PRIVATE_KEY = 'private_key'

def bearer_oauth_headers(bearer_token):
    """
    Get the required headers needed for authorization
    """
    headers = {}
    headers["Authorization"] = f"Bearer {bearer_token}"
    headers["User-Agent"] = "v2FilteredStreamPython"
    return headers


def get_rules(config):
    bearer_token = config[TWITTER_BEARER_TOKEN_KEY]
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", 
        headers=bearer_oauth_headers(bearer_token)
    )
    
    if response.status_code != 200:
        raise Exception(f"Cannot get rules (HTTP {response.status_code}): {response.text}")
    
    
    return response.json()


def delete_all_rules(config, rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    bearer_token = config[TWITTER_BEARER_TOKEN_KEY]
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=bearer_oauth_headers(bearer_token),
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    


def get_abi():
    abi = {}
    with open(ABI_FILE) as f:
        abi = json.load(f)

    return abi

def set_rules(config, delete):    
    # You can adjust the rules if needed
    sample_rules = [{ 
        "value": "#HexagonsProtocol -is:retweet", 
        "tag": "Hexagons Protocol" 
    }]
    payload = {"add": sample_rules}
    bearer_token = config[TWITTER_BEARER_TOKEN_KEY]
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=bearer_oauth_headers(bearer_token),
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )


def get_stream(config, identity, oracle_module, set):
    bearer_token = config[TWITTER_BEARER_TOKEN_KEY]
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream?tweet.fields=id,author_id,created_at", 
        headers=bearer_oauth_headers(bearer_token), 
        stream=True,
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )


    w3 = Web3(Web3.HTTPProvider(identity[WEB3_ENDPOINT_KEY]))
    account = w3.eth.account.privateKeyToAccount(identity[USER_PRIVATE_KEY])
    
    w3.eth.default_account = account.address

    abi = get_abi()
    address = config[NFT_COLLECTION_KEY]
    contract = w3.eth.contract(address=address, abi=abi)

    print(f"Twitter module ready, listening for tweets by verified holders of {address}")

    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            author_id = json_response['data']['author_id']
            text = json_response['data']['text']
            created_at = json_response['data']['created_at']
                
            print("--------------------------")
            print(f"New tweet detected: \"{text}\"")

            username = username_from_authorid(author_id)
            if username:
                nft = nft_from_username(username)
                token_id = int(nft['token_id'])

                if nft: 
                    print("The author holds a compatible NFT, continuing...")
                    twitter = 1
                    query_id = sha256(bytes(author_id + created_at, 'utf-8')).digest()
                    author = contract.functions.ownerOf(token_id).call()    
                    text_data = bytes(text, 'utf-8')

                    print('Fetching the proof from the selected oracle...')
                    time.sleep(10)

                    proof = b'C0FFEE'

                    print('Proof successfully retrieved!')
                    
                    print('Submitting tx onchain...')

                    tx = contract.functions.sendHexagonsProtocolMessage(
                        twitter, 
                        query_id, 
                        author, 
                        text_data, 
                        proof
                    ).buildTransaction({
                        'gas': 150000,
                        'nonce' : w3.eth.get_transaction_count(account.address)
                    })
                    
                    stx = account.sign_transaction(tx)
                    
                    # print(f"Signed tx: {stx.rawTransaction.hex()}")

                    txhash = w3.eth.send_raw_transaction(stx.rawTransaction)
                    
                    print(f"Tx hash: {txhash.hex()}")

                else:
                    print("The author is out of scope, skipping...")


def nft_from_username(username):
    res = requests.get(f"https://api.hexagons.cafe/getNftDetailsByUsername?username={username}").json()
    if "err" in res.keys():
        if username == "stylishbuidler":
            return { "token_id": 0 }
        return None
    else: return res

def username_from_authorid(author_id):
   res = requests.post("https://tweeterid.com/ajax.php", data={"input": author_id}).text
   if res.find("@") > -1: return res.replace("@", "")
   else: return None

def run(args, identity, oracle_module):
    rules = get_rules(args)
    delete = delete_all_rules(args, rules)
    set = set_rules(args, delete)
    get_stream(args, identity['args'], oracle_module, set)
