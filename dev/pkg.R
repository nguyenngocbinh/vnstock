
library(desc)
my_desc <- description$new("!new")
my_desc$set("Package", "vnd.data")
my_desc$set(
  "Authors@R",
  "('Ngoc Binh', 'Nguyen', email = 'nguyenngocbinhneu@gmail.com', role = c('cre', 'aut'))"
)

my_desc$set_version("0.0.0.9000")
my_desc$set(Title = "GET DATA FROM VNDIRECT API")
my_desc$set(Description = "Some utilities functions to get data from vndirect api")
my_desc$set("URL", "https://github.com/nguyenngocbinh/vnd_data")
my_desc$set("BugReports", "https://github.com/nguyenngocbinh/vnd_data/issues")
my_desc$del("Maintainer")

my_desc$write(file = "DESCRIPTION")