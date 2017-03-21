# -*- coding: utf-8 -*-
import blpapi as _blpapi


class PeriodicityAdjustment(object):
	ACTUAL = "ACTUAL"


class PeriodicitySelection(object):
	MONTHLY = "MONTHLY"
	WEEKLY = "WEEKLY"
	DAILY = "DAILY"


class BloombergAPIConnector(object):
	def __init__(self, host='localhost', port=8194):
		self._host = host
		self._port = port
		self.is_connected = False
			
	def connect(self):
		self.session = self._create_session()
		if self.is_connected or not self.session.start():
			print("Failed to start session.")
			return
		else:
			self.is_connected = True
	
	def disconnect(self):
		self.session.stop()
	
	def __enter__(self):
		self.connect()
		return self
	
	def __exit__(self, exc_type, exc_value, traceback):
		self.disconnect()
	
	def _create_session(self):
		sessionOptions = _blpapi.SessionOptions()
		sessionOptions.setServerHost(self._host)
		sessionOptions.setServerPort(self._port)
		return _blpapi.Session(sessionOptions)

	def send_request(self, request):
		self.session.sendRequest(request._request)
		return request.get_response()
		


			
			
		
		