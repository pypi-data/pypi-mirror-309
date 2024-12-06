from threading import Thread
from typing import Callable, Optional, Tuple

class ThreadManager:
    def __init__(self):
        self.exit_flag = False
        self.threads = []

    def start_thread(self, target: Callable, args: Tuple = (), on_finish: Optional[Callable] = None) -> None:
        """Start a thread with the given target function and arguments."""
        
        def wrapper():
            try:
                target(*args)
            finally:
                if on_finish:
                    on_finish()  # Call on_finish when the thread is done

        # Create a single thread that runs the wrapper function
        thread = Thread(target=wrapper)
        thread.daemon = True  # Mark the thread as a daemon
        thread.start()
        self.threads.append(thread)

    def stop_threads(self) -> None:
        """Immediately clear the threads and set the exit flag."""
        self.exit_flag = True
        for thread in self.threads:
            # Logic to stop threads if needed
            if thread.is_alive():
                pass
        self.threads.clear()

    def are_threads_alive(self) -> bool:
        """Check if any threads are alive."""
        return any(thread.is_alive() for thread in self.threads)

    def join_threads(self) -> None:
        """Wait for all threads to finish."""
        for thread in self.threads:
            thread.join()

    def run_threaded_tasks(self, tasks: list[dict]) -> None:
        """Run multiple tasks concurrently with optional finish functions."""
        for task in tasks:
            target = task.get('target')
            args = task.get('args', [])
            on_finish = task.get('on_finish', None)
            self.start_thread(target, tuple(args), on_finish=on_finish)

    def wait_for_threads(self) -> None:
        """Wait for all threads to finish."""
        for thread in self.threads:
            thread.join()  # Wait for each thread to finish
