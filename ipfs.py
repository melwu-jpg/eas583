import requests
import json

def pin_to_ipfs(data):
	assert isinstance(data,dict), f"Error pin_to_ipfs expects a dictionary"

	json_data = {"data": data}

	url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"

	headers = {"accept":"application/json" ,
	 "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiIxY2QxYmI3Zi0xNWVjLTRhMmEtYjFlMS1jYjFjYjY2YTMyNzQiLCJlbWFpbCI6Im1lbHd1QHNlYXMudXBlbm4uZWR1IiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInBpbl9wb2xpY3kiOnsicmVnaW9ucyI6W3siZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjEsImlkIjoiRlJBMSJ9LHsiZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjEsImlkIjoiTllDMSJ9XSwidmVyc2lvbiI6MX0sIm1mYV9lbmFibGVkIjpmYWxzZSwic3RhdHVzIjoiQUNUSVZFIn0sImF1dGhlbnRpY2F0aW9uVHlwZSI6InNjb3BlZEtleSIsInNjb3BlZEtleUtleSI6IjI4NDJkMzM3MTAzMjQ3NTUzMGZkIiwic2NvcGVkS2V5U2VjcmV0IjoiNDVlZDViMGU0Y2U3ZTVhMjcyN2ExMTk0ZGNmNTk1MDQ0NzNiZjcwNWMwYmJjMTdhNzQxMTI5ZDMxY2VhZTU4ZSIsImV4cCI6MTc2MDk3NzgxM30.0cIqGKqldxMITb9wlbjXX4Spp6_xJ-3mh4J5ZyqlLoY"
	 }

	response = requests.post(url,json=json_data, headers=headers)

	response_data = response.json()

	cid = response_data.get("IpfsHash")

	return cid

def get_from_ipfs(cid,content_type="json"):
	assert isinstance(cid,str), f"get_from_ipfs accepts a cid in the form of a string"
	
	url = f"https://gateway.pinata.cloud/ipfs/{cid}"

	response = requests.get(url)

	response.raise_for_status()

	raw_data = response.json()

	if isinstance(raw_data, dict):
		return raw_data.get("data", raw_data)


	assert isinstance(data,dict), f"get_from_ipfs should return a dict"
	return data
