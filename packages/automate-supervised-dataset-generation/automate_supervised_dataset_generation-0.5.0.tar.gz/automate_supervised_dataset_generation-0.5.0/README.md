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
num_page = 1
labels = ["Not AI related","AI"]
sleep_time = 10
test_size=0.2
max_evals=3
trial_timeout=120
rv = automate_supervised_dataset_generation.automate.parallel_scraping(query,num_page,labels,sleep_time,test_size,max_evals,trial_timeout)
    
```

## License

`automate-supervised-dataset-generation` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
