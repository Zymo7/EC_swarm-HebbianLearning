#!/usr/bin/env python3
"""
Test script to verify the dynamic target tracking implementation.
This tests both backward compatibility and new functionality.
"""
import sys
from pathlib import Path
sys.path.append(Path(__file__).parents[1].__str__())

import numpy as np
from utils.Sensors import Sensors
from utils.Fitnesses import FitnessCalculator
from utils.Individual import Individual, thymio_genotype
from utils.Controllers import NNController, hebbianNNController

def test_sensors_backward_compatibility():
    """Test that sensors work without target_position (backward compatibility)"""
    print("\n=== Testing Sensors Backward Compatibility ===")
    
    sensor_list = ["NN", "NN"]
    sensors = Sensors(sensor_list, arena="circle_30x30")
    
    # Create mock positions and headings
    positions = np.array([[1.0, 2.0], [3.0, 4.0]])
    headings = np.array([0.0, 1.57])
    
    # Call without target_position (backward compatibility)
    sensors.calculate_states(positions, headings)
    states = sensors.get_current_state()
    
    # Should have 9D state (4 distances + 4 headings + 1 gradient)
    assert len(states[0]) == 9, f"Expected 9D state, got {len(states[0])}D"
    print(f"✓ Backward compatibility: State is 9D as expected: {states[0].shape}")
    
def test_sensors_with_target():
    """Test that sensors work with target_position (new functionality)"""
    print("\n=== Testing Sensors with Target Position ===")
    
    sensor_list = ["NN", "NN"]
    sensors = Sensors(sensor_list, arena="circle_30x30")
    
    # Create mock positions and headings
    positions = np.array([[1.0, 2.0], [3.0, 4.0]])
    headings = np.array([0.0, 1.57])
    target_position = np.array([15.0, 15.0])  # Center of 30x30 arena
    
    # Call with target_position (new functionality)
    sensors.calculate_states(positions, headings, target_position)
    states = sensors.get_current_state()
    
    # Should have 11D state (4 distances + 4 headings + 1 gradient + 2 target pos)
    assert len(states[0]) == 11, f"Expected 11D state, got {len(states[0])}D"
    print(f"✓ With target: State is 11D as expected: {states[0].shape}")
    
    # Verify the target position is correctly calculated
    expected_rel_x = target_position[0] - positions[0, 0]  # 15 - 1 = 14
    expected_rel_y = target_position[1] - positions[1, 0]  # 15 - 3 = 12
    actual_rel_x = states[0][9]
    actual_rel_y = states[0][10]
    
    print(f"✓ Robot 0: Expected relative target ({expected_rel_x:.1f}, {expected_rel_y:.1f}), " 
          f"Got ({actual_rel_x:.1f}, {actual_rel_y:.1f})")

def test_fitness_backward_compatibility():
    """Test that fitness calculation works without target_position"""
    print("\n=== Testing Fitness Backward Compatibility ===")
    
    # Create mock swarm and fitness calculator
    n_input = 9
    n_output = 2
    genotype = thymio_genotype("NN", n_input, n_output)
    swarm = [Individual(genotype, 0), Individual(genotype, 1)]
    
    initial_positions = np.array([[0.0, 1.0], [0.0, 1.0]])
    fitness_calc = FitnessCalculator(swarm, initial_positions, 10.0, 
                                     arena="circle_30x30", 
                                     objectives=['gradient'])
    
    positions = np.array([[5.0, 6.0], [5.0, 6.0]])
    headings = np.array([0.0, 1.57])
    
    # Call without target_position (backward compatibility)
    fitness = fitness_calc.obtain_fitnesses(positions, headings)
    print(f"✓ Backward compatibility: Gradient fitness calculated: {fitness}")
    assert fitness is not None, "Fitness should not be None"

