import random
import pandas as pd
import matplotlib.pyplot as plt

class Gacha:
    def __init__(self):
        self.card_data = []
        self.total_probability = 0.0

    def init_random(self, seed):
        """Initialize the random number generator with a given seed."""
        random.seed(seed)

    def init_gifts(self, gifts_data):
        """Register gift data and calculate cumulative probabilities."""
        self.card_data = gifts_data
        self.total_probability = sum(gift['prob'] for gift in gifts_data)

    def draw(self):
        """Simulate a gacha draw and return the result index."""
        draw_value = random.uniform(0, self.total_probability)
        cumulative = 0.0

        for i, gift in enumerate(self.card_data):
            cumulative += gift['prob']
            if draw_value <= cumulative:
                return i
        return len(self.card_data) - 1  # Default to the last item if not found

# Parameters
trials = 10000  # Number of trials
cost_per_gacha = 100  # Cost per gacha
bin_width = 50000  # Width for frequency distribution bins

# Define gifts data
gifts = [
    {"prob": 1.0, "name": "Emperor"},
    {"prob": 10.0, "name": "King"},
    {"prob": 30.0, "name": "Adelie"},
    {"prob": 100.0, "name": "Gentoo"},
    {"prob": 200.0, "name": "N-Rockhopper"},
    {"prob": 500.0, "name": "Cape"},
    {"prob": 1159.0, "name": "Humboldt"},
]

# Gacha simulation setup
gacha = Gacha()
gacha.init_random(1234)
gacha.init_gifts(gifts)

# Simulate gacha draws
def simulate_gacha(trials, cost_per_gacha):
    random.seed()
    sum_trials = []
    min_cost = float('inf')
    max_cost = 0
    total_cost = 0

    for _ in range(trials):
        flags = [0] * len(gifts)
        n = 0
        cost = 0

        while n != len(gifts):  # Continue until all gifts are collected
            result = gacha.draw()
            cost += cost_per_gacha
            if flags[result] == 0:
                flags[result] = 1

            n = sum(flags)

        sum_trials.append(cost)
        total_cost += cost

        # Update min and max costs
        if cost < min_cost:
            min_cost = cost
        if cost > max_cost:
            max_cost = cost

    avg_cost = total_cost / trials
    return sum_trials, min_cost, max_cost, avg_cost

# Run the simulation
sum_trials, min_cost, max_cost, avg_cost = simulate_gacha(trials, cost_per_gacha)

# Display results
print(f"Cost per gacha: {cost_per_gacha} yen")
print(f"Number of trials: {trials}")
print(f"Minimum cost to complete: {min_cost} yen")
print(f"Maximum cost to complete: {max_cost} yen")
print(f"Average cost to complete: {avg_cost} yen")


# Create a frequency distribution
width_count = (max_cost + bin_width) // bin_width
distribution = [0] * (width_count + 1)

for cost in sum_trials:
    index = cost // bin_width
    if index < len(distribution):
        distribution[index] += 1

# Prepare data for CSV
csv_data = {"Range (in 1000 yen)": [], "Frequency": []}
for i in range(len(distribution)):
    lower_bound = (bin_width * i) // 1000
    upper_bound = ((bin_width * (i + 1) - 1) // 1000)
    if i == len(distribution) - 1:
        csv_data["Range (in 1000 yen)"].append(f"{lower_bound}--")
    else:
        csv_data["Range (in 1000 yen)"].append(f"{lower_bound}--{upper_bound}")
    csv_data["Frequency"].append(distribution[i])

# Create a DataFrame and save to CSV
df = pd.DataFrame(csv_data)
csv_path = "/Users/Desktop/Gacha-Simulation/gacha_simulation.csv"  # Save in the current directory
                                                                   # Please change to any file path
df.to_csv(csv_path, index=False)

# Plot the distribution
plt.figure(figsize=(12, 6))
plt.bar(csv_data["Range (in 1000 yen)"], csv_data["Frequency"], color='lightblue')
plt.xlabel("Cost Range (in 1000 yen)")
plt.ylabel("Frequency")
plt.title("Frequency Distribution of Gacha Costs")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save the plot
plot_path = "/Users/Desktop/Gacha-Simulation/Simulation Result_Example.png"  # Save in the current directory
                                                                             # Please change to any file path
plt.savefig(plot_path)
