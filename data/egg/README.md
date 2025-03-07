# `egg`


## Description of the Egg case



## Content of the project



## The available Egg dataset

There is no intention to reproduce the results of the original Egg dataset[^2]. 
The dataset is only used as an input to the optimization experiments.
So the obtained drainage strategy is expected to differ from previous publications.  


## Modifications of the original datasets

There are deviations from the original dataset that were needed to implement the optimization experiments. 
Most of these changes are related to the reservoir simulator `DATA` file.
These changes are summarized below:

- Replaced the `mDarcy.INC` by `PERM.INC` (realization-dependent permeability).
- Removed `RPTONLY` from the `SUMMARY` section.
- Added `RPTRST` with `'BASIC=4' 'FREQ=2' 'ALLPROPS'`.
- Added `FOIP` and `FPR` to the `SUMMARY` section.
- Changed `START` to `24.03.2025`.
- Removed the `TUNNING` section.
- Renamed realization 100 to realization 0 to be consistent with EVEREST.




[^1]: Jansen, J.D., Fonseca, R.M., Kahrobaei, S., Siraj, M.M., Van Essen, G.M. and Van den Hof, P.M.J. (2014), The egg model – a geological ensemble for reservoir simulation. Geosci. Data J., 1: 192-195. https://doi.org/10.1002/gdj3.21
[^2]: J.D.Jansen (2013): The Egg Model - data files. Version 1. 4TU.ResearchData. dataset. https://doi.org/10.4121/uuid:916c86cd-3558-4672-829a-105c62985ab2