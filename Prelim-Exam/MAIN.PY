import csv
import time
import sys
import threading
from typing import List, Tuple, Any
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkinter import font as tkFont

class SortingBenchmark:
    """A comprehensive benchmarking tool for sorting algorithms."""
    
    def __init__(self, csv_file_path: str):
        """Initialize the benchmark tool with a CSV file path."""
        self.csv_file_path = csv_file_path
        self.data = []
        self.load_time = 0
        self.sort_time = 0
        
    def load_csv(self, num_rows: int = None) -> float:
        """
        Load the CSV file into memory.
        
        Args:
            num_rows: Number of rows to load. If None, loads all rows.
            
        Returns:
            Time taken to load the file in seconds.
        """
        start_time = time.time()
        self.data = []
        
        try:
            with open(self.csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                row_count = 0
                
                for row in reader:
                    if num_rows and row_count >= num_rows:
                        break
                    
                    self.data.append(row)
                    row_count += 1
                    
                    # Progress indicator
                    if row_count % 10000 == 0:
                        print(f"  Loaded {row_count:,} records...", end='\r')
            
            if self.data:
                print(f"  ✓ Successfully loaded {len(self.data):,} records")
            
        except FileNotFoundError:
            print(f"Error: File '{self.csv_file_path}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"Error loading CSV: {e}")
            sys.exit(1)
        
        self.load_time = time.time() - start_time
        return self.load_time
    
    def bubble_sort(self, key: str, reverse: bool = False) -> List[dict]:
        """
        Bubble Sort algorithm - O(n²) complexity.
        
        Args:
            key: Column name to sort by.
            reverse: If True, sort in descending order.
            
        Returns:
            Sorted list of records.
        """
        arr = [row.copy() for row in self.data]
        n = len(arr)
        
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if self._compare(arr[j], arr[j + 1], key, reverse):
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
            
            if not swapped:
                break
            
            # Progress indicator
            if (i + 1) % max(1, n // 10) == 0:
                progress = (i + 1) / n * 100
                print(f"  Bubble Sort Progress: {progress:.1f}%", end='\r')
        
        print("  ✓ Bubble Sort complete")
        return arr
    
    def insertion_sort(self, key: str, reverse: bool = False) -> List[dict]:
        """
        Insertion Sort algorithm - O(n²) complexity.
        
        Args:
            key: Column name to sort by.
            reverse: If True, sort in descending order.
            
        Returns:
            Sorted list of records.
        """
        arr = [row.copy() for row in self.data]
        
        for i in range(1, len(arr)):
            key_item = arr[i]
            j = i - 1
            
            while j >= 0 and self._compare(arr[j], key_item, key, reverse):
                arr[j + 1] = arr[j]
                j -= 1
            
            arr[j + 1] = key_item
            
            # Progress indicator
            if i % max(1, len(arr) // 10) == 0:
                progress = i / len(arr) * 100
                print(f"  Insertion Sort Progress: {progress:.1f}%", end='\r')
        
        print("  ✓ Insertion Sort complete")
        return arr
    
    def merge_sort(self, key: str, reverse: bool = False) -> List[dict]:
        """
        Merge Sort algorithm - O(n log n) complexity.
        
        Args:
            key: Column name to sort by.
            reverse: If True, sort in descending order.
            
        Returns:
            Sorted list of records.
        """
        arr = [row.copy() for row in self.data]
        
        self._merge_sort_helper(arr, 0, len(arr) - 1, key, reverse)
        print("  ✓ Merge Sort complete")
        return arr
    
    def _merge_sort_helper(self, arr: List[dict], left: int, right: int, 
                          key: str, reverse: bool) -> None:
        """Helper function for merge sort using divide and conquer."""
        if left < right:
            mid = (left + right) // 2
            self._merge_sort_helper(arr, left, mid, key, reverse)
            self._merge_sort_helper(arr, mid + 1, right, key, reverse)
            self._merge(arr, left, mid, right, key, reverse)
    
    def _merge(self, arr: List[dict], left: int, mid: int, right: int, 
               key: str, reverse: bool) -> None:
        """Merge operation for merge sort."""
        left_arr = arr[left:mid + 1]
        right_arr = arr[mid + 1:right + 1]
        
        i = j = 0
        k = left
        
        while i < len(left_arr) and j < len(right_arr):
            if not self._compare(left_arr[i], right_arr[j], key, reverse):
                arr[k] = left_arr[i]
                i += 1
            else:
                arr[k] = right_arr[j]
                j += 1
            k += 1
        
        while i < len(left_arr):
            arr[k] = left_arr[i]
            i += 1
            k += 1
        
        while j < len(right_arr):
            arr[k] = right_arr[j]
            j += 1
            k += 1
    
    def _compare(self, row1: dict, row2: dict, key: str, reverse: bool) -> bool:
        """
        Compare two rows based on the specified key.
        Handles both integer and string comparisons.
        
        Returns True if row1 should come after row2 (for ascending order).
        """
        val1 = row1[key]
        val2 = row2[key]
        
        # Try to convert to integer for ID column
        if key == 'ID':
            val1 = int(val1)
            val2 = int(val2)
        
        if reverse:
            return val1 < val2
        else:
            return val1 > val2
    
    def display_results(self, sorted_data: List[dict], algorithm: str, 
                       key: str, num_rows: int) -> None:
        """Display the sorting results."""
        print("\n" + "="*80)
        print(f"SORTING RESULTS - {algorithm}")
        print("="*80)
        print(f"Column sorted: {key}")
        print(f"Total records sorted: {len(sorted_data):,}")
        print(f"Load time: {self.load_time:.4f} seconds")
        print(f"Sort time: {self.sort_time:.4f} seconds")
        print(f"Total time: {self.load_time + self.sort_time:.4f} seconds")
        print("="*80)
        print("\nFirst 10 records:")
        print("-"*80)
        
        # Print headers
        if sorted_data:
            headers = list(sorted_data[0].keys())
            col_widths = {h: max(len(h), 15) for h in headers}
            
            header_str = " | ".join(f"{h:^{col_widths[h]}}" for h in headers)
            print(header_str)
            print("-"*80)
            
            # Print first 10 rows
            for i, row in enumerate(sorted_data[:10]):
                row_str = " | ".join(f"{str(row[h]):^{col_widths[h]}}" for h in headers)
                print(f"{i+1:2}. {row_str}")
        
        print("-"*80 + "\n")
    
    def benchmark(self, algorithm: str, column: str, num_rows: int, 
                 reverse: bool = False) -> List[dict]:
        """
        Run a benchmark test with the specified algorithm.
        
        Args:
            algorithm: Name of sorting algorithm ('bubble', 'insertion', 'merge').
            column: Column to sort by ('ID', 'FirstName', 'LastName').
            num_rows: Number of rows to process.
            reverse: If True, sort in descending order.
            
        Returns:
            Sorted data.
        """
        print(f"\nLoading data...")
        self.load_csv(num_rows)
        
        # Check for performance warnings
        if len(self.data) > 50000 and algorithm in ['bubble', 'insertion']:
            print(f"\n⚠️  WARNING: {algorithm.upper()} sort with {len(self.data):,} records")
            print("   This O(n²) algorithm may take a very long time!")
            response = input("   Continue? (y/n): ").strip().lower()
            if response != 'y':
                print("   Benchmark cancelled.")
                return []
        
        print(f"\nRunning {algorithm.upper()} Sort...")
        start_time = time.time()
        
        if algorithm.lower() == 'bubble':
            sorted_data = self.bubble_sort(column, reverse)
        elif algorithm.lower() == 'insertion':
            sorted_data = self.insertion_sort(column, reverse)
        elif algorithm.lower() == 'merge':
            sorted_data = self.merge_sort(column, reverse)
        else:
            print(f"Unknown algorithm: {algorithm}")
            return []
        
        self.sort_time = time.time() - start_time
        self.display_results(sorted_data, algorithm.upper(), column, num_rows)
        
        return sorted_data


class BenchmarkGUI:
    """GUI for the Sorting Algorithm Benchmarking Tool."""
    
    def __init__(self, root):
        """Initialize the GUI."""
        self.root = root
        self.root.title("Sorting Algorithm Benchmarking Tool")
        self.root.geometry("1000x800")
        self.root.resizable(True, True)
        
        self.csv_file = r"c:\Users\aaron Jamez\OneDrive\Desktop\2ND YEAR\generated_data.csv"
        self.benchmark = SortingBenchmark(self.csv_file)
        self.is_running = False
        
        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface."""
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Title
        title_font = tkFont.Font(family="Helvetica", size=16, weight="bold")
        title_label = ttk.Label(
            main_frame,
            text="Sorting Algorithm Benchmarking Tool",
            font=title_font
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Control Frame
        control_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="10")
        control_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        control_frame.columnconfigure(1, weight=1)
        
        # Algorithm Selection
        ttk.Label(control_frame, text="Algorithm:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.algorithm_var = tk.StringVar(value="merge")
        algorithm_frame = ttk.Frame(control_frame)
        algorithm_frame.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        for algo in ["bubble", "insertion", "merge"]:
            ttk.Radiobutton(
                algorithm_frame,
                text=algo.capitalize(),
                variable=self.algorithm_var,
                value=algo
            ).pack(side=tk.LEFT, padx=10)
        
        # Column Selection
        ttk.Label(control_frame, text="Sort Column:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.column_var = tk.StringVar(value="ID")
        column_combo = ttk.Combobox(
            control_frame,
            textvariable=self.column_var,
            values=["ID", "FirstName", "LastName"],
            state="readonly",
            width=15
        )
        column_combo.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Number of Rows
        ttk.Label(control_frame, text="Number of Rows:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.rows_var = tk.StringVar(value="1000")
        rows_spinbox = ttk.Spinbox(
            control_frame,
            from_=1,
            to=100000,
            textvariable=self.rows_var,
            width=15
        )
        rows_spinbox.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Button Frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
        self.run_button = ttk.Button(
            button_frame,
            text="Run Benchmark",
            command=self.run_benchmark
        )
        self.run_button.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5)
        
        clear_button = ttk.Button(
            button_frame,
            text="Clear Output",
            command=self.clear_output
        )
        clear_button.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate'
        )
        self.progress_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.progress_label = ttk.Label(main_frame, text="Ready")
        self.progress_label.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        # Output Frame
        output_frame = ttk.LabelFrame(main_frame, text="Results", padding="5")
        output_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        # Output Text Widget
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            height=20,
            width=100,
            font=("Courier", 9),
            wrap=tk.WORD
        )
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Welcome message
        self.output_text.insert(tk.END, "="*80 + "\n")
        self.output_text.insert(tk.END, "SORTING ALGORITHM BENCHMARKING TOOL\n")
        self.output_text.insert(tk.END, "="*80 + "\n\n")
        self.output_text.insert(tk.END, "This tool compares the performance of three sorting algorithms:\n")
        self.output_text.insert(tk.END, "  • Bubble Sort (O(n²) - Simple but slow)\n")
        self.output_text.insert(tk.END, "  • Insertion Sort (O(n²) - Better than bubble for small datasets)\n")
        self.output_text.insert(tk.END, "  • Merge Sort (O(n log n) - Fast and efficient)\n\n")
        self.output_text.insert(tk.END, "Select your configuration and click 'Run Benchmark' to start.\n")
        self.output_text.config(state=tk.DISABLED)
    
    def log_output(self, message: str, clear: bool = False):
        """Add message to output text widget."""
        self.output_text.config(state=tk.NORMAL)
        if clear:
            self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, message)
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.root.update()
    
    def update_progress(self, value: float, text: str = ""):
        """Update progress bar and label."""
        self.progress_var.set(value)
        if text:
            self.progress_label.config(text=text)
        self.root.update()
    
    def run_benchmark(self):
        """Run the benchmark in a separate thread."""
        if self.is_running:
            messagebox.showwarning("Warning", "A benchmark is already running!")
            return
        
        try:
            algorithm = self.algorithm_var.get()
            column = self.column_var.get()
            num_rows = int(self.rows_var.get())
            
            if num_rows < 1 or num_rows > 100000:
                messagebox.showerror("Error", "Number of rows must be between 1 and 100,000")
                return
            
            # Run in separate thread to avoid freezing GUI
            self.is_running = True
            self.run_button.config(state=tk.DISABLED)
            
            thread = threading.Thread(
                target=self._run_benchmark_thread,
                args=(algorithm, column, num_rows),
                daemon=True
            )
            thread.start()
            
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please check your settings.")
    
    def _run_benchmark_thread(self, algorithm: str, column: str, num_rows: int):
        """Run benchmark in separate thread."""
        try:
            self.log_output("", clear=True)
            self.update_progress(0, "Loading data...")
            
            # Load CSV
            start_time = time.time()
            self.benchmark.load_csv(num_rows)
            load_time = time.time() - start_time
            
            loaded_records = len(self.benchmark.data)
            
            # Check for warnings
            if loaded_records > 50000 and algorithm in ['bubble', 'insertion']:
                self.log_output(f"\n⚠️  WARNING: {algorithm.upper()} sort with {loaded_records:,} records\n")
                self.log_output("   This O(n²) algorithm may take a VERY LONG TIME!\n\n")
            
            self.update_progress(10, f"Loaded {loaded_records:,} records in {load_time:.4f}s")
            
            # Run sorting algorithm
            self.log_output(f"\nRunning {algorithm.upper()} Sort...\n")
            self.update_progress(20, f"Sorting with {algorithm}...")
            
            start_time = time.time()
            
            if algorithm == 'bubble':
                sorted_data = self._bubble_sort_with_progress(column)
            elif algorithm == 'insertion':
                sorted_data = self._insertion_sort_with_progress(column)
            elif algorithm == 'merge':
                sorted_data = self.benchmark.merge_sort(column)
            
            sort_time = time.time() - start_time
            
            # Display results
            self.display_results(sorted_data, algorithm, column, load_time, sort_time, loaded_records)
            self.update_progress(100, "Benchmark complete!")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.update_progress(0, "Error")
        finally:
            self.is_running = False
            self.run_button.config(state=tk.NORMAL)
    
    def _bubble_sort_with_progress(self, key: str) -> List[dict]:
        """Bubble sort with progress updates."""
        arr = [row.copy() for row in self.benchmark.data]
        n = len(arr)
        
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if self.benchmark._compare(arr[j], arr[j + 1], key, False):
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
            
            if not swapped:
                break
            
            progress = 20 + (i + 1) / n * 70
            self.update_progress(progress, f"Bubble Sort: {progress:.1f}%")
        
        return arr
    
    def _insertion_sort_with_progress(self, key: str) -> List[dict]:
        """Insertion sort with progress updates."""
        arr = [row.copy() for row in self.benchmark.data]
        
        for i in range(1, len(arr)):
            key_item = arr[i]
            j = i - 1
            
            while j >= 0 and self.benchmark._compare(arr[j], key_item, key, False):
                arr[j + 1] = arr[j]
                j -= 1
            
            arr[j + 1] = key_item
            
            progress = 20 + i / len(arr) * 70
            self.update_progress(progress, f"Insertion Sort: {progress:.1f}%")
        
        return arr
    
    def display_results(self, sorted_data: List[dict], algorithm: str, column: str, 
                       load_time: float, sort_time: float, num_records: int):
        """Display benchmark results."""
        output = ""
        output += "\n" + "="*80 + "\n"
        output += f"SORTING RESULTS - {algorithm.upper()}\n"
        output += "="*80 + "\n"
        output += f"Column sorted: {column}\n"
        output += f"Total records sorted: {num_records:,}\n"
        output += f"Load time: {load_time:.4f} seconds\n"
        output += f"Sort time: {sort_time:.4f} seconds\n"
        output += f"Total time: {load_time + sort_time:.4f} seconds\n"
        output += "="*80 + "\n\n"
        output += "First 10 records:\n"
        output += "-"*80 + "\n"
        
        if sorted_data:
            headers = list(sorted_data[0].keys())
            col_widths = {h: max(len(h), 15) for h in headers}
            
            header_str = " | ".join(f"{h:^{col_widths[h]}}" for h in headers)
            output += header_str + "\n"
            output += "-"*80 + "\n"
            
            for i, row in enumerate(sorted_data[:10]):
                row_str = " | ".join(f"{str(row[h]):^{col_widths[h]}}" for h in headers)
                output += f"{i+1:2}. {row_str}\n"
        
        output += "-"*80 + "\n"
        
        self.log_output(output)
    
    def clear_output(self):
        """Clear the output text widget."""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.progress_label.config(text="Ready")


def main():
    """Main function to run the GUI."""
    root = tk.Tk()
    gui = BenchmarkGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
