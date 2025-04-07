import FinanceDataReader as fdr

from backend.models.stock import StockInfoResponse


def search_company(name: str) -> StockInfoResponse:

  krx_stocks = fdr.StockListing('KRX')
  company_info = krx_stocks[krx_stocks['Name'] == name]

  if company_info.empty:
      return StockInfoResponse(
          api_res=1,
          code=None,
          name=None,
          market=None
      )

  return StockInfoResponse(
        api_res=0,
        code=company_info['Code'].values[0],
        name=company_info['Name'].values[0],
        market=company_info['Market'].values[0]
    )