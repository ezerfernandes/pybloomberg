# -*- coding: utf-8 -*-
import datetime as _dt
import response as _response
import blpapi as _blpapi


class RequestType(object):
	HistoricalDataRequest = 'HistoricalDataRequest'

	
class BloombergAPIRequest(object):
	def __init__(
		self, connection,
		service_name='//blp/refdata',
		request_type=RequestType.HistoricalDataRequest
		):
		self._conn = connection
		self._service_name = service_name
		self._request_type = request_type
		self._request = self._create_request()
		self.field_list = []
		self.security_list = []
	
	def _create_request(self):
		ref_service = self._get_service()
		return ref_service.createRequest(self._request_type)

	def _get_service(self):
		try:
			self._conn.session.openService(self._service_name)
			return self._conn.session.getService(self._service_name)
		except:
			raise Exception("Failed to open {}".format(service_name))
	
	def set_securities(self, security_list):
		self.security_list = security_list
		for security_name in security_list:
			self._request.getElement("securities").appendValue(security_name)
	
	def set_fields(self, field_list):
		self.field_list = field_list
		for field_name in field_list:
			self._request.getElement("fields").appendValue(field_name)
	
	def set_parameters(self, **kwarg):
		for k, v in kwarg.iteritems():
			if v is not None:
				if isinstance(v, _dt.date):
					v = self._repr_date(v)
				self._request.set(k, v)
	
	def _repr_date(self, date):
		return date.strftime('%Y%m%d')
	
	def get_response(self):
		response = _response.BloombergAPIResponse(self)
		return response
	
	def get_dic_results(self):
		results = self.get_response_messages()
		return {}
	
	def get_response_messages(self):
		messages = []
		for ev in self.get_events_generator():
			if ev.eventType() in (_blpapi.Event.RESPONSE, _blpapi.Event.PARTIAL_RESPONSE):
				for msg in ev:
					messages.append(msg)
		return messages

	def get_events_generator(self):
		while True:
			event = self._conn.session.nextEvent()
			yield event
			if event.eventType() == _blpapi.Event.RESPONSE:
				break