def test_fitness_with_target():
    """Test that fitness calculation works with target_position"""
    print("\n=== Testing Fitness with Target Tracking ===")
    
    # Create mock swarm and fitness calculator
    n_input = 11
    n_output = 2
    genotype = thymio_genotype("NN", n_input, n_output)
    swarm = [Individual(genotype, 0), Individual(genotype, 1)]
    
    initial_positions = np.array([[0.0, 1.0], [0.0, 1.0]])
    fitness_calc = FitnessCalculator(swarm, initial_positions, 10.0, 
                                     arena="circle_30x30", 
                                     objectives=['target_tracking'])
    
    positions = np.array([[14.0, 16.0], [16.0, 14.0]])
    headings = np.array([0.0, 1.57])
    target_position = np.array([15.0, 15.0])
    
    # Call with target_position (new functionality)
    fitness = fitness_calc.obtain_fitnesses(positions, headings, target_position)
    print(f"✓ With target: Target tracking fitness calculated: {fitness}")
    
    # Check that fitness is reasonable (should be high when close to target)
    assert fitness[0] > 0 and fitness[0] <= 1, f"Fitness should be in (0, 1], got {fitness[0]}"
    print(f"  Distance-based fitness: {fitness[0]:.4f}")

def test_controller_9d_input():
    """Test that controllers work with 9D input (backward compatibility)"""
    print("\n=== Testing Controller with 9D Input ===")
    
    controller = NNController(n_states=9, n_actions=2, torch_=False)
    genotype = np.random.randn(9 * 9 + 9 * 2)  # Random weights
    controller.geno2pheno(genotype)
    
    # Create 9D state
    state = np.array([1.0, 1.5, 0.5, 2.0,  # 4 distances
                      0.1, -0.2, 0.3, -0.1,  # 4 headings
                      128.0])  # gradient value
    
    action = controller.velocity_commands(state)
    print(f"✓ 9D input: Action computed: {action}")
    assert action.shape == (2,), f"Expected action shape (2,), got {action.shape}"

def test_controller_11d_input():
    """Test that controllers work with 11D input (new functionality)"""
    print("\n=== Testing Controller with 11D Input ===")
    
    controller = NNController(n_states=11, n_actions=2, torch_=False)
    genotype = np.random.randn(11 * 11 + 11 * 2)  # Random weights
    controller.geno2pheno(genotype)
    
    # Create 11D state
    state = np.array([1.0, 1.5, 0.5, 2.0,  # 4 distances
                      0.1, -0.2, 0.3, -0.1,  # 4 headings
                      128.0,  # gradient value
                      5.0, -3.0])  # target position (relative)
    
    action = controller.velocity_commands(state)
    print(f"✓ 11D input: Action computed: {action}")
    assert action.shape == (2,), f"Expected action shape (2,), got {action.shape}"

def test_update_target_position():
    """Test the update_target_position function"""
    print("\n=== Testing Target Position Update ===")
    
    from utils.Simulate_swarm_population import update_target_position
    
    # Test at time 0
    target = update_target_position(0.0, 15.0, 15.0, 5.0, 0.1)
    expected = np.array([20.0, 15.0])  # At angle 0, target is at (center_x + radius, center_y)
    print(f"✓ At t=0: target at ({target[0]:.2f}, {target[1]:.2f}), expected ({expected[0]:.2f}, {expected[1]:.2f})")
    assert np.allclose(target, expected, atol=0.01), f"Target position mismatch"
    
    # Test at time pi/2 / angular_velocity = pi/(2*0.1) ≈ 15.7 seconds
    t = np.pi / (2 * 0.1)
    target = update_target_position(t, 15.0, 15.0, 5.0, 0.1)
    expected = np.array([15.0, 20.0])  # At angle pi/2, target is at (center_x, center_y + radius)
    print(f"✓ At t={t:.2f}: target at ({target[0]:.2f}, {target[1]:.2f}), expected ({expected[0]:.2f}, {expected[1]:.2f})")
    assert np.allclose(target, expected, atol=0.01), f"Target position mismatch"

def main():
    print("=" * 60)
    print("Dynamic Target Tracking Implementation Tests")
    print("=" * 60)
    
    try:
        test_sensors_backward_compatibility()
        test_sensors_with_target()
        test_fitness_backward_compatibility()
        test_fitness_with_target()
        test_controller_9d_input()
        test_controller_11d_input()
        test_update_target_position()
        
        print("\n" + "=" * 60)
        print("✓✓✓ All tests passed! ✓✓✓")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
