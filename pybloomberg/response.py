# -*- coding: utf-8 -*-
import pandas as _pd
import datetime as _dt


class BloombergAPIResponse(object):
	def __init__(self, request):
		self.request = request

	def as_events(self):
		return self.request.get_events_generator()

	def as_dict(self):
		precos = {}
		for msg in self.request.get_response_messages():
			sec_name = msg.getElement("securityData").getElement("security").getValue()
			field_data = msg.getElement("securityData").getElement("fieldData")
			precos[sec_name] = {
				x.getElement("date").getValue(): x.getElement(self.request.field_list[0]).getValue()
				for x in field_data.values()
				}
		return precos

	def as_dataframe(self):
		tickers = []
		for msg in self.request.get_response_messages():
			sec_name = msg.getElement("securityData").getElement("security").getValue()
			field_data = msg.getElement("securityData").getElement("fieldData")
			v = {x.getElement("date").getValue(): x.getElement(self.request.field_list[0]).getValue()
				for x in field_data.values()}
			tick = _pd.Series(v, name = sec_name)
			tickers.append(tick)
		return _pd.concat(tickers, axis = 1)

