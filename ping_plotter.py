import matplotlib.pyplot as plt
import re

def plot_ping_times(filename="ping_data.txt"):
    """Reads ping data from a file, plots the times, and saves the graph.

    Args:
        filename: The name of the text file containing the ping data.
    """

    try:
        with open(filename, "r") as f:
            ping_times = []
            for line in f:
                match = re.search(r"time=(\d+)ms", line)
                if match:
                    time = int(match.group(1))
                    ping_times.append(time)

        if not ping_times:
            print("No ping times found in the file.")
            return

        # Create the plot
        plt.figure(figsize=(10, 6))  # Adjust figure size for better visualization
        plt.plot(ping_times, marker='o', linestyle='-')

        plt.xlabel("Ping Number")
        plt.ylabel("Time (ms)")
        plt.title("Ping Times Over Time")
        plt.grid(True)  # Add grid for better readability

        # Improve y-axis scaling for fluctuations
        min_time = min(ping_times)
        max_time = max(ping_times)
        padding = (max_time - min_time) * 0.2  # Add some padding to the y-axis
        plt.ylim(max(0, min_time - padding), max_time + padding) # Ensure y-axis doesn't start at a large negative value

        plt.tight_layout() # Adjust layout to prevent labels from overlapping

        # Save the figure
        plt.savefig("ping_graph.png")  # Save as PNG
        print("Ping graph saved as ping_graph.png")

        # Optionally display the graph (if you're running in an environment that supports it)
        # plt.show()

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    plot_ping_times()  # You can specify the filename if it's different
