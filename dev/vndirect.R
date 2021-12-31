VNDIRECT <- list(
  METHODS = c('GET', 'POST', 'PUT', 'DELETE')
)

#' Request the VNDIRECT API
#' @param symbol stock symbol
#' @param size size
#' @return data.frame
#' @importFrom httr GET content
#' @importFrom magrittr extract2 `%>%`
#' @importFrom purrr map_dfr
#' @importFrom dplyr bind_rows
#' @example vndirect_query('VCB', 1000)
vndirect_query <- function(symbol = NULL, size = 100) {
  
  if (is.null(symbol)) {
    stop('symbol is not set')
  }
  
  base <- "https://finfo-api.vndirect.com.vn/v4/stock_prices/"
  
  endpoint = paste('code:', symbol)
  
  params = list(
    sort = "date",
    size = size,
    page = 1,
    q = endpoint
  )
  
  res <- GET(base, query = params)
  
  df <- content(res) %>% 
    extract2('data') %>% 
    map_dfr(bind_rows) 
  
  df
}

# formals(vndirect_query)$method <- VNDIRECT$METHODS

