import win32serviceutil
import win32service
import win32event
import servicemanager
from os import path,mkdir
import logging
from logging import handlers
from main import main
from threading import Event
from sys import argv,exit
from get_path import get_path



class ddns_service(win32serviceutil.ServiceFramework):
    _svc_name_ = "CloudFlare DDNS" #服务名
    _svc_display_name_ = "CloudFlare DDNS" #服务在windows系统中显示的名称
    _svc_description_ = "CloudFlare的DDNS服务" #服务描述


    def __init__(self, args):

        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.logger = self._getLogger()
        self.stop=Event()


    def _getLogger(self):
        logger = logging.getLogger('CLoudFlare DDNS Service')
        dirpath=get_path()
        if not path.exists(path.join(dirpath, "log")):
            mkdir(path.join(dirpath, "log"))
        handler = handlers.TimedRotatingFileHandler(path.join(dirpath, "log/DDNS_Service.log"),when="midnight",backupCount=7)

        formatter = logging.Formatter('【%(levelname)s】%(asctime)s《%(module)s：第%(lineno)d行》 · %(message)s',"%H:%M:%S")
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        return logger


    def SvcDoRun(self):
        '''
        服务逻辑
        '''
        self.logger.info("服务开始运行")#输出日志   
        while not self.stop.is_set():
            main()
            self.stop.wait(90)
        self.logger.info("服务成功停止")

    def SvcStop(self):
        '''
        服务停止时运行函数
        '''
        self.logger.info("开始停止服务")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.stop.set()
    


if __name__=='__main__':
    if len(argv) == 1 and argv[0].endswith('.exe') and not argv[0].endswith(r'win32/pythonservice.exe'):
        # 启动服务
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(ddns_service)
        servicemanager.StartServiceCtrlDispatcher()
    
    elif len(argv) == 2 and argv[1] == 'help':
        #help 命令支持
        print('''
        选项：
        help：显示本帮助
        install：安装为系统服务（需要管理员权限）
        ''')
        exit()
    else:
        win32serviceutil.HandleCommandLine(ddns_service)