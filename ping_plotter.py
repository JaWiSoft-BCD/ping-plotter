import matplotlib.pyplot as plt
import re
import numpy as np

def plot_ping_times(filename="ping_data.txt"):
    try:
        with open(filename, "r") as f:
            ping_times = []
            failures = []
            for i, line in enumerate(f):
                match = re.search(r"time=(\d+)ms", line)
                if match:
                    time = int(match.group(1))
                    ping_times.append(time)
                elif "Request timed out" in line or "Destination host unreachable" in line or "General failure" in line or "TTL expired in transit" in line or "No route to host" in line:
                    ping_times.append(None)
                    failures.append(i)

        if not ping_times:
            print("No ping times found in the file.")
            return

        plt.figure(figsize=(10, 6))

        # Convert ping_times to a NumPy array for easier masking
        ping_times_np = np.array(ping_times, dtype=float)  # Use float to handle None values

        # Plot the successful pings (where there's a valid time)
        valid_indices = ~np.isnan(ping_times_np)  # Indices where ping_times_np is NOT NaN
        plt.plot(np.arange(len(ping_times))[valid_indices], ping_times_np[valid_indices], marker='o', linestyle='-', label="Successful Pings")

        # Plot the failures as red 'x's on the line itself
        for i in failures:
            plt.plot(i, -10, marker='x', color='red', markersize=10, markeredgewidth=3)  # Plot 'x' below the graph

        plt.xlabel("Ping Number")
        plt.ylabel("Time (ms)")
        plt.title("Ping Times Over Time (with Failures)")
        plt.grid(True)

        min_time = np.nanmin(ping_times_np) if any(ping_times_np) else 0 # Use np.nanmin to ignore NaNs
        max_time = np.nanmax(ping_times_np) if any(ping_times_np) else 100
        padding = (max_time - min_time) * 0.2
        plt.ylim(max(0, min_time - padding), max_time + padding)

        plt.tight_layout()
        plt.legend()
        plt.savefig("ping_graph.png")
        print("Ping graph saved as ping_graph.png")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    plot_ping_times()
