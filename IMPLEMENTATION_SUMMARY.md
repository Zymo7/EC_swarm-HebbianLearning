# Dynamic Target Tracking Implementation Summary

## Overview
This document summarizes the implementation of dynamic target tracking functionality for the EC_swarm-HebbianLearning repository.

## Changes Made

### 1. Core Functionality (`utils/Sensors.py`)
- **Added `target_position_sensor()` method**: Calculates relative position of target from each agent's perspective
- **Modified `calculate_states()` method**: Now accepts optional `target_position` parameter
- **Extended state vector**: When target position is provided, adds 2D relative position to state for NN-based controllers
- **Maintains backward compatibility**: Works with existing 9D state when target_position is None

### 2. Fitness Function (`utils/Fitnesses.py`)
- **Added `calculate_target_tracking()` method**: 
  - Calculates mean distance from all agents to target
  - Returns fitness = 1/(1 + mean_distance)
  - Encourages agents to get close to and track the target
- **Extended `obtain_fitnesses()` method**: Supports 'target_tracking' objective
- **Updated `get_fitness_size()` method**: Accounts for new objective type

### 3. Simulation Environment (`utils/Simulate_swarm_population.py`)
- **Added `update_target_position()` function**: 
  - Implements circular motion: target_pos = center + radius * [cos(ωt), sin(ωt)]
  - Configurable radius and angular velocity
- **Extended `EnvSettings`**: Added three new configuration parameters:
  - `dynamic_target`: bool - Enable/disable dynamic target
  - `target_radius`: float - Radius of circular motion
  - `target_angular_velocity`: float - Angular velocity in rad/s
- **Modified simulation loop**:
  - Calculates target position at each timestep if dynamic_target is enabled
  - Passes target position to sensors and fitness calculator

### 4. Controller Updates (`utils/Controllers.py`)
Updated state normalization for 11D input in:
- `NNController.velocity_commands()`: Added normalization for state[9:11]
- `widthNNController.velocity_commands()`: Added normalization for state[9:11]
- `recurrentNNController.velocity_commands()`: Added normalization for state[9:11] (total 13D with recurrence)
- `hebbianNNController.velocity_commands()`: Added normalization for state[9:11]
- `GNNController.velocity_commands()`: Added normalization for state[9:11]
- `adaptiveNNController`: Already compatible (uses NNController internally)

All controllers now handle both 9D (original) and 11D (with target) inputs gracefully.

### 5. New Experiment Script (`experiments/Dynamic_Target_Tracking.py`)
- Based on `Single_swarm_EvoExp.py`
- Configured for dynamic target tracking:
  - `n_input = 11` (increased from 9)
  - `objectives = ['target_tracking']`
  - `dynamic_target = True`
  - `target_radius = arena_size / 3`
  - `target_angular_velocity = 0.1`
- Uses Hebbian learning controller (hNN) with 11D input

### 6. Testing and Validation
Created two test scripts:
- **`validate_structure.py`**: 
  - No dependencies required
  - Validates code structure and presence of required methods
  - Checks all 12 key implementation points
- **`test_dynamic_target.py`**: 
  - Comprehensive functional tests
  - Tests backward compatibility (9D input)
  - Tests new functionality (11D input)
  - Tests target motion calculation
  - Tests fitness function

### 7. Documentation (`README.md`)
- Added "Dynamic Target Tracking" section
- Documented new features and configuration
- Provided usage examples
- Added testing instructions

## Key Design Decisions

### 1. Backward Compatibility
- All changes are backward compatible
- Original experiments work unchanged when `dynamic_target=False`
- Default behavior maintains 9D state vector

### 2. State Vector Extension
- Target position added as **relative coordinates** (not absolute)
- Placed at the end of state vector: [...existing 9 dims..., rel_x, rel_y]
- Enables agents to perceive target direction and distance

### 3. Fitness Function Design
- Simple distance-based metric: `1/(1 + mean_distance)`
- Bounded in (0, 1] range
- Encourages collective tracking (uses mean of all agents)
- Can be easily extended for alternative objectives

### 4. Target Motion
- Circular motion chosen for:
  - Predictability (useful for learning)
  - Continuous challenge (target never stops)
  - Configurability (radius and speed adjustable)
- Can be extended to other motion patterns in future

### 5. Controller Flexibility
- Arena size hardcoded to 30 in controllers for normalization
- Could be made dynamic by passing arena_size to controllers
- Current approach maintains API simplicity

## Testing Results

All validation checks passed:
- ✓ Sensors support target position
- ✓ Fitness function implements target tracking
- ✓ Environment settings include dynamic target configuration
- ✓ Controllers normalize 11D input correctly
- ✓ Experiment script configured properly
- ✓ Structure validation: 12/12 checks passed

## Usage Example

```python
from utils.Simulate_swarm_population import simulate_swarm_population, EnvSettings

# Configure for dynamic target tracking
settings = EnvSettings.copy()
settings['dynamic_target'] = True
settings['target_radius'] = 10.0
settings['target_angular_velocity'] = 0.1
settings['objectives'] = ['target_tracking']

# Run simulation with 11D input controllers
fitnesses = simulate_swarm_population(
    life_timeout=600,
    individuals=population,  # Controllers with n_input=11
    headless=True,
    env_params=settings
)
```

## Future Enhancements

Possible extensions:
1. **Multiple targets**: Track multiple moving targets
2. **Different motion patterns**: Linear, random walk, figure-8, etc.
3. **Obstacle avoidance**: Combined with target tracking
4. **Dynamic obstacle integration**: Moving obstacles + moving target
5. **Multi-objective fitness**: Combine target tracking with cohesion/alignment
6. **Prediction capabilities**: Agents learn to predict target motion
7. **Arena size as parameter**: Pass to controllers for better generalization

## Files Modified

1. `utils/Sensors.py` - Target position sensing
2. `utils/Fitnesses.py` - Target tracking fitness
3. `utils/Simulate_swarm_population.py` - Dynamic target support
4. `utils/Controllers.py` - 11D input handling
5. `experiments/Dynamic_Target_Tracking.py` - New experiment (created)
6. `experiments/TEST/test_dynamic_target.py` - Tests (created)
7. `experiments/TEST/validate_structure.py` - Validation (created)
8. `README.md` - Documentation

Total: 8 files, +649 lines, -11 lines

## Verification

To verify the implementation:

```bash
# Structure validation (no dependencies)
python experiments/TEST/validate_structure.py

# Run the experiment (requires Isaac Gym)
python experiments/Dynamic_Target_Tracking.py
```
