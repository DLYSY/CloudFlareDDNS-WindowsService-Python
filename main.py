from logging import getLogger
from urllib3.exceptions import MaxRetryError
from urllib3 import PoolManager
from askapi import ask_api
from re import compile
from json import loads
from os import path
from inspect import getfile,currentframe
from sys import exit



logger=getLogger('CLoudFlare DDNS Service')
    
dns_file=path.join(path.abspath(path.dirname(getfile(currentframe()))),'dns.json')
account_file=path.join(path.abspath(path.dirname(getfile(currentframe()))),'account.json')

with open(account_file,"r+")as file:
    account_info=loads(file.read())

def main():
    global account_info,logger


    logger.info("开始获取ipv4")
    try:
        ipv4 = PoolManager().request(method="GET", url="https://ipv4.icanhazip.com").data.decode().rstrip()#请求ipv4地址
        if compile('[0-9][0-9]?[0-9]?\.[0-9][0-9]?[0-9]?\.[0-9][0-9]?[0-9]?\.[0-9][0-9]?[0-9]?').findall(ipv4):
            logger.info("获取到的ipv4地址为%s",ipv4)
        else:
            logger.warn("获取到的地址为%s，不符合ipv4地址规范，请注意！",ipv4)
    except MaxRetryError:
        logger.error("获取ipv4时链接超时！请检查网络链接")
    except Exception as error:
        logger.error("尝试获取ipv4失败！回溯错误：\n%s",error)

    logger.info("开始获取 ipv6")
    try:
        ipv6 = PoolManager().request(method='GET', url='http://ipv6.icanhazip.com').data.decode().rstrip()
        if compile('^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$').findall(ipv6):
            logger.info("获取到的ipv6地址为%s",ipv6)
        else:
            logger.warn("获取到的地址为%s，不符合ipv6地址规范，请注意！",ipv6)
    except MaxRetryError:
        logger.error("获取ipv6时链接超时！请确定ipv6的可用性或检查网络链接")
    except Exception as error:
        logger.error("尝试获取ipv6失败！回溯错误：\n%s",error)


    try:
        with open(dns_file,'r') as dns_file_content:
            dns_info=loads(dns_file_content.read())
    except FileNotFoundError:
        logger.error("找不到DNS解析json文件")
        exit()
    except Exception as error_info:
        logger.error("")

    for i,data in enumerate(dns_info):
        if data['type']=='AAAA':
            data["content"]=ipv6
        elif data['type']=='A':
            data["content"]=ipv4

        res=ask_api(accountInfo=account_info,dnsInfo=data)
        if res==200:
            logger.info("成功解析ipv4")
        else:
            logger.error("%s号DNS解析失败，服务器返回：%s",i,res)

if __name__=="__main__":
    main()