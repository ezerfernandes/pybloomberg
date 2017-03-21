# -*- coding: utf-8 -*-
from pybloomberg import BloombergAPIConnector
import pybloomberg.queries as queries
import datetime as dt


if __name__ == '__main__':
	with BloombergAPIConnector() as conn:
		precos = queries.get_historical_data(conn,
			["IBM US Equity", "MSFT US Equity"],
			"PX_LAST",
			dt.date(2015, 1, 1),
			dt.date(2016, 1, 1),
			).as_dataframe()
		print(precos)