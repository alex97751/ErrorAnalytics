import re
import sys
import random

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from collections import defaultdict

# Extracts the notebook name from the log file based on '/autograded' path
def extract_notebook_name(log_file):
    pattern = re.compile(r"/([^/]+)/autograded")
    
    with open(log_file, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                return match.group(1)
    return "Unknown Notebook"

# Counts the number of submissions from the log file
def count_submissions(log_file, phrase="Creating"):
    count = 0
    with open(log_file, 'r') as file:
        count = sum(line.count(phrase) for line in file)
    return count

# Extracts pattern counts from the log file
def find_patterns(log_file, pattern_matcher):
    pattern_counts = defaultdict(int)
    pattern_regex = re.compile(r"'evalue': '" + pattern_matcher + "_(.*?)'")
    
    with open(log_file, 'r') as file:
        for line in file:
            matches = pattern_regex.findall(line)
            for match in matches:
                pattern_counts[match] += 1

    return pattern_counts

# Plots the data using matplotlib
def plot_pattern_counts(pattern_counts, student_count, pattern_descriptions, title, threshold):
    patterns = list(pattern_counts.keys())
    counts = list(pattern_counts.values())

    colors = [(random.uniform(0, 0.5), random.uniform(0, 0.8), 1) for _ in patterns]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_facecolor('#F7F6F6') 
    
    bar_width = 0.6
    bars = ax.bar(patterns, counts, width=bar_width, color=colors, edgecolor='black')

    ax.set_xlabel('Patterns')
    ax.set_ylabel('Affected Students')
    ax.set_title(f'Pattern Distribution in {title}')
    ax.set_xticks(range(len(patterns)))
    ax.set_xticklabels(patterns, rotation=45, ha='right')
    ax.set_ylim(0, student_count)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.grid(axis='y', linestyle='--', color='gray', alpha=0.3)

    legend_labels = [f"{pattern}: {desc}" for pattern, desc in pattern_descriptions.items()]
    ax.legend(bars, legend_labels, loc='upper right', bbox_to_anchor=(1.3, 1), frameon=False)

    plt.tight_layout()

    plt.show()

def main():
    log_file = sys.argv[1] if len(sys.argv) > 1 else "log.txt"
    pattern_matcher = sys.argv[2] if len(sys.argv) > 2 else "Pattern"

    threshold = 1

    notebook_title = extract_notebook_name(log_file)
    student_count =count_submissions(log_file)
    print(f'Total Students: {student_count}')

    pattern_data = find_patterns(log_file, pattern_matcher)
    pattern_counts = {}
    pattern_descriptions = {}

    for pattern, count in pattern_data.items():
        pattern_num, desc = pattern.split(": ", 1)
        pattern_key = f"Pattern {pattern_num}"
        pattern_counts[pattern_key] = count
        pattern_descriptions[pattern_key] = desc

        print(f"{pattern_key}: {count} students affected (Description: {desc})")

    # Appy threshold if needed
    if threshold > 1:
        removed_entries = [key for key, value in pattern_counts.items() if value < threshold]
        pattern_counts = {key: value for key, value in pattern_counts.items() if value >= threshold}
        for key in removed_entries:
            if key in pattern_descriptions:
                del pattern_descriptions[key]   

    # Plot the pattern distribution
    plot_pattern_counts(pattern_counts, student_count, pattern_descriptions, notebook_title, threshold)

if __name__ == "__main__":
    main()
