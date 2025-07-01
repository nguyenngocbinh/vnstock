# vnstock

vnstock is a Python library for retrieving historical stock data from the VNDIRECT API.

## Installation

You can install vnstock using `pip`:

```
pip install vnstock
```

## Usage

```python
from vnstock.vnstock import VNStockData

tickers = ['TPB', 'VCB', 'HCM']
size = 100
vns = VNStockData(tickers, size)
df = vns.get_data()
print(df)
```

## Running Tests

This package uses Python's built-in `unittest` framework. Example tests are provided in the `tests/` directory.

To run all tests, from the `python-package` directory, use:

```
python -m unittest discover tests
```

## Documentation

For detailed documentation, please visit the [GitHub repository](https://github.com/nguyenngocbinh/vnstock).

## License

vnstock is released under the MIT License.

## Contributing

If you'd like to contribute to vnstock, please fork the repository and create a pull request.

## Bug Reports

If you encounter any issues or have suggestions, please report them in the [issue tracker](https://github.com/nguyenngocbinh/vnstock/issues).
