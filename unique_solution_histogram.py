import matplotlib.pyplot as plt
from collections import defaultdict, Counter

# Dictionary mapping each position (0-8) to its valid neighbor indices on a 3x3 grid
NEIGHBORS = {
    0: (1, 3),       1: (0, 2, 4),    2: (1, 5),
    3: (0, 4, 6),    4: (1, 3, 5, 7), 5: (2, 4, 8),
    6: (3, 7),       7: (4, 6, 8),    8: (5, 7)
}

def get_multiplier(num_moves):
    """Returns the multiplier based on the structural rules."""
    if num_moves == 2:   # Corner
        return 2
    elif num_moves == 3: # Edge
        return 4
    elif num_moves == 4: # Center
        return 4
    return 1

def dfs(state, blank_idx, depth, max_depth, current_value, state_values):
    # Base Case: Reached the target depth (leaf node)
    if depth == max_depth:
        state_values[state].append(current_value)
        return

    # Determine the branching factor and multiplier for the CURRENT state
    moves = NEIGHBORS[blank_idx]
    num_moves = len(moves)
    multiplier = get_multiplier(num_moves)
    next_value = current_value * multiplier

    # Explore all valid moves
    for next_blank in moves:
        # Create the new board state by swapping the blank tile (0) with the neighbor
        state_list = list(state)
        state_list[blank_idx], state_list[next_blank] = state_list[next_blank], state_list[blank_idx]
        new_state = tuple(state_list)
        
        # Recursive DFS call
        dfs(new_state, next_blank, depth + 1, max_depth, next_value, state_values)

def analyze_and_plot_global_values(max_depth):
    initial_state = (0, 1, 2, 3, 4, 5, 6, 7, 8)
    initial_blank_idx = 0
    
    state_values = defaultdict(list)
    
    print(f"Running DFS for depth m = {max_depth}...\n")
    dfs(initial_state, initial_blank_idx, 0, max_depth, 1, state_values)
    
    # Constant numerator for the global value formula: 4^m
    numerator = 4 ** max_depth
    
    # Store global values for the histogram
    global_values_list = []
    
    # Data structure to organize states before printing
    processed_states = []
    
    for state, values in state_values.items():
        times_reached = len(values)
        value_counts = Counter(values)
        
        # Compute the Global Value: sum of ((4^m) / Value) * repetition
        global_value = sum((numerator / val) * count for val, count in value_counts.items())
        
        # Add to our list for the plot
        global_values_list.append(global_value)
        
        # Save to list for sorting and terminal printing
        processed_states.append({
            'state': state,
            'times_reached': times_reached,
            'value_counts': value_counts,
            'global_value': global_value
        })

    # Sort the output by times reached (descending), then by global value
    processed_states.sort(key=lambda x: (x['times_reached'], x['global_value']), reverse=True)
    
    print("-" * 80)
    print(f"ALL REACHED CONFIGURATIONS AT DEPTH m = {max_depth}")
    print("-" * 80)
    print(f"Total unique states at leaves: {len(processed_states)}")
    print("Formula Used: sum( (4^m / Value) * repetition )")
    print("-" * 80 + "\n")
    
    for i, data in enumerate(processed_states, 1):
        state = data['state']
        
        # Format the value repetitions for the terminal
        breakdown_str = ", ".join([f"Value {val} repeats {count}x" for val, count in sorted(data['value_counts'].items())])
        
        # Format the state as a readable 3x3 grid string
        grid_str = f"[{state[0]} {state[1]} {state[2]}] " \
                   f"[{state[3]} {state[4]} {state[5]}] " \
                   f"[{state[6]} {state[7]} {state[8]}]"
        
        print(f"{i:03d}. Grid: {grid_str}")
        print(f"     Total Times Reached:  {data['times_reached']} times")
        print(f"     Value Repetitions:    [{breakdown_str}]")
        # Print the computed Global Value
        print(f"     Global Value:         {data['global_value']:.2f}")
        print("-" * 80)
        
    # --- PLOTTING THE HISTOGRAM ---
    print("\nGenerating histogram...")
    plt.figure(figsize=(10, 6))
    
    # Create the histogram
    counts, bins, patches = plt.hist(global_values_list, bins=100, color='#4A90E2', edgecolor='black', alpha=0.8)
    
    # Add labels and styling
    plt.title(f"Histogram  (Depth m = {max_depth})", fontsize=14, fontweight='bold')
    # plt.xlabel("\kappa", fontsize=12)
    plt.ylabel("Frequency (Number of Unique States)", fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Display the plot window
    plt.tight_layout()
    plt.show()

# Run the script
if __name__ == "__main__":
    # Setting depth to 4 as requested in your example
    DEPTH = 10 
    
    analyze_and_plot_global_values(max_depth=DEPTH)