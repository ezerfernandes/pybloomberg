# -*- coding: utf-8 -*-
__all__ = ['get_historical_data']


import request as _rq


def get_historical_data(
	connection, security_list, field_name, start_date, end_date,
	per_adjustment='ACTUAL', per_selection='DAILY',
	max_data_points=None,
	):
	request = _rq.BloombergAPIRequest(connection)
	request.set_securities(security_list)
	request.set_fields([field_name,])
	request.set_parameters(
		periodicityAdjustment=per_adjustment,
		periodicitySelection=per_selection,
		startDate=start_date,
		endDate=end_date,
		maxDataPoints=max_data_points,
		)
	results = []
	response = connection.send_request(request)
	return response