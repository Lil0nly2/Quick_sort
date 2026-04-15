import random
import time
import sys

sys.setrecursionlimit(2000000)


# ---------------- BASE CLASS ----------------
class SortExperiment:
    """
    Base class for sorting experiments.
    Tracks swaps.
    """

    def __init__(self):
        self.swap_count = 0

    def reset_counters(self):
        self.swap_count = 0


# ---------------- QUICK SORT CLASS ----------------
class QuickSortExperiment(SortExperiment):
    """
    QuickSort implementation with different pivot strategies.
    Inherited
    """

    def __init__(self, pivot_type):
        super().__init__()
        self.pivot_type = pivot_type

    def partition(self, arr, low, high):
        """
        Partition the array using the selected pivot strategy.
        Returns the pivot index.
        """

        # Choose pivot
        if self.pivot_type == "first":
            pivot_index = low
        elif self.pivot_type == "last":
            pivot_index = high
        else:
            pivot_index = random.randint(low, high)

        # Move pivot to end
        if pivot_index != high:
            arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
            self.swap_count += 1

        pivot = arr[high]
        i = low - 1

        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                if i != j:
                    arr[i], arr[j] = arr[j], arr[i]
                    self.swap_count += 1

        # Place pivot in correct position
        if (i + 1) != high:
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            self.swap_count += 1

        return i + 1

    def quick_sort(self, arr, low, high):
        """
        QuickSort.
        """

        while low < high:
            pi = self.partition(arr, low, high)

            # Recurse on smaller partition first
            if pi - low < high - pi:
                self.quick_sort(arr, low, pi - 1)
                low = pi + 1
            else:
                self.quick_sort(arr, pi + 1, high)
                high = pi - 1

    def sort(self, arr):
        """
        to sort the array.
        """
        self.quick_sort(arr, 0, len(arr) - 1)


# ---------------- INPUT GENERATOR ----------------
class InputGenerator:
    """
    Generates different types of input arrays.
    """

    def generate(input_type, size):
        if input_type == "increasing":
            return list(range(size))
        elif input_type == "decreasing":
            return list(range(size, 0, -1))
        else:
            return random.sample(range(size), size)


# ---------------- EXPERIMENT RUNNER ----------------
class ExperimentRunner:
    """
    Runs experiments for different sizes, inputs, and pivot strategies.
    """

    def __init__(self, sizes, input_types, pivot_types):
        self.sizes = sizes
        self.input_types = input_types
        self.pivot_types = pivot_types

    def run(self):
        results = {}

        for input_type in self.input_types:
            results[input_type] = {}

            for pivot in self.pivot_types:
                sorter = QuickSortExperiment(pivot)
                results[input_type][pivot] = []

                for size in self.sizes:
                    arr = InputGenerator.generate(input_type, size)
                    working_array = arr.copy()

                    sorter.reset_counters()

                    print(f"Running: N={size}, Input={input_type}, Pivot={pivot}")

                    start = time.time()
                    sorter.sort(working_array)
                    end = time.time()

                    result = {
                        "swaps": sorter.swap_count,
                        "time": end - start
                    }

                    print(
                        f"Swaps={result['swaps']},  "
                        f"Time={result['time']}s\n"
                    )

                    results[input_type][pivot].append(result)

        return results


# ---------------- MAIN ----------------
if __name__ == "__main__":
    sizes = [10000,100000,1000000]
    input_types = ["increasing", "decreasing", "random"]
    pivot_types = ["first", "last", "random"]

    runner = ExperimentRunner(sizes, input_types, pivot_types)
    results = runner.run()