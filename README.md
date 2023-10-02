# Get data from vndirect API

## Installation 

```{r}
# install.packages("devtools")
devtools::install_github("nguyenngocbinh/vndirect")
```

## Get data

``` r
library(vndirect)
dt <- getData('VCB', 100)
head(dt)
```

    ## # A tibble: 6 x 25
    ##   ticker_name date       time     floor type  basicPrice ceilingPrice floorPrice
    ##   <chr>       <date>     <chr>    <chr> <chr>      <dbl>        <dbl>      <dbl>
    ## 1 VCB         2022-03-01 14:44:58 HOSE  STOCK       84.5         90.4       78.6
    ## 2 VCB         2022-02-28 15:02:03 HOSE  STOCK       85.1         91         79.2
    ## 3 VCB         2022-02-25 15:02:04 HOSE  STOCK       85.3         91.2       79.4
    ## 4 VCB         2022-02-24 15:02:03 HOSE  STOCK       86.9         92.9       80.9
    ## 5 VCB         2022-02-23 15:02:03 HOSE  STOCK       86.8         92.8       80.8
    ## 6 VCB         2022-02-22 15:02:02 HOSE  STOCK       87.4         93.5       81.3
    ## # ... with 17 more variables: open <dbl>, high <dbl>, low <dbl>, close <dbl>,
    ## #   average <dbl>, adOpen <dbl>, adHigh <dbl>, adLow <dbl>, adClose <dbl>,
    ## #   adAverage <dbl>, nmVolume <dbl>, nmValue <dbl>, ptVolume <dbl>,
    ## #   ptValue <dbl>, change <dbl>, adChange <dbl>, pctChange <dbl>

``` r
dplyr::glimpse(dt)
```

    ## Rows: 100
    ## Columns: 25
    ## $ ticker_name  <chr> "VCB", "VCB", "VCB", "VCB", "VCB", "VCB", "VCB", "VCB", "~
    ## $ date         <date> 2022-03-01, 2022-02-28, 2022-02-25, 2022-02-24, 2022-02-~
    ## $ time         <chr> "14:44:58", "15:02:03", "15:02:04", "15:02:03", "15:02:03~
    ## $ floor        <chr> "HOSE", "HOSE", "HOSE", "HOSE", "HOSE", "HOSE", "HOSE", "~
    ## $ type         <chr> "STOCK", "STOCK", "STOCK", "STOCK", "STOCK", "STOCK", "ST~
    ## $ basicPrice   <dbl> 84.5, 85.1, 85.3, 86.9, 86.8, 87.4, 87.2, 87.5, 87.0, 87.~
    ## $ ceilingPrice <dbl> 90.4, 91.0, 91.2, 92.9, 92.8, 93.5, 93.3, 93.6, 93.0, 93.~
    ## $ floorPrice   <dbl> 78.6, 79.2, 79.4, 80.9, 80.8, 81.3, 81.1, 81.4, 81.0, 81.~
    ## $ open         <dbl> 84.5, 85.1, 85.3, 86.7, 87.0, 87.0, 86.6, 86.4, 87.0, 87.~
    ## $ high         <dbl> 85.4, 85.1, 85.9, 86.8, 87.0, 87.0, 87.6, 87.5, 87.7, 87.~
    ## $ low          <dbl> 84.1, 84.4, 85.0, 85.0, 85.8, 85.0, 86.6, 86.4, 86.8, 86.~
    ## $ close        <dbl> 85.0, 84.5, 85.1, 85.3, 86.9, 86.8, 87.4, 87.2, 87.5, 87.~
    ## $ average      <dbl> 84.8487, 84.7500, 85.2500, 85.7200, 86.7600, 86.0500, 87.~
    ## $ adOpen       <dbl> 84.5, 85.1, 85.3, 86.7, 87.0, 87.0, 86.6, 86.4, 87.0, 87.~
    ## $ adHigh       <dbl> 85.4, 85.1, 85.9, 86.8, 87.0, 87.0, 87.6, 87.5, 87.7, 87.~
    ## $ adLow        <dbl> 84.1, 84.4, 85.0, 85.0, 85.8, 85.0, 86.6, 86.4, 86.8, 86.~
    ## $ adClose      <dbl> 85.0, 84.5, 85.1, 85.3, 86.9, 86.8, 87.4, 87.2, 87.5, 87.~
    ## $ adAverage    <dbl> 84.8487, 84.7500, 85.2500, 85.7200, 86.7600, 86.0500, 87.~
    ## $ nmVolume     <dbl> 1295400, 1322100, 1616500, 2078700, 986300, 1540200, 1017~
    ## $ nmValue      <dbl> 109913000000, 112046270000, 137812170000, 178190380000, 8~
    ## $ ptVolume     <dbl> 7900, 0, 60000, 79000, 0, 60000, 79000, 0, 60000, 79000, ~
    ## $ ptValue      <dbl> 6.588400e+03, 0.000000e+00, 5.217000e+09, 6.768100e+09, 0~
    ## $ change       <dbl> 0.5, -0.6, -0.2, -1.6, 0.1, -0.6, 0.2, -0.3, 0.5, 0.0, 1.~
    ## $ adChange     <dbl> 0.5, -0.6, -0.2, -1.6, 0.1, -0.6, 0.2, -0.3, 0.5, 0.0, 1.~
    ## $ pctChange    <dbl> 0.5917, -0.7051, -0.2345, -1.8412, 0.1152, -0.6865, 0.229~


```
vndirect
├─ cran-comments.md
├─ CRAN-SUBMISSION
├─ DESCRIPTION
├─ LICENSE
├─ man
│  └─ getData.Rd
├─ NAMESPACE
├─ R
│  └─ vndirect.R
├─ README.md
├─ tests
│  └─ test-getData.R
├─ vignettes
│  ├─ .gitignore
│  └─ getdata.Rmd
└─ vndirect.Rproj

```