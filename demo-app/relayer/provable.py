import json
import requests

oracle_endpoint = "https://api.provable.xyz/api/v1"

def query_status(id):
  resp = requests.get(f"{oracle_endpoint}/api/v1/query/{id}/status").json()

  result = None
  try:
    result = resp['result']['checks'][0]['results'][0]
  except Exception as e:

    return False

  return (result, None)

def fetch_with_proof(url):
  payload = { 
    'datasource': 'URL', 
    'query': url, 
    'proof_type': 0, 
  }
  resp = requests.post(oracle_endpoint + "/query/create", data=payload).json()
  id = resp['result']['id']

  resp = requests.get(oracle_endpoint + '/api/v1/query/{}/status'.format(id)).json()

  result = None
  
  # while not result:
  #   (result, proof) = query_status(id)

  result, proof = query_status(id)

  if not proof:
    proof = b'C0FFEE' # FIXME: handle the case when the proof is missing
  return (result, proof)

  