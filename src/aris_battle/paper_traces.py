"""Numerical traces currently reported in the manuscript."""

JAMMING_SWEEP = [
    {"gain_db": 0, "no_aris_prr": 99, "attacker_aris_prr": 98, "defender_aris_prr": 100},
    {"gain_db": 5, "no_aris_prr": 92, "attacker_aris_prr": 71, "defender_aris_prr": 100},
    {"gain_db": 10, "no_aris_prr": 50, "attacker_aris_prr": 11, "defender_aris_prr": 100},
    {"gain_db": 15, "no_aris_prr": 8, "attacker_aris_prr": 1, "defender_aris_prr": 100},
    {"gain_db": 20, "no_aris_prr": 1, "attacker_aris_prr": 0, "defender_aris_prr": 100},
    {"gain_db": 25, "no_aris_prr": 0, "attacker_aris_prr": 0, "defender_aris_prr": 97},
    {"gain_db": 30, "no_aris_prr": 0, "attacker_aris_prr": 0, "defender_aris_prr": 80},
    {"gain_db": 35, "no_aris_prr": 0, "attacker_aris_prr": 0, "defender_aris_prr": 29},
    {"gain_db": 40, "no_aris_prr": 0, "attacker_aris_prr": 0, "defender_aris_prr": 4},
]

SENSING_TRACE = [
    {"time_s": 0, "no_aris_db": 0, "obfuscation_db": 0, "counter_aris_db": 0},
    {"time_s": 10, "no_aris_db": 2, "obfuscation_db": 5, "counter_aris_db": 1},
    {"time_s": 20, "no_aris_db": -1, "obfuscation_db": -3, "counter_aris_db": -0.5},
    {"time_s": 30, "no_aris_db": 3, "obfuscation_db": 4, "counter_aris_db": 1.5},
    {"time_s": 40, "no_aris_db": -2, "obfuscation_db": -5, "counter_aris_db": -1},
    {"time_s": 50, "no_aris_db": 1, "obfuscation_db": 2, "counter_aris_db": 0.5},
    {"time_s": 60, "no_aris_db": 0, "obfuscation_db": 0, "counter_aris_db": 0},
    {"time_s": 70, "no_aris_db": 2, "obfuscation_db": 5, "counter_aris_db": 1},
    {"time_s": 80, "no_aris_db": -1, "obfuscation_db": -3, "counter_aris_db": -0.5},
    {"time_s": 90, "no_aris_db": 3, "obfuscation_db": 4, "counter_aris_db": 1.5},
    {"time_s": 100, "no_aris_db": -2, "obfuscation_db": -5, "counter_aris_db": -1},
]

SECURE_COMMUNICATION = [
    {"receiver": "Bob", "condition": "ARIS-A active", "ser_percent": 0.0},
    {"receiver": "Eve", "condition": "No ARIS-B", "ser_percent": 74.8},
    {"receiver": "Eve", "condition": "ARIS-B optimized", "ser_percent": 0.2},
    {"receiver": "Bob", "condition": "ARIS-B optimized", "ser_percent": 0.0},
]

SENSING_ACCURACY = [
    {"condition": "No obfuscation", "accuracy_percent": 92},
    {"condition": "ARIS-A obfuscation", "accuracy_percent": 47},
    {"condition": "ARIS-B countermeasure", "accuracy_percent": 86},
]

ALGORITHM_OUTCOMES = [
    {"algorithm": "Greedy (GD)", "standalone_gain_db": 8.3, "battle_win_rate_percent": 53},
    {"algorithm": "Beamforming (BF)", "standalone_gain_db": 7.8, "battle_win_rate_percent": 62},
    {"algorithm": "Element flip (FL)", "standalone_gain_db": 5.1, "battle_win_rate_percent": 22},
    {"algorithm": "Random (RD)", "standalone_gain_db": 1.2, "battle_win_rate_percent": 12},
    {"algorithm": "No optimization", "standalone_gain_db": 0.0, "battle_win_rate_percent": 3},
]

TIMING_EFFECTS = [
    {"mode": "Independent optimization", "defender_win_rate_percent": 65, "attacker_win_rate_percent": 35},
    {"mode": "Reactive optimization", "defender_win_rate_percent": 55, "attacker_win_rate_percent": 45},
    {"mode": "Simultaneous optimization", "defender_win_rate_percent": 40, "attacker_win_rate_percent": 60},
]

HARDWARE_SWEEP = [
    {"aris_a_elements": 64, "aris_b_elements": 64, "gain_db": 0.0},
    {"aris_a_elements": 128, "aris_b_elements": 64, "gain_db": 2.1},
    {"aris_a_elements": 256, "aris_b_elements": 64, "gain_db": 4.8},
    {"aris_a_elements": 64, "aris_b_elements": 128, "gain_db": -2.3},
    {"aris_a_elements": 128, "aris_b_elements": 128, "gain_db": 0.0},
    {"aris_a_elements": 256, "aris_b_elements": 128, "gain_db": 2.7},
    {"aris_a_elements": 64, "aris_b_elements": 256, "gain_db": -5.1},
    {"aris_a_elements": 128, "aris_b_elements": 256, "gain_db": -2.9},
    {"aris_a_elements": 256, "aris_b_elements": 256, "gain_db": 0.0},
]

CHANNEL_EFFECTS = [
    {"condition": "Shallow water (50 m)", "aris_a_advantage_percent": 58, "aris_b_advantage_percent": 42},
    {"condition": "Deep water (200 m)", "aris_a_advantage_percent": 52, "aris_b_advantage_percent": 48},
    {"condition": "Multipath-rich", "aris_a_advantage_percent": 45, "aris_b_advantage_percent": 55},
    {"condition": "Thermocline present", "aris_a_advantage_percent": 42, "aris_b_advantage_percent": 58},
    {"condition": "High ambient noise", "aris_a_advantage_percent": 60, "aris_b_advantage_percent": 40},
]

EDGE_PERFORMANCE = [
    {"algorithm": "Centralized cloud", "convergence_time_s": 45.3, "energy_j": 128.5, "win_rate_percent": 67},
    {"algorithm": "Distributed greedy", "convergence_time_s": 12.8, "energy_j": 42.3, "win_rate_percent": 58},
    {"algorithm": "Bayesian optimization", "convergence_time_s": 18.9, "energy_j": 35.7, "win_rate_percent": 63},
    {"algorithm": "Consensus-based", "convergence_time_s": 8.5, "energy_j": 28.9, "win_rate_percent": 55},
    {"algorithm": "Random (baseline)", "convergence_time_s": 25.0, "energy_j": 15.0, "win_rate_percent": 12},
]

