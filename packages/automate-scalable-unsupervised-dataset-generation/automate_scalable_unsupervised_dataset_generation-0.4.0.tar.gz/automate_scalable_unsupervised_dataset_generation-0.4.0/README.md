# automate-scalable-unsupervised-dataset-generation
-----

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install automate-scalable-unsupervised-dataset-generation
```

## Start the app
```
import automate_scalable_unsupervised_dataset_generation.automate
query = ["Artificial Intelligence","recipe of lemon tea!"]
num_page = 5
sleep_time = 10
results = automate_scalable_unsupervised_dataset_generation.automate.parallel_scraping(query,num_page,sleep_time)
```

## License

`automate-scalable-unsupervised-dataset-generation` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
