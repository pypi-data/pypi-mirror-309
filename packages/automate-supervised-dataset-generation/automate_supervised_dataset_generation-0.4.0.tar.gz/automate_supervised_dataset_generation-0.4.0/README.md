# automate-supervised-dataset-generation
-----

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install automate-supervised-dataset-generation
```

## Start the app
```
import automate_supervised_dataset_generation.automate
query = "Artificial Intelligence"
num_page = 5
sleep_time = 10
labels = ["spam","not Spam"]
results = automate_supervised_dataset_generation.automate.parallel_scraping(query,num_page,labels,sleep_time)
```

## License

`automate-unsupervised-dataset-generation` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
