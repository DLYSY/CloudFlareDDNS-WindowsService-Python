from logging import getLogger
import requests
from askapi import ask_api
from re import compile
from json import loads
from os import path
from inspect import getfile,currentframe
from sys import exit



logger=getLogger('CLoudFlare DDNS Service')
    
dns_file=path.join(path.abspath(path.dirname(getfile(currentframe()))),'dns.json')
account_file=path.join(path.abspath(path.dirname(getfile(currentframe()))),'api_token.json')

logger.debug("读取账户信息")
try:
    with open(account_file,"r+")as file:
        api_token=loads(file.read())["api_token"]
    logger.debug("读取成功")
except FileNotFoundError:
    logger.critical("找不到account.json")
    exit()



def main():
    global account_info,logger

    logger.debug("获取ipv4")
    try:
        get_ipv4_error=1
        ipv4 = requests.get("http://ipv4.icanhazip.com",proxies={"http":None,"https":None}).text.rstrip()#请求ipv4地址
        if compile('[0-9][0-9]?[0-9]?\.[0-9][0-9]?[0-9]?\.[0-9][0-9]?[0-9]?\.[0-9][0-9]?[0-9]?').findall(ipv4):
            logger.info("获取到的ipv4地址为%s",ipv4)
        else:
            logger.warning("获取到的地址为%s，不符合ipv4地址规范，但依然尝试解析",ipv4)
        get_ipv4_error=0
    except requests.Timeout:
        logger.error("获取ipv4时链接超时")
    except requests.ConnectionError:
        logger.error("获取ipv4时链接错误")
    except:
        logger.exception("获取ipv4时发生意外错误：")

    logger.debug("获取ipv6")
    try:
        get_ipv6_error=1
        ipv6 = requests.get('http://ipv6.icanhazip.com',proxies={"http":None,"https":None}).text.rstrip()
        if compile('^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$').findall(ipv6):
            logger.info("获取到的ipv6地址为%s",ipv6)
        else:
            logger.warning("获取到的地址为%s，不符合ipv6地址规范，但依然尝试解析",ipv6)
        get_ipv6_error=0
    except requests.Timeout:
        logger.error("获取ipv6链接超时")
    except requests.ConnectionError:
        logger.error("获取ipv6链接错误")
    except :
        logger.exception("获取ipv6时发生意外错误：")

    logger.debug("读取dns信息")
    try:
        with open(dns_file,'r') as dns_file_content:
            dns_info=loads(dns_file_content.read())
        logger.debug("读取成功")
    except FileNotFoundError:
        logger.critical("找不到DNS解析json文件")
        exit()
    except:
        logger.exception("发生意外错误：")
        exit()

    logger.debug("解析DNS")
    for i,data in enumerate(dns_info):
        if data['type']=='AAAA' and not get_ipv6_error:
            data["content"]=ipv6
        elif data['type']=='A' and not get_ipv4_error:
            data["content"]=ipv4
        elif data['type']=='AAAA' and get_ipv6_error:
            continue
        elif data['type']=='A' and get_ipv4_error:
            continue

        ask_api_status_code=ask_api(api_token=api_token,dns_info=data)
        match ask_api_status_code:
            case 200:
                logger.info("%s号DNS成功解析",i)
            case None:
                logger.error("%s号ask api发生错误，跳过",i)
            case _:
                logger.error("%s号DNS解析失败，服务器返回：%s",i,ask_api_status_code)



if __name__=="__main__":
    import logging
    handler = logging.StreamHandler()

    formatter = logging.Formatter('【%(levelname)s】%(asctime)s《%(module)s：第%(lineno)d行》 · %(message)s',"%y/%m/%d-%H:%M:%S")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    main()