from json import dumps
from logging import getLogger
from requests import Session, Timeout, ConnectionError
from requests.adapters import HTTPAdapter



logger=getLogger("CLoudFlare DDNS Service")

ask_api_session = Session()
ask_api_session.mount("http://", HTTPAdapter(max_retries=2))
ask_api_session.mount("https://", HTTPAdapter(max_retries=2))



def ask_api(api_token:str,dns_info:dict):
    global logger, ask_api_session

    logger.debug("创建请求标头、内容等")
    apiUrl = "https://api.cloudflare.com/client/v4/zones/"+dns_info["zone_id"]+"/dns_records/"+dns_info["dns_id"]

    dns_info.pop("dns_id")
    dns_info.pop("zone_id")

    body = dumps(dns_info)

    logger.debug("请求api")
    try:
        ask_api_request = ask_api_session.put(apiUrl, data=body, headers={'Authorization':'Bearer '+api_token}, timeout=(5,5))
        logger.debug("api请求成功")
        return ask_api_request.status_code
    except Timeout:
        logger.error("请求api时超时")
        return None
    except ConnectionError:
        logger.error("请求api链接错误")
        return None
    except:
        logger.exception("请求api时发生意外错误：")
        return None