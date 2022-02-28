#' Request the VNDIRECT API
#' @param .ticker stock symbol
#' @param .size length of historical data
#' @return data.frame
#' @importFrom httr GET content
#' @importFrom magrittr extract2 `%>%`
#' @importFrom purrr map_dfr
#' @importFrom dplyr bind_rows
#' @example vnd_get_data('VCB', 1000)
vnd_get_data <- function(.ticker = NULL, .size = 1000) {
  
  if (is.null(.ticker)) {
    stop('.ticker is not set')
  }
  
  if(.size <= 0){
    stop('.size must be > 0')
  }
  
  base <- "https://finfo-api.vndirect.com.vn/v4/stock_prices/"
  
  endpoint = paste('code:', .ticker)
  
  params = list(
    sort = "date",
    size = .size,
    page = 1,
    q = endpoint
  )
  
  res <- GET(base, query = params)
  
  df <- content(res) %>% 
    extract2('data') %>% 
    map_dfr(bind_rows) %>% 
    rename(ticker_name = code) %>% 
    mutate(date = as.Date(date))
    
  
  df
}
