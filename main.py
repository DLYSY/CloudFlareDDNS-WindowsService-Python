from logging import getLogger
from ask_api import ask_api
from json import load
from os import path
from sys import exit
from get_ip import get_ip
from sys import argv



logger=getLogger('CLoudFlare DDNS Service')
    
config_file=path.join(path.dirname(path.realpath(argv[0])),'config.json')



def main():
    global config_file,logger

    logger.debug("读取配置信息")
    try:
        with open(config_file,'r') as file_content:
            config_info=load(file_content)
        logger.debug("读取成功")
    except FileNotFoundError:
        logger.critical("找不到config文件")
        exit()
    except:
        logger.exception("读取配置时发生意外错误：")
        exit()

    logger.debug("解析DNS")
    for i,data in enumerate(config_info["dns_info"]):
        match data["type"]:
            case "AAAA":
                data["content"]=get_ip(6)
            case "A":
                data["content"]=get_ip(4)
            case _:
                pass
        
        if data["content"]!=None:
            ask_api_status_code=ask_api(api_token=config_info["api_token"],dns_info=data)
            match ask_api_status_code:
                case 200:
                    logger.info("%s号DNS成功解析",i)
                case None:
                    logger.error("%s号ask api发生错误，跳过",i)
                case _:
                    logger.error("%s号DNS解析失败，服务器返回：%s",i,ask_api_status_code)
        else:
            logger.error("%s号获取到的ip不正确，跳过",i)

    

if __name__=="__main__":
    import logging
    handler = logging.StreamHandler()

    formatter = logging.Formatter('【%(levelname)s】%(asctime)s《%(module)s：第%(lineno)d行》 · %(message)s',"%y/%m/%d-%H:%M:%S")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    main()