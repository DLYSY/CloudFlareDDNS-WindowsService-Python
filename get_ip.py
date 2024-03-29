from logging import getLogger
from re import compile
from requests import Session, Timeout, ConnectionError
from requests.adapters import HTTPAdapter



logger=getLogger("CLoudFlare DDNS Service")

reg=(None,None,None,None,compile('[0-9][0-9]?[0-9]?\.[0-9][0-9]?[0-9]?\.[0-9][0-9]?[0-9]?\.[0-9][0-9]?[0-9]?'),None,compile('(([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))'))

get_ip_session = Session()
get_ip_session.mount("http://", HTTPAdapter(max_retries=2))
get_ip_session.mount("https://", HTTPAdapter(max_retries=2))



def get_ip(ip_type:int):
    global logger, reg, get_ip_session

    match ip_type:
        case 4|6:
            logger.debug("获取ip")
            try:
                request_text=get_ip_session.get("https://myip{}.ipip.net/".format(ip_type),proxies={"http":None,"https":None}, timeout=(10, 10)).text
            except Timeout:
                logger.error("获取ipv%s时超时",ip_type)
                return None
            except ConnectionError:
                logger.error("获取ipv%s时链接错误",ip_type)
                return None
            except:
                logger.exception("获取ipv%s时发生意外错误：",ip_type)
                return None
        case _:
            raise ValueError("必须指定6以使用ipv6或4以使用ipv4")
    ip_search=reg[ip_type].search(request_text)
    if ip_search!=None:
        ip=ip_search.group()
        logger.info("获取到的ipv%s地址为%s",ip_type,ip)
        return ip
    else:
        logger.error("获取到不正确的ipv%s",ip_type)
        return None