import os
import socket
import subprocess

from gpsdclient import GPSDClient

# from api.errors import APIException
# from api.services.config.settings import settings_singleton
# from api.services.logger import get_logger


# ====================
settings = {
    'gps': {
        'serial': '/dev/ttyAMA0'
    }
}

class APIException(Exception):
	def __init__(self, code, message):
		self.code = code
		self.message = message
		super().__init__(self.code, self.message)
	def to_dict(self):
		return {
			'code': self.code,
			'message': self.message
		}


def get_logger(context='api'):
    class Logger:
        def debug(self, msg):
            print(f'[{context}] Debug: {msg}')
        
        def exception(self, msg):
            print(f'[{context}] Exception: {msg}')
    
    return Logger()

logger = get_logger('system')
# ====================

class GPS:

	def __init__(self) -> None:
		self.client = GPSDClient(timeout=5)

	@staticmethod
	def start():
		logger.debug('Check if gpsd is running...')
		gpsd_processes = int(subprocess.run(["pgrep", "-c", "gpsd"], capture_output=True, text=True).stdout)
		logger.debug(f'GPSD Processes: {gpsd_processes}')
		if gpsd_processes == 0:
			dev = settings['gps']['serial']
			if not os.path.exists(dev):
				logger.exception(f'Dispositivo {dev} não encontrado, verifique conexão serial')
				return
			logger.debug(f'Starting gpsd process for {dev}')
			subprocess.run(["sudo", "gpsd", "-F", "/var/run/gpsd.sock", dev])

	@staticmethod
	def stop():
		logger.debug('Killing all gps daemon')
		pidstr = subprocess.run(["pgrep", "gpsd"], capture_output=True, text=True).stdout.strip()
		if pidstr == '':
			return
		subprocess.check_call(f'sudo kill -9 {int(pidstr)}', shell=True)

	@staticmethod
	def restart():
		GPS.stop()
		GPS.start()

	def get(self, retry = -1):
		try:
			for result in self.client.dict_stream(convert_datetime=False):
				if (result.get("class") == "TPV"):
					yield { "time": result.get("time", None), "lat": result.get("lat", 0),  "lon": result.get("lon", 0) }
				if retry == 0:
					logger.exception('Tentativas de obter dados do GPS falharam')
					raise APIException('GPS0005', 'Tentativas de obter dados do GPS falharam')
				if retry > 0:
					retry -= 1
		except socket.timeout: # Timeout
			logger.exception('Módulo GPS não obteve nenhum resultado, verifique conexão e reinicie')
			yield { "time": None, "lat": 0,  "lon": 0 }
		except Exception as e: 
			logger.exception(f'Exception: {str(e)}')
			yield { "time": None, "lat": 0,  "lon": 0 }

if __name__ == "__main__":
	import time
	GPS.start()
	time.sleep(1)
	for p in GPS().get():
		print(p)
