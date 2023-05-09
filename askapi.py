from urllib3 import PoolManager
from json import dumps

def ask_api(accountInfo, dnsInfo):
    apiUrl = 'https://api.cloudflare.com/client/v4/zones/%s/dns_records/%s' % (
        accountInfo['zones'], dnsInfo['dns_records']
    )

    dnsInfo.pop('dns_records')
    body = dumps(dnsInfo)

    headers = {
        'user-agent': 'Mozilla/5.0',
        'X-Auth-Email': accountInfo['email'],
        'X-Auth-Key': accountInfo['api'],
        'Content-Type': 'application/json'
    }

    res = PoolManager().request("PUT", apiUrl, body=body, headers=headers)
    return res.status