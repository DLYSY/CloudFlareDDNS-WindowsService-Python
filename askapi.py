import requests
from json import dumps
from logging import getLogger



logger=getLogger("CLoudFlare DDNS Service")



def ask_api(accountInfo, dnsInfo):
    global logger

    logger.debug("创建请求标头、内容等")
    apiUrl = 'https://api.cloudflare.com/client/v4/zones/%s/dns_records/%s' % (accountInfo['zones'], dnsInfo['dns_records'])

    dnsInfo.pop('dns_records')
    body = dumps(dnsInfo)
    headers = {
        'user-agent': 'Mozilla/5.0',
        'X-Auth-Email': accountInfo['email'],
        'X-Auth-Key': accountInfo['api'],
        'Content-Type': 'application/json'
    }

    logger.debug("请求api")
    try:
        ask_api_status_code = requests.put(apiUrl,data=body,headers=headers).status_code
        logger.debug("api请求成功")
        return ask_api_status_code
    except requests.Timeout:
        logger.error("请求api时超时")
        return None
    except requests.ConnectionError:
        logger.error("请求api链接错误")
        return None
    except:
        logger.exception("请求api时发生意外错误：")
        return None