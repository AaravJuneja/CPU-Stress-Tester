import multiprocessing
import time
import random
import psutil

def cpu_intensive_task(duration, process_id):
    start_time = time.time()
    while time.time() - start_time < duration:
        # Simulate CPU-intensive workload
        for _ in range(10000):
            for _ in range(10000):
                result = 0
                for i in range(10000):
                    result += i * i
        time.sleep(0.1)  # Sleep for a short period to avoid excessive CPU usage

    print(f"Process {process_id} completed.")

def run_cpu_stress_test(num_threads, duration):
    print("Running CPU Stress Test...")
    print("Progress:")

    processes = []
    for i in range(num_threads):
        p = multiprocessing.Process(target=cpu_intensive_task, args=(duration, i+1))
        p.start()
        processes.append(p)

    start_time = time.time()
    while time.time() - start_time < duration:
        completed_processes = sum(not p.is_alive() for p in processes)
        progress = (completed_processes / num_threads) * 100
        print(f"  {progress:.2f}% complete  |  {completed_processes}/{num_threads} processes completed", end="\r", flush=True)
        time.sleep(1)
        progress += random.uniform(0.1, 1.0)  # Increase progress by a random number

    for p in processes:
        p.terminate()
        p.join()

    print("\nCPU Stress Test completed.")

    # Provide performance feedback
    cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
    avg_cpu_usage = sum(cpu_usage) / len(cpu_usage)
    max_cpu_usage = max(cpu_usage)

    print("Performance Feedback:")
    print(f"Average CPU Usage: {avg_cpu_usage}%")
    print(f"Max CPU Usage: {max_cpu_usage}%")

    # Additional feedback on CPU performance
    if avg_cpu_usage <= 50:
        print("The CPU performance during the stress test was excellent.")
    elif avg_cpu_usage <= 80:
        print("The CPU performance during the stress test was good.")
    else:
        print("The CPU performance during the stress test was moderate.")

    if max_cpu_usage <= 70:
        print("The CPU handled the peak workload very well.")
    elif max_cpu_usage <= 90:
        print("The CPU handled the peak workload well.")
    else:
        print("The CPU reached its maximum capacity during the stress test.")

    # Check if any CPU cores were heavily loaded
    heavily_loaded_cores = [core for core, usage in enumerate(cpu_usage) if usage > 80]
    if heavily_loaded_cores:
        print("The following CPU cores were heavily loaded during the stress test:")
        for core in heavily_loaded_cores:
            print(f"Core {core + 1}")
    else:
        print("All CPU cores handled the workload evenly.")

    print()

def get_cpu_info():
    cpu_info = {
        "Physical cores": psutil.cpu_count(logical=False),
        "Total cores": psutil.cpu_count(logical=True),
        "CPU frequency": psutil.cpu_freq().current,
        "CPU usage": psutil.cpu_percent(interval=1, percpu=True)
    }
    return cpu_info

def display_cpu_info(cpu_info):
    print("CPU Information:")
    for key, value in cpu_info.items():
        print(f"{key}: {value}")
    print()

def display_menu():
    print("CPU Stress Testing Tool Menu:")
    print("1. Run CPU Stress Test")
    print("2. Display CPU Information")
    print("3. Exit")

def validate_input(input_str, valid_range):
    try:
        choice = int(input_str)
        if choice in valid_range:
            return choice
        else:
            raise ValueError
    except ValueError:
        return None

if __name__ == "__main__":
    cpu_info = get_cpu_info()
    display_cpu_info(cpu_info)

    while True:
        display_menu()
        choice = validate_input(input("Enter your choice: "), range(1, 4))

        if choice == 1:
            num_threads = int(input("Enter the number of threads: "))
            duration = int(input("Enter the duration of the stress test (in seconds): "))
            run_cpu_stress_test(num_threads, duration)
        elif choice == 2:
            display_cpu_info(cpu_info)
        elif choice == 3:
            print("Exiting the CPU Stress Testing Tool...")
            break
        else:
            print("Invalid choice! Please try again.")