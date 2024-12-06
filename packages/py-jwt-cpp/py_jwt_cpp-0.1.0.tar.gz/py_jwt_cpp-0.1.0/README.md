# py_jwt_cpp

A Python wrapper around [jwt-cpp](https://github.com/Thalhammer/jwt-cpp).


## Installation

`pip install py_jwt_cpp`

## Usage

```python
import py_jwt_cpp

jwt = py_jwt_cpp.encode(data, private_key)
```

where:

- `data` is a `dict` with string key and string value.
- `RS256` algorithm will be used.


## Development

- To install deployment dependencies, run `poetry install`.
- To test the change locally, run `poetry run python setup.py build_ext --inplace`

## Local Build

```
poetry install
poetry build
```

## CI Build

1. tag the ref with a name staring with `cibuildwheel`
2. Push the tag onto Github. It will trigger `cibuildwheel` workflow building wheels for:

- OS
    - `latest-ubuntu`
    - `macos-13`
    - `macos-latest`
- Python:
    - `ubuntu`: `>= 3.8`
    - `macos`: `>= 3.9`

## Release

1. Tag your branch with a name staring with `cibuildwheel`.
2. Push it onto Github to trigger the wheel build.
3. Build sdist by `poetry build`.
4. Download the wheels from Github and put them into the `dist` folder.
5. Commit the change, tag a version such as `0.1.0`, and push the tag back to Github.

## TODO

- [ ] `decode` function.
- [ ] allowing `headers`
- [ ] allowing algorithms other than `RS256`


## LICENSE

MIT
