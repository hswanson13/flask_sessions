"""
Example script to illustrate how a global `LocalStack` object can be used
when working with multiple threads.
"""
import random
import threading
import time

from werkzeug.local import LocalStack

# Create a global LocalStack object for storing data about each thread
thread_data_stack = LocalStack()

def long_running_function(thread_index: int):
    """Simulates a long-running function by using time.sleep()."""

    thread_data_stack.push({'index': thread_index, 'thread_id': threading.get_native_id()})
    print(f'Starting thread #{thread_index}... {thread_data_stack}')

    time.sleep(random.randrange(1, 11))

    print(f'LocalStack contains: {thread_data_stack.top}')
    print(f'Finished thread #{thread_index}!')
    thread_data_stack.pop()


if __name__ == "__main__":
    threads = []

    # Create and start 3 threads that each run long_running_function()
    for index in range(3):
        thread = threading.Thread(target=long_running_function, args=(index,))
        threads.append(thread)
        thread.start()

    # Wait until each thread terminates before the script exits by
    # 'join'ing each thread
    for thread in threads:
        thread.join()

    print('Done!')