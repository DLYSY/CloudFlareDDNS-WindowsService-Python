import win32serviceutil
import win32service
import win32event
import servicemanager
from os import path
import logging
from logging import handlers
from main import main
from threading import Event
from sys import argv



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

        # this_file = getfile(currentframe())
        # dirpath = path.abspath(path.dirname(this_file))

        # dirpath=path.dirname(path.abspath(__file__))
        
        dirpath=path.dirname(path.realpath(argv[0]))
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
        # invoked as non-pywin32-PythonService.exe executable without
        # arguments
        
        # We assume here that we were invoked by the Windows Service
        # Control Manager (SCM) as a PyInstaller executable in order to
        # start our service.
        
        # Initialize the service manager and start our service.
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(ddns_service)
        servicemanager.StartServiceCtrlDispatcher()
    
    else:
        # invoked with arguments, or without arguments as a regular
        # Python script
  
        # We support a "help" command that isn't supported by
        # `win32serviceutil.HandleCommandLine` so there's a way for
        # users who run this script from a PyInstaller executable to see
        # help. `win32serviceutil.HandleCommandLine` shows help when
        # invoked with no arguments, but without the following that would
        # never happen when this script is run from a PyInstaller
        # executable since for that case no-argument invocation is handled
        # by the `if` block above.
        if len(argv) == 2 and argv[1] == 'help':
            argv = argv[:1]
        win32serviceutil.HandleCommandLine(ddns_service)