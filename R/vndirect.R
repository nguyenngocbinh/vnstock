#' REQUEST THE VNDIRECT API
#' @param .ticker stock symbol
#' @param .size length of historical data
#' @return data.frame
#' @importFrom magrittr extract2 `%>%`
#' @importFrom dplyr bind_rows rename mutate
#' @importFrom purrr map_dfr
#' @example vnd_get_data('TPB', 1000)
#' @export
vnd_get_data <- function(.ticker = NULL, .size = 100) {
  
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
  
  res <- httr::GET(base, query = params) %>% 
    httr::content() %>% 
    extract2('data')
  
  if(length(res) < 1) {
    stop(paste('Do not have data. Try to correct ticker_name:', .ticker))
  }
  
  
  df <-  res %>% 
    map_dfr(bind_rows) %>% 
    rename(ticker_name = code) %>% 
    mutate(date = as.Date(date))
  
  
  df
}


#' GET DATA FROM MULTIPLE STOCKS
#' @param .tickers list of stock symbols
#' @param .size length of historical data
#' @return data.frame
#' @importFrom purrr map_dfr possibly
#' @example vnd_get_list_data(c('TPB', 'VCB'))
#' @export
vnd_get_list_data <- function(.tickers = NULL, .size = 100) {
  if (is.null(.tickers)) {
    stop('.ticker is not set')
  }
  
  if (.size <= 0) {
    stop('.size must be > 0')
  }
  
  df <- map_dfr(.tickers,
                possibly(vnd_get_data, NULL),
                .size = .size)
  
  return(df)
}



#' Company information
#'
#' @param .tickers ticker with 3 characters
#' @export
#' @example
#' tpb_info <- vnd_company_info("TPB")
#' all_company <- vnd_company_info()

vnd_company_info <-  function(.ticker = character()) {
  
  base <- 'https://finfo-api.vndirect.com.vn/stocks'
  
  endpoint = paste0(base, "?symbol=", .ticker)
  
  res <- httr::GET(endpoint) %>% 
    httr::content() %>% 
    magrittr::extract2('data')
  
  df_company_info <-  res %>% 
    map_dfr(bind_rows) %>% 
    rename(ticker_name = symbol) 
  
  df_company_info
  
}

