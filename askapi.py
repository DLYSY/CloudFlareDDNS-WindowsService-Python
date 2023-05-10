import requests
from json import dumps

def ask_api(accountInfo, dnsInfo):
    apiUrl = 'https://api.cloudflare.com/client/v4/zones/%s/dns_records/%s' % (accountInfo['zones'], dnsInfo['dns_records'])

    dnsInfo.pop('dns_records')
    body = dumps(dnsInfo)

    headers = {
        'user-agent': 'Mozilla/5.0',
        'X-Auth-Email': accountInfo['email'],
        'X-Auth-Key': accountInfo['api'],
        'Content-Type': 'application/json'
    }
    ask_api_status_code = requests.put(apiUrl,data=body,headers=headers).status_code
    return ask_api_status_code