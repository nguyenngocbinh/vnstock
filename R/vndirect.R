#' REQUEST THE VNDIRECT API
#' 
#' Retrieves historical stock data from the VNDIRECT API for multiple tickers.
#'
#' @param .tickers A character vector of stock symbols.
#' @param .size Length of historical data.
#' @return A data frame containing historical stock data for all tickers.
#' @importFrom magrittr `%>%`
#' @importFrom dplyr bind_rows
#' @import httr
#'
#' @examples
#' getData(c('TPB', 'VCB', 'HCM'), 1000)
#'
#' @export
getData <- function(.tickers = NULL, .size = 100) {
  
  # Check if .tickers and .size are valid
  if (is.null(.tickers) || length(.tickers) == 0) {
    stop('.tickers is not set')
  }
  
  if (.size <= 0) {
    stop('.size must be > 0')
  }
  
  # Define the base URL
  base <- "https://finfo-api.vndirect.com.vn/v4/stock_prices/"
  
  # Initialize an empty data frame to store the results
  df <- data.frame()
  
  for (ticker in .tickers) {
    
    # Check if the ticker is valid (e.g., it should be a non-empty string)
    if (!is.character(ticker) || nchar(ticker) != 3) {
      stop('Invalid ticker:', ticker)
    }
    
    # Define the endpoint for each ticker
    endpoint <- paste0('code:', ticker)
    print(endpoint)
    
    # Set query parameters
    params <- list(
      sort = "date",
      size = .size,
      page = 1,
      q = endpoint
    )
    
    # Send the HTTP request
    res <- httr::GET(url = base, query = params)
    
    # Check if the HTTP request was successful
    if (httr::http_error(res)) {
      warning(paste('Failed to retrieve data for ticker:', ticker))
      next  # Skip to the next ticker on error
    }
    
    # Extract and process the data
    list_data <- httr::content(res, "parsed")$data
    
    # Convert to a data frame
    if (length(list_data) > 0) {
      df_ticker <- purrr::map_dfr(list_data, bind_rows) %>% 
        dplyr::mutate(date = as.Date(date))
      
      # Add the data for the current ticker to the results
      df <- dplyr::bind_rows(df, df_ticker)
    } else {
      warning(paste('No data available for ticker:', ticker))
    }
  }
  
  return(df)
}


#' Company Information
#'
#' Retrieves company information from the VNDIRECT API for a given ticker.
#'
#' @param .ticker Ticker with 3 characters. Pass this parameter if you want to return information for a specific company.
#' @return A data frame containing company information.
#' @importFrom httr GET
#' @importFrom magrittr `%>%`
#' @export
#'
#' @examples 
#' # Retrieve information for a specific company
#' cpn_info <- companyInfo()
#' 
#' @export
companyInfo <- function(.ticker = NULL) {
  # Check if .ticker is valid
  if (is.null(.ticker) || nchar(.ticker) != 3) {
    stop('Invalid or missing .ticker. Please provide a valid 3-character ticker.')
  }
  
  # Define the base URL and endpoint
  base <- 'https://finfo-api.vndirect.com.vn/v4/stocks'
  endpoint <- paste0(base, "code:", .ticker)
  
  # Send the HTTP request
  res <- httr::GET(url = base, query = params)
  
  # Check if the HTTP request was successful
  if (httr::http_error(res)) {
    stop(paste('Failed to retrieve data for ticker:', .ticker))
  }
  
  # Extract and process the data
  df_company_info <- httr::content(res, "parsed")$data %>%
    purrr::map_dfr(bind_rows) 
  
  return(df_company_info)
}


