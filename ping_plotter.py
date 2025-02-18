import matplotlib.pyplot as plt
import re

def plot_ping_times(filename="ping_data.txt"):
    """Reads ping data, plots times, marks failures, and saves the graph.

    Args:
        filename: The name of the text file containing the ping data.
    """

    try:
        with open(filename, "r") as f:
            ping_times = []
            failures = []  # List to store indices of failed pings
            for i, line in enumerate(f):
                match = re.search(r"time=(\d+)ms", line)
                if match:
                    time = int(match.group(1))
                    ping_times.append(time)
                elif "Request timed out" in line or "Destination host unreachable" in line or "General failure" in line: # Add more failure conditions as needed
                    ping_times.append(None) # Append None for failed pings to handle plotting
                    failures.append(i)
                # You can add more conditions here based on your ping output format.
                elif "TTL expired in transit" in line:
                    ping_times.append(None)
                    failures.append(i)
                elif "No route to host" in line:
                    ping_times.append(None)
                    failures.append(i)



        if not ping_times:
            print("No ping times found in the file.")
            return

        plt.figure(figsize=(10, 6))
        plt.plot(ping_times, marker='o', linestyle='-', label="Successful Pings")

        # Mark failures in red
        if failures:
          failure_times = [ping_times[i] if i < len(ping_times) else None for i in failures] # Get y-values for failures, handle potential index errors
          plt.scatter(failures, failure_times, color='red', marker='x', s=100, label="Ping Failures") # Increased marker size for visibility

        plt.xlabel("Ping Number")
        plt.ylabel("Time (ms)")
        plt.title("Ping Times Over Time (with Failures)")
        plt.grid(True)

        min_time = min(filter(lambda x: x is not None, ping_times)) if any(ping_times) else 0 # Handle cases where all pings fail
        max_time = max(filter(lambda x: x is not None, ping_times)) if any(ping_times) else 100 # Default max time if all fail
        padding = (max_time - min_time) * 0.2
        plt.ylim(max(0, min_time - padding), max_time + padding)

        plt.tight_layout()
        plt.legend()  # Show the legend
        plt.savefig("ping_graph.png")
        print("Ping graph saved as ping_graph.png")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    plot_ping_times()
