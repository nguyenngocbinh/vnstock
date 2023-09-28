library(testthat)
library(vndirect)
test_that("Get data for a valid ticker", {
  # Replace 'TPB' with a valid ticker from your API
  result <- getData(.tickers = "TPB", .size = 100)
  
  # Check if the result is a data frame
  expect_is(result, "data.frame")
  
  # Add more specific expectations based on the structure of the result
  # For example, check if specific columns exist or if certain values are present
})

test_that("Get data for multiple tickers", {
  # Replace with a list of valid tickers from your API
  tickers <- c("TPB", "HPG", "SSI")
  
  result <- getData(.tickers = tickers, .size = 100)
  
  # Check if the result is a data frame
  expect_is(result, "data.frame")
  
  # Add more specific expectations based on the structure of the result
  # For example, check if specific columns exist or if certain values are present
})

test_that("Get data for an invalid ticker", {
  # Replace 'INVALID' with an invalid ticker to test error handling
  expect_error(getData(.tickers = "INVALID", .size = 100), class = "error")
})

test_that("Get data with missing tickers", {
  # Test for missing .tickers parameter
  expect_error(getData(.size = 100), class = "error")
})

test_that("Get data with invalid size", {
  # Test for .size <= 0
  expect_error(getData(.tickers = "TPB", .size = 0), class = "error")
})

