# EC_swarm
Pipeline for using Evolutionary Computing techniques applied on swarm robotics.

------
#### This branch is directly related to the following paper:
### Emergence of specialized Collective Behaviors in Evolving Heterogeneous Swarms

Link to this work can be found here
https://arxiv.org/abs/2402.04763

To run the same evolutionary experiments as presented in the paper run the following line after [Installation](#installation):

```
./run-experiment.sh Hebbian_swarm_EvoExp
```

[//]: # (To retest the best controllers and re-run the validation experiments:)

[//]: # (```)

[//]: # (wget https://dataverse.nl/dataset.xhtml?persistentId=doi%3A10.34894%2F0VSN8Z#)

[//]: # (unzip ./results.zip)

[//]: # (python ./results/RetestBest.py)

[//]: # (```)

---

## Dynamic Target Tracking

This repository now includes support for **dynamic target tracking**, extending the original static gradient-based navigation to handle moving targets.

### Features

The dynamic target tracking implementation includes:

- **Circular Motion Target**: Target moves in uniform circular motion with configurable radius and angular velocity
- **Extended Observation Space**: State vector expanded from 9D to 11D
  - Original: 4 distances + 4 headings + 1 gradient = 9D
  - New: 4 distances + 4 headings + 1 gradient + 2 target position (relative) = 11D
- **New Fitness Function**: `target_tracking` objective that encourages agents to approach and follow the moving target
- **Backward Compatible**: All existing experiments work unchanged when `dynamic_target=False`

### Running Dynamic Target Tracking Experiments

To run dynamic target tracking experiments:

```bash
python experiments/Dynamic_Target_Tracking.py
```

This experiment uses:
- 11-dimensional input (includes relative target position)
- Circular target motion (radius = arena_size/3, angular_velocity = 0.1 rad/s)
- Target tracking fitness function

### Configuration

Dynamic target settings in `EnvSettings`:

```python
simulator_settings = {
    'dynamic_target': True,              # Enable dynamic target
    'target_radius': 10.0,               # Radius of circular motion
    'target_angular_velocity': 0.1,      # Angular velocity (rad/s)
    'objectives': ['target_tracking'],   # Use target tracking fitness
    # ... other settings
}
```

### Testing

Run validation tests to verify the implementation:

```bash
# Structure validation (no dependencies required)
python experiments/TEST/validate_structure.py

# Full functional tests (requires dependencies)
python experiments/TEST/test_dynamic_target.py
```

---

### Citation:
```
@article{van2024emergence,
  title={Emergence of specialized Collective Behaviors in Evolving Heterogeneous Swarms},
  author={van Diggelen, Fuda and De Carlo, Matteo and Cambier, Nicolas and Ferrante, Eliseo and Eiben, AE},
  journal={arXiv preprint arXiv:2402.04763},
  year={2024}
}
```

Replication data can be downloaded from here https://doi.org/10.34894/0VSN8Z

---
REQUIREMENTS
------------

This EC pipeline requires the following for the simulator <a href="https://developer.nvidia.com/isaac-gym" target="_blank">Isaac Gym</a>:
* Ubuntu 18.04 or 20.04
* CUDAnn (only an installation is required, there is no need to use it)
* Python 3.8

## Installation
- clone the repository
```bash
git clone https://github.com/fudavd/EC_swarm
```

- Download and extract Isaac Gym in the `/thirdparty/` folder (can be downloaded from <a href="https://developer.nvidia.com/isaac-gym" target="_blank">here</a>)
- Create a Python virtual environment in the `EC_swarm` root directory:
```bash
virtualenv -p=python3.8 .venv
source .venv/bin/activate
pip install -r requirements.txt
```
---
Publications
------
#### This repo is directly related to the following papers:
* Van Diggelen, F., Luo, J., Karagüzel, T. A., Cambier, N., Ferrante, E., & Eiben, A. E. (2022, July). Environment induced emergence of collective behavior in evolving swarms with limited sensing. In _Proceedings of the Genetic and Evolutionary Computation Conference_ (pp. 31-39). https://doi.org/10.1145/3512290.3528735. [**[Branch]**](https://github.com/fudavd/EC_swarm/tree/GECCO_2022)
* van Diggelen, F., De Carlo, M., Cambier, N., Ferrante, E., & Eiben, G. (2024, September). Emergence of Specialised Collective Behaviors in Evolving Heterogeneous Swarms. In International Conference on Parallel Problem Solving from Nature (pp. 53-69). Cham: Springer Nature Switzerland. https://doi.org/10.1007/978-3-031-70068-2_4. [**[Branch]**](https://github.com/fudavd/EC_swarm/tree/PPSN_2024)
---
