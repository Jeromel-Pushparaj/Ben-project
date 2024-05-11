# import time

# def my_function():
#     print("This is my function!")

# # Delay function
# def run_with_delay(func, delay_seconds):
#     print(f"Function will run with a delay of {delay_seconds} seconds.")
#     time.sleep(delay_seconds)
#     func()

# # Example usage
# delay_seconds = 3
# run_with_delay(my_function, delay_seconds)

import time

def my_function():
    print("This is my function!")

# Function to run another function repeatedly with a delay
def run_repeatedly_with_delay(func, delay_seconds, num_iterations):
    for i in range(num_iterations):
        print(f"Iteration {i+1}:")
        func()
        time.sleep(delay_seconds)

# Example usage
delay_seconds = 3
num_iterations = 5
run_repeatedly_with_delay(my_function, delay_seconds, num_iterations)
