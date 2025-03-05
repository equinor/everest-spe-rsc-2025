# `simple`


## Description of the simple case

The simple case is an optimization experiment that uses a sine product as the objective function. 
The objective function is defined in the `forward_model.py` script and is given by:

```math
z = \sin(\pi \cdot x) \cdot \sin(\pi \cdot y)
```

where $x$ and $y$ are the control variables. 
The goal of the optimization is to find the values of $x$ and $y$ that maximize the objective function $z$.

## Content of the project

The case consists of:

1. a custom forward model script `forward_model.py` and job `forward_model`
2. an EVEREST configuration file `simple.yml`

The organization of these files follows an informal standard with a top level directory called `everest` and sub-directories called `input`, `model` and etc. 
This is the current layout of the files:

```
simple
├── everest
│   ├── input
│   │   ├── forward_model       # job script for the forward model
│   │   └── forward_model.py    # Python script for the forward model
│   └── model
│       ├── .benchmark.yml      # configuration file to benchmark simple.yml
│       └── simple.yml          # simple case EVEREST configuration file
└── README.md                   # this documentation
```


## Reproducing the presented results for the `simple.yml` case

The `simple.yml` case as created to exemplify an optimization experiment using one analytical function.
If you're interested in reproducing the presented results, you have to supplement the `simple.yml` configuration using the content of `.benchmark.yml`.
As the name suggests, this is a rather simple case, so you can simply copy the contents of `.benchmark.yml` and past it in `simple.yml`.
For more complicated setups, you should use supporting scripts or tools.
We suggest `yq`:

```bash
yq eval-all '. as $item ireduce ({}; . + $item)' simple.yml .benchmark.yml > simple_benchmark.yml
```

Finally can you obtain the expected results by running `everest run simple_benchmark.yml` and extracting the complete results from `simple.csv`.
