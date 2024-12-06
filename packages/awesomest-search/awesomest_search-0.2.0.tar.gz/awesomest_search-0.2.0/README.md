# awesomest-search
-----

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install awesomest-search
```

## Start the app
```
import awesomest_search.search
para = "Hi my name is Prakhar!"
search_term = "Prakhar!"
level = 1 # for faster execution
# level = 2 # for slower execution
results = awesomest_search.search.awesome_search(para,search_term,level)
pprint(results)

```

## License

`automate-unsupervised-dataset-generation` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
