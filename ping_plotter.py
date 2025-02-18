import matplotlib.pyplot as plt
import re
import numpy as np

def plot_ping_times(filename="ping_data.txt"):
    try:
        with open(filename, "r") as f:
            ping_times = []
            failures = []
            ip_address = None  # Store the IP address
            for i, line in enumerate(f):
                match = re.search(r"Reply from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", line)
                if match and ip_address is None:  # Extract IP only once
                    ip_address = match.group(1)
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

        ping_times_np = np.array(ping_times, dtype=float)
        valid_indices = ~np.isnan(ping_times_np)
        plt.plot(np.arange(len(ping_times))[valid_indices], ping_times_np[valid_indices], marker='o', linestyle='-', label="Successful Pings")

        failure_proxy = plt.Line2D([0], [0], marker='x', color='red', markersize=10, markeredgewidth=3, linestyle="None")
        for i in failures:
            plt.plot(i, -10, marker='x', color='red', markersize=10, markeredgewidth=3)

        plt.xlabel("Ping Number")
        plt.ylabel("Time (ms)")
        plt.title(f"Ping Times Over Time (with Failures)") # Removed IP from title
        plt.grid(True)

        min_time = np.nanmin(ping_times_np) if any(ping_times_np) else 0
        max_time = np.nanmax(ping_times_np) if any(ping_times_np) else 100
        padding = (max_time - min_time) * 0.2
        plt.ylim(max(0, min_time - padding), max_time + padding)

        plt.tight_layout()

        # Add information to the bottom of the plot
        plt.figtext(0.5, 0.01, f"IP Address: {ip_address} | Pings: {len(ping_times)} | Failures: {len(failures)}", ha="center", fontsize=10)

        plt.legend(handles=[plt.gca().lines[0], failure_proxy], labels=["Successful Pings", "Ping Failures"])
        plt.savefig("ping_graph.png")
        print("Ping graph saved as ping_graph.png")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    plot_ping_times()
