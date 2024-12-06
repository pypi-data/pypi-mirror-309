import numpy as np
import matplotlib.pyplot as plt

def plot_distribution(data, ground_truth, positions = [0.5, 1.5], y_start = None, y_limit = [10, 10]):

    if y_start == None:
        y_start = np.min(data)-10
    
    data1 = data
    data2 = [np.median(data), ground_truth]
    positions = [positions[0], positions[1]]
    sorted_data1 = np.sort(data1)
    median_value = np.median(sorted_data1)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

    ax1.bar(range(len(data1)), sorted_data1, color="skyblue", edgecolor="black")
    median_index = np.where(sorted_data1 == median_value)[0][0]
    ax1.bar(median_index, median_value, color="red", edgecolor="black", label="Median", alpha=0.7)

    ax1.set_ylim(y_start, np.max(sorted_data1) + y_limit[0])
    ax1.set_title("Distribution of patches' predictions for a single image") 
    ax1.set_xlabel("Order")
    ax1.set_ylabel("Age (months)")
    ax1.legend()

    bar_colors = ['red', 'blue']
    labels = ['Median', 'Ground Truth']

    difference = abs(data2[1] - data2[0])
    bars = ax2.bar(positions, data2, width=0.4, color=bar_colors, edgecolor="black", label=labels)
    ax2.annotate('', xy=(positions[0], data2[0]), xytext=(positions[0], data2[0] + 5),
                arrowprops=dict(facecolor='black', shrink=0.05))
    ax2.text(0.37, data2[0] + 6, 'Our prediction', fontsize=12)
    
    ax2.plot([1, 1], [data2[0], data2[1]], color="black", lw=2)

    ax2.plot([0.95, 1.05], [data2[0], data2[0]], color="black", lw=2)
    ax2.plot([0.95, 1.05], [data2[1], data2[1]], color="black", lw=2)
    difference = abs(data2[1] - data2[0])
    ax2.text(1.05, (data2[0] + data2[1]) / 2, f"{difference:.3f}", fontsize=12, color="black")

    ax2.set_xticks([])
    
    ax2.set_ylim(y_start, max(median_value, ground_truth) + y_limit[1])
    ax2.set_title("Our Prediction vs Ground Truth")
    ax2.set_ylabel("Age (months)")
    ax2.legend()

    plt.tight_layout()
    plt.show()
