# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_jwt_cpp']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'py_jwt_cpp',
    'version': '0.1.0',
    'description': 'A Python wrapper around jwt-cpp',
    'long_description': '# py_jwt_cpp\n\nA Python wrapper around [jwt-cpp](https://github.com/Thalhammer/jwt-cpp).\n\n\n## Installation\n\n`pip install py_jwt_cpp`\n\n## Usage\n\n```python\nimport py_jwt_cpp\n\njwt = py_jwt_cpp.encode(data, private_key)\n```\n\nwhere:\n\n- `data` is a `dict` with string key and string value.\n- `RS256` algorithm will be used.\n\n\n## Development\n\n- To install deployment dependencies, run `poetry install`.\n- To test the change locally, run `poetry run python setup.py build_ext --inplace`\n\n## Local Build\n\n```\npoetry install\npoetry build\n```\n\n## CI Build\n\n1. tag the ref with a name staring with `cibuildwheel`\n2. Push the tag onto Github. It will trigger `cibuildwheel` workflow building wheels for:\n\n- OS\n    - `latest-ubuntu`\n    - `macos-13`\n    - `macos-latest`\n- Python:\n    - `ubuntu`: `>= 3.8`\n    - `macos`: `>= 3.9`\n\n## Release\n\n1. Tag your branch with a name staring with `cibuildwheel`.\n2. Push it onto Github to trigger the wheel build.\n3. Build sdist by `poetry build`.\n4. Download the wheels from Github and put them into the `dist` folder.\n5. Commit the change, tag a version such as `0.1.0`, and push the tag back to Github.\n\n## TODO\n\n- [ ] `decode` function.\n- [ ] allowing `headers`\n- [ ] allowing algorithms other than `RS256`\n\n\n## LICENSE\n\nMIT\n',
    'author': 'Yanghsing Lin',
    'author_email': 'yanghsing.lin@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
