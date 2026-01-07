#!/usr/bin/env python3
"""
Basic validation script to check the structure of the implementation.
This doesn't require external dependencies.
"""
import ast
import sys
from pathlib import Path

def check_method_exists(filepath, class_name, method_name):
    """Check if a method exists in a class"""
    with open(filepath, 'r') as f:
        tree = ast.parse(f.read())
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name == method_name:
                    return True
    return False

def check_function_exists(filepath, function_name):
    """Check if a function exists in a file"""
    with open(filepath, 'r') as f:
        tree = ast.parse(f.read())
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            return True
    return False

def check_dict_key_exists(filepath, dict_name, key_name):
    """
    Check if a key exists in a dictionary definition.
    
    Note: This uses simple string search which may have limitations:
    - May give false positives if the key appears in comments or strings
    - May miss keys if formatting differs significantly
    - Sufficient for validation but not for production parsing
    """
    with open(filepath, 'r') as f:
        content = f.read()
        # Simple string search (not perfect but works for our case)
        return f"'{key_name}'" in content or f'"{key_name}"' in content

def main():
    root = Path(__file__).parents[2]
    print("=" * 60)
    print("Dynamic Target Tracking - Structure Validation")
    print("=" * 60)
    
    checks = []
    
    # Check Sensors.py
    print("\n[1/5] Checking utils/Sensors.py...")
    sensors_path = root / "utils" / "Sensors.py"
    
    check = check_method_exists(sensors_path, "Sensors", "target_position_sensor")
    checks.append(("Sensors.target_position_sensor()", check))
    print(f"  {'✓' if check else '✗'} target_position_sensor method exists")
    
    with open(sensors_path) as f:
        content = f.read()
        check = "target_position=None" in content
        checks.append(("calculate_states accepts target_position", check))
        print(f"  {'✓' if check else '✗'} calculate_states accepts target_position parameter")
    
    # Check Fitnesses.py
    print("\n[2/5] Checking utils/Fitnesses.py...")
    fitnesses_path = root / "utils" / "Fitnesses.py"
    
    check = check_method_exists(fitnesses_path, "FitnessCalculator", "calculate_target_tracking")
    checks.append(("FitnessCalculator.calculate_target_tracking()", check))
    print(f"  {'✓' if check else '✗'} calculate_target_tracking method exists")
    
    with open(fitnesses_path) as f:
        content = f.read()
        check = "'target_tracking'" in content
        checks.append(("target_tracking objective support", check))
        print(f"  {'✓' if check else '✗'} target_tracking objective is supported")
    
    # Check Simulate_swarm_population.py
    print("\n[3/5] Checking utils/Simulate_swarm_population.py...")
    sim_path = root / "utils" / "Simulate_swarm_population.py"
    
    check = check_function_exists(sim_path, "update_target_position")
    checks.append(("update_target_position function", check))
    print(f"  {'✓' if check else '✗'} update_target_position function exists")
    
    check = check_dict_key_exists(sim_path, "EnvSettings", "dynamic_target")
    checks.append(("dynamic_target in EnvSettings", check))
    print(f"  {'✓' if check else '✗'} dynamic_target key in EnvSettings")
    
    check = check_dict_key_exists(sim_path, "EnvSettings", "target_radius")
    checks.append(("target_radius in EnvSettings", check))
    print(f"  {'✓' if check else '✗'} target_radius key in EnvSettings")
    
    check = check_dict_key_exists(sim_path, "EnvSettings", "target_angular_velocity")
    checks.append(("target_angular_velocity in EnvSettings", check))
    print(f"  {'✓' if check else '✗'} target_angular_velocity key in EnvSettings")
    
    # Check Controllers.py
    print("\n[4/5] Checking utils/Controllers.py...")
    controllers_path = root / "utils" / "Controllers.py"
    
    with open(controllers_path) as f:
        content = f.read()
        # Check that state[9:11] normalization is present
        check = "state[9:11]" in content
        checks.append(("Controller supports 11D input", check))
        print(f"  {'✓' if check else '✗'} Controllers normalize state[9:11] for target position")
    
    # Check Dynamic_Target_Tracking.py
    print("\n[5/5] Checking experiments/Dynamic_Target_Tracking.py...")
    experiment_path = root / "experiments" / "Dynamic_Target_Tracking.py"
    
    with open(experiment_path) as f:
        content = f.read()
        check = "n_input = 11" in content
        checks.append(("Experiment uses n_input=11", check))
        print(f"  {'✓' if check else '✗'} n_input = 11")
        
        check = "'target_tracking'" in content
        checks.append(("Experiment uses target_tracking objective", check))
        print(f"  {'✓' if check else '✗'} objectives = ['target_tracking']")
        
        check = "'dynamic_target': True" in content or "['dynamic_target'] = True" in content
        checks.append(("Experiment enables dynamic_target", check))
        print(f"  {'✓' if check else '✗'} dynamic_target = True")
    
    # Summary
    print("\n" + "=" * 60)
    passed = sum(1 for _, check in checks if check)
    total = len(checks)
    
    print(f"Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("✓✓✓ All structure checks passed! ✓✓✓")
        print("=" * 60)
        return 0
    else:
        print("\n✗ Failed checks:")
        for name, check in checks:
            if not check:
                print(f"  - {name}")
        print("=" * 60)
        return 1

if __name__ == '__main__':
    sys.exit(main())
