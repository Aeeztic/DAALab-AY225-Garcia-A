import time
import copy
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkinter import font as tkFont


class SortingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithm Suite - Enterprise Edition")
        self.root.geometry("1400x850")
        self.root.minsize(1200, 750)
        
        self.data = []
        self.sorted_data = []
        self.current_algorithm = None
        self.execution_time = 0
        
        # Set professional color scheme
        self.bg_color = "#0F1419"  # Midnight Blue
        self.sidebar_color = "#0D0F15"  # Darker Midnight Blue
        self.accent_color = "#00E5CC"  # Electric Mint
        self.success_color = "#00D9A3"  # Mint Green
        self.warning_color = "#FF6B6B"  # Coral Red (complementary)
        self.info_color = "#00E5CC"  # Electric Mint
        self.text_primary = "#FFFFFF"  # White
        self.text_secondary = "#B0BEC5"  # Light Gray
        
        self.root.configure(bg=self.bg_color)
        
        # Configure styles
        self.setup_styles()
        
        # Create UI
        self.create_header()
        self.create_main_layout()
        
        # Auto-load dataset
        self.auto_load_dataset()
    
    def setup_styles(self):
        """Setup professional styling"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles
        style.configure('TButton', font=('Segoe UI', 10), padding=8)
        style.configure('Header.TLabel', font=('Segoe UI', 16, 'bold'), background=self.sidebar_color, foreground='white')
    
    def create_header(self):
        """Create professional header"""
        header = tk.Frame(self.root, bg=self.sidebar_color, height=70)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)
        
        # Company logo/title area
        title_frame = tk.Frame(header, bg=self.sidebar_color)
        title_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=25, pady=15)
        
        main_title = tk.Label(title_frame, text="█ SORTING ALGORITHM SUITE", 
                             font=('Segoe UI', 18, 'bold'), bg=self.sidebar_color, fg=self.accent_color)
        main_title.pack(anchor=tk.W)
        
        subtitle = tk.Label(title_frame, text="Enterprise Data Processing System v1.0", 
                           font=('Segoe UI', 9), bg=self.sidebar_color, fg=self.text_secondary)
        subtitle.pack(anchor=tk.W)
        
        # Status indicator
        status_frame = tk.Frame(header, bg=self.sidebar_color)
        status_frame.pack(side=tk.RIGHT, padx=25, pady=15)
        
        status_dot = tk.Label(status_frame, text="●", font=('Segoe UI', 20), 
                             fg=self.success_color, bg=self.sidebar_color)
        status_dot.pack(side=tk.LEFT, padx=(0, 8))
        
        status_text = tk.Label(status_frame, text="System Ready", 
                              font=('Segoe UI', 10, 'bold'), bg=self.sidebar_color, fg=self.success_color)
        status_text.pack(side=tk.LEFT)
    
    def create_main_layout(self):
        """Create main content layout"""
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Left section - Data Input & Info
        left_section = self.create_left_section(main_frame)
        left_section.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Middle section - Controls
        middle_section = self.create_middle_section(main_frame)
        middle_section.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Right section - Results
        right_section = self.create_right_section(main_frame)
        right_section.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=0)
    
    def create_left_section(self, parent):
        """Create left section with data preview"""
        section = tk.Frame(parent, bg='#1A1F2E', relief=tk.FLAT, bd=0)
        
        # Header with icon
        header_frame = tk.Frame(section, bg='#16212A', height=50)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(header_frame, text="📊  INPUT DATA PREVIEW", 
                               font=('Segoe UI', 11, 'bold'), 
                               bg='#16212A', fg=self.accent_color, justify=tk.LEFT)
        header_label.pack(anchor=tk.W, padx=15, pady=12)
        
        # Data display with scrollbar
        content_frame = tk.Frame(section, bg='#1A1F2E')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.data_text = scrolledtext.ScrolledText(content_frame, height=25, 
                                                   font=('Courier New', 9), 
                                                   bg='#0D0F15', fg='#00E5CC',
                                                   relief=tk.FLAT, bd=1)
        self.data_text.pack(fill=tk.BOTH, expand=True)
        self.data_text.config(state=tk.DISABLED)
        
        # Statistics panel
        stats_frame = tk.Frame(section, bg='#1A1F2E', height=100)
        stats_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        stats_frame.pack_propagate(False)
        
        divider = tk.Frame(stats_frame, bg=self.accent_color, height=1)
        divider.pack(fill=tk.X, pady=(10, 15))
        
        stats_label = tk.Label(stats_frame, text="STATISTICS", 
                              font=('Segoe UI', 9, 'bold'), bg='#1A1F2E', fg=self.accent_color)
        stats_label.pack(anchor=tk.W, pady=(0, 8))
        
        self.stats_text = tk.Label(stats_frame, text="Waiting for data...", 
                                  font=('Segoe UI', 9), bg='#1A1F2E', fg=self.text_secondary,
                                  justify=tk.LEFT)
        self.stats_text.pack(anchor=tk.W)
        
        return section
    
    def create_middle_section(self, parent):
        """Create middle section with algorithm controls"""
        section = tk.Frame(parent, bg='#1A1F2E', relief=tk.FLAT, bd=0, width=220)
        section.pack_propagate(False)
        
        # Header
        header_frame = tk.Frame(section, bg='#16212A', height=50)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(header_frame, text="⚙️  ALGORITHMS", 
                               font=('Segoe UI', 11, 'bold'), 
                               bg='#16212A', fg=self.accent_color)
        header_label.pack(anchor=tk.W, padx=15, pady=12)
        
        # Buttons frame
        buttons_frame = tk.Frame(section, bg='#1A1F2E')
        buttons_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=15)
        
        # Algorithm buttons
        self.create_algorithm_button(buttons_frame, "BUBBLE SORT", self.run_bubble_sort, 
                                    self.warning_color, "🔄")
        
        self.create_algorithm_button(buttons_frame, "INSERTION SORT", self.run_insertion_sort, 
                                    self.accent_color, "📍")
        
        self.create_algorithm_button(buttons_frame, "MERGE SORT", self.run_merge_sort, 
                                    self.success_color, "🔀")
        
        # Divider
        divider = tk.Frame(buttons_frame, bg='#16212A', height=1)
        divider.pack(fill=tk.X, pady=15)
        
        # Clear button
        self.create_control_button(buttons_frame, "CLEAR RESULTS", self.clear_results, 
                                  '#4A5568', "🗑️")
        
        return section
    
    def create_algorithm_button(self, parent, text, command, color, emoji):
        """Create styled algorithm button"""
        btn = tk.Button(parent, text=f"{emoji} {text}", command=command,
                       font=('Segoe UI', 9, 'bold'), bg=color, fg='white',
                       relief=tk.FLAT, bd=0, padx=15, pady=12, cursor='hand2',
                       activebackground=self.darken_color(color))
        btn.pack(fill=tk.X, pady=6)
        
        # Hover effect
        def on_enter(e):
            btn.config(bg=self.darken_color(color))
        def on_leave(e):
            btn.config(bg=color)
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
    
    def create_control_button(self, parent, text, command, color, emoji):
        """Create styled control button"""
        btn = tk.Button(parent, text=f"{emoji} {text}", command=command,
                       font=('Segoe UI', 8, 'bold'), bg=color, fg='white',
                       relief=tk.FLAT, bd=0, padx=15, pady=8, cursor='hand2')
        btn.pack(fill=tk.X, pady=4)
    
    def create_right_section(self, parent):
        """Create right section with results"""
        section = tk.Frame(parent, bg='#1A1F2E', relief=tk.FLAT, bd=0)
        
        # Header
        header_frame = tk.Frame(section, bg='#16212A', height=50)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(header_frame, text="📈  SORTED RESULTS", 
                               font=('Segoe UI', 11, 'bold'), 
                               bg='#16212A', fg=self.accent_color)
        header_label.pack(anchor=tk.W, padx=15, pady=12)
        
        # Results info panel
        info_frame = tk.Frame(section, bg='#1A1F2E')
        info_frame.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        # Algorithm name
        algo_frame = tk.Frame(info_frame, bg='#1A1F2E')
        algo_frame.pack(fill=tk.X, pady=3)
        
        tk.Label(algo_frame, text="Algorithm:", font=('Segoe UI', 9, 'bold'), 
                bg='#1A1F2E', fg=self.text_primary).pack(side=tk.LEFT)
        self.algo_name_label = tk.Label(algo_frame, text="None", 
                                       font=('Segoe UI', 9), bg='#1A1F2E', fg=self.accent_color)
        self.algo_name_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Execution time
        time_frame = tk.Frame(info_frame, bg='#1A1F2E')
        time_frame.pack(fill=tk.X, pady=3)
        
        tk.Label(time_frame, text="Execution Time:", font=('Segoe UI', 9, 'bold'), 
                bg='#1A1F2E', fg=self.text_primary).pack(side=tk.LEFT)
        self.time_label = tk.Label(time_frame, text="0.000000 sec", 
                                  font=('Segoe UI', 9), bg='#1A1F2E', fg=self.success_color)
        self.time_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Elements count
        count_frame = tk.Frame(info_frame, bg='#1A1F2E')
        count_frame.pack(fill=tk.X, pady=3)
        
        tk.Label(count_frame, text="Elements Sorted:", font=('Segoe UI', 9, 'bold'), 
                bg='#1A1F2E', fg=self.text_primary).pack(side=tk.LEFT)
        self.count_label = tk.Label(count_frame, text="0", 
                                   font=('Segoe UI', 9), bg='#1A1F2E', fg=self.accent_color)
        self.count_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Divider
        divider = tk.Frame(section, bg=self.accent_color, height=1)
        divider.pack(fill=tk.X, padx=15, pady=10)
        
        # Results display
        content_frame = tk.Frame(section, bg='#1A1F2E')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        self.results_text = scrolledtext.ScrolledText(content_frame, height=25, 
                                                      font=('Courier New', 9), 
                                                      bg='#0D0F15', fg='#00E5CC',
                                                      relief=tk.FLAT, bd=1)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        self.results_text.config(state=tk.DISABLED)
        
        return section
    
    def darken_color(self, color):
        """Darken a hex color for hover effect"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(max(0, c - 30) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*darkened)
    
    def bubble_sort(self, arr):
        """Bubble sort algorithm - returns sorted array and time taken"""
        start_time = time.time()
        n = len(arr)
        arr_copy = copy.deepcopy(arr)
        
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if arr_copy[j] > arr_copy[j + 1]:
                    arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
                    swapped = True
            if not swapped:
                break
        
        end_time = time.time()
        time_taken = end_time - start_time
        return arr_copy, time_taken
    
    def insertion_sort(self, arr):
        """Insertion sort algorithm - returns sorted array and time taken"""
        start_time = time.time()
        arr_copy = copy.deepcopy(arr)
        
        for i in range(1, len(arr_copy)):
            key = arr_copy[i]
            j = i - 1
            while j >= 0 and arr_copy[j] > key:
                arr_copy[j + 1] = arr_copy[j]
                j -= 1
            arr_copy[j + 1] = key
        
        end_time = time.time()
        time_taken = end_time - start_time
        return arr_copy, time_taken
    
    def merge_sort(self, arr):
        """Merge sort algorithm - returns sorted array and time taken"""
        start_time = time.time()
        arr_copy = copy.deepcopy(arr)
        
        def merge(left, right):
            result = []
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            result.extend(left[i:])
            result.extend(right[j:])
            return result
        
        def merge_sort_helper(arr):
            if len(arr) <= 1:
                return arr
            mid = len(arr) // 2
            left = merge_sort_helper(arr[:mid])
            right = merge_sort_helper(arr[mid:])
            return merge(left, right)
        
        arr_copy = merge_sort_helper(arr_copy)
        end_time = time.time()
        time_taken = end_time - start_time
        return arr_copy, time_taken
    
    def auto_load_dataset(self):
        """Automatically load dataset.txt"""
        try:
            with open("dataset.txt", 'r') as file:
                self.data = [int(line.strip()) for line in file if line.strip()]
            
            self.display_data_preview()
            self.update_statistics()
            
        except FileNotFoundError:
            self.data_text.config(state=tk.NORMAL)
            self.data_text.delete(1.0, tk.END)
            self.data_text.insert(tk.END, "⚠️  Error: dataset.txt not found")
            self.data_text.config(state=tk.DISABLED)
            self.stats_text.config(text="❌ File not found")
        except ValueError:
            self.data_text.config(state=tk.NORMAL)
            self.data_text.delete(1.0, tk.END)
            self.data_text.insert(tk.END, "⚠️  Error: Invalid data format")
            self.data_text.config(state=tk.DISABLED)
            self.stats_text.config(text="❌ Invalid format")
    
    def display_data_preview(self):
        """Display loaded data"""
        self.data_text.config(state=tk.NORMAL)
        self.data_text.delete(1.0, tk.END)
        self.data_text.insert(tk.END, f"✓ Loaded {len(self.data):,} elements\n\n")
        self.data_text.insert(tk.END, "Data:\n" + str(self.data))
        self.data_text.config(state=tk.DISABLED)
    
    def update_statistics(self):
        """Update data statistics"""
        if not self.data:
            self.stats_text.config(text="No data loaded")
            return
        
        stats = f"Total: {len(self.data):,} elements\n"
        stats += f"Min: {min(self.data):,}\n"
        stats += f"Max: {max(self.data):,}\n"
        stats += f"Average: {sum(self.data)/len(self.data):.2f}\n"
        stats += f"Sum: {sum(self.data):,}"
        
        self.stats_text.config(text=stats)
    
    def run_bubble_sort(self):
        """Execute bubble sort"""
        if not self.data:
            messagebox.showwarning("Warning", "No data loaded. Please load dataset.txt")
            return
        self.sorted_data, self.execution_time = self.bubble_sort(self.data)
        self.display_results("BUBBLE SORT")
    
    def run_insertion_sort(self):
        """Execute insertion sort"""
        if not self.data:
            messagebox.showwarning("Warning", "No data loaded. Please load dataset.txt")
            return
        self.sorted_data, self.execution_time = self.insertion_sort(self.data)
        self.display_results("INSERTION SORT")
    
    def run_merge_sort(self):
        """Execute merge sort"""
        if not self.data:
            messagebox.showwarning("Warning", "No data loaded. Please load dataset.txt")
            return
        self.sorted_data, self.execution_time = self.merge_sort(self.data)
        self.display_results("MERGE SORT")
    
    def display_results(self, algorithm):
        """Display execution results"""
        self.algo_name_label.config(text=algorithm)
        self.time_label.config(text=f"{self.execution_time:.6f} sec")
        self.count_label.config(text=f"{len(self.sorted_data):,}")
        
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        result_text = f"Sorted Data ({len(self.sorted_data):,} elements):\n\n"
        result_text += str(self.sorted_data)
        
        self.results_text.insert(tk.END, result_text)
        self.results_text.config(state=tk.DISABLED)
    
    def clear_results(self):
        """Clear results"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)
        
        self.algo_name_label.config(text="None")
        self.time_label.config(text="0.000000 sec")
        self.count_label.config(text="0")


if __name__ == "__main__":
    root = tk.Tk()
    gui = SortingGUI(root)
    root.mainloop()
