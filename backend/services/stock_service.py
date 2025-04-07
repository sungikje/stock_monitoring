# Lib import
from fastapi import HTTPException
import FinanceDataReader as fdr
from typing import List

# Project import
from backend.models.stock import StockInfoResponse


def search_company(name: str) -> List[StockInfoResponse]:

	krx_stocks = fdr.StockListing('KRX')
	company_info = krx_stocks[krx_stocks['Name'].str.contains(name, case=False, na=False)]

	if company_info.empty:
		print('error')
		raise HTTPException(status_code=404, detail="Company not found")

	result = [
		StockInfoResponse(
			code=row['Code'],
			name=row['Name'],
			market=row['Market']
		)
		for _, row in company_info.iterrows()
	]

	return result