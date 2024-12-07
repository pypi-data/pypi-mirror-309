import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.font import Font

class ModernTheme:
    # Modern color scheme (same as before)
    BG_COLOR = "#f0f2f5"          
    FRAME_BG = "#ffffff"           
    PRIMARY = "#2563eb"            
    HOVER = "#1d4ed8"             
    TEXT_PRIMARY = "#1f2937"       
    TEXT_SECONDARY = "#6b7280"     
    BORDER = "#e5e7eb"            
    SUCCESS = "#10b981"           
    SCROLLBAR = "#cbd5e1"         
    SCROLLBAR_HOVER = "#94a3b8"   

class PodProxyManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Kubernetes Pod Proxy Manager")
        self.root.configure(bg=ModernTheme.BG_COLOR)
        
        self.setup_styles()
        self.port_entries = {}
        self.setup_gui()

    def setup_styles(self):
        # Previous style configurations remain the same
        style = ttk.Style()
        style.configure("Modern.TFrame", background=ModernTheme.FRAME_BG)
        style.configure("Card.TFrame", 
                       background=ModernTheme.FRAME_BG, 
                       relief="flat", 
                       borderwidth=1)
        
        style.configure("Modern.TButton",
                       background=ModernTheme.PRIMARY,
                       foreground="white",
                       padding=(10, 5),
                       font=('Segoe UI', 9))
        
        style.configure("Modern.TLabel",
                       background=ModernTheme.FRAME_BG,
                       foreground=ModernTheme.TEXT_PRIMARY,
                       font=('Segoe UI', 9))
        
        style.configure("Header.TLabel",
                       background=ModernTheme.FRAME_BG,
                       foreground=ModernTheme.TEXT_PRIMARY,
                       font=('Segoe UI', 10, 'bold'))
        
        style.configure("Modern.TEntry",
                       fieldbackground=ModernTheme.BG_COLOR,
                       borderwidth=1,
                       relief="flat",
                       padding=3)

        style.configure("Modern.Vertical.TScrollbar",
                       background=ModernTheme.SCROLLBAR,
                       bordercolor=ModernTheme.SCROLLBAR,
                       arrowcolor=ModernTheme.SCROLLBAR,
                       troughcolor=ModernTheme.BG_COLOR,
                       relief="flat",
                       borderwidth=0,
                       width=8)

    def on_mousewheel(self, event):
        # Check if the canvas has a scrollregion
        if self.canvas.bbox("all"):
            # Adjust scroll speed
            scroll_speed = -1 * (event.delta / 120)
            self.canvas.yview_scroll(int(scroll_speed), "units")
            # Prevent event from propagating
            return "break"

    def create_pod_card(self, parent, pod, row):
        # Create a card frame for each pod
        card = ttk.Frame(parent, style="Card.TFrame")
        card.grid(row=row, column=0, padx=8, pady=4, sticky="ew")
        parent.grid_columnconfigure(0, weight=1)

        # Add mousewheel binding to all elements in the card
        card.bind("<MouseWheel>", self.on_mousewheel)

        # Pod name with icon
        name_frame = ttk.Frame(card, style="Modern.TFrame")
        name_frame.pack(fill="x", padx=8, pady=4)
        name_frame.bind("<MouseWheel>", self.on_mousewheel)
        
        name_label = ttk.Label(name_frame, 
                              text=f"🔷 {pod['name']}", 
                              style="Modern.TLabel",
                              font=('Segoe UI', 9))
        name_label.pack(side="left")
        name_label.bind("<MouseWheel>", self.on_mousewheel)

        # Status with colored indicator
        status_label = ttk.Label(name_frame, 
                                text="● Running", 
                                foreground=ModernTheme.SUCCESS,
                                style="Modern.TLabel")
        status_label.pack(side="right")
        status_label.bind("<MouseWheel>", self.on_mousewheel)

        # Port entry and button container
        control_frame = ttk.Frame(card, style="Modern.TFrame")
        control_frame.pack(fill="x", padx=8, pady=4)
        control_frame.bind("<MouseWheel>", self.on_mousewheel)

        port_frame = ttk.Frame(control_frame, style="Modern.TFrame")
        port_frame.pack(side="left")
        port_frame.bind("<MouseWheel>", self.on_mousewheel)
        
        port_label = ttk.Label(port_frame, 
                              text="Port:", 
                              style="Modern.TLabel")
        port_label.pack(side="left", padx=(0, 4))
        port_label.bind("<MouseWheel>", self.on_mousewheel)
        
        port_entry = ttk.Entry(port_frame, 
                              width=6, 
                              style="Modern.TEntry")
        port_entry.pack(side="left")
        port_entry.insert(0, str(9000 + row))
        port_entry.bind("<MouseWheel>", self.on_mousewheel)
        self.port_entries[pod['name']] = port_entry

        # Start button
        start_button = ttk.Button(control_frame,
                                 text="Start Proxy",
                                 style="Modern.TButton",
                                 command=lambda p=pod['name']: self.start_proxy(p))
        start_button.pack(side="right")
        start_button.bind("<MouseWheel>", self.on_mousewheel)

    def fetch_pods(self):
        try:
            result = subprocess.run(
                ["kubectl", "get", "pods", "--no-headers"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            if result.returncode != 0:
                messagebox.showerror("Error", f"Failed to fetch pods: {result.stderr}")
                return []

            pods_info = []
            for line in result.stdout.splitlines():
                parts = line.split()
                if len(parts) >= 3 and parts[2].lower() == "running":
                    pods_info.append({
                        'name': parts[0],
                        'status': parts[2]
                    })
            return sorted(pods_info, key=lambda x: x['name'])
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return []

    def start_proxy(self, pod_name):
        if pod_name not in self.port_entries:
            messagebox.showwarning("Error", f"No port entry found for {pod_name}")
            return

        try:
            port = int(self.port_entries[pod_name].get())
            if not (9000 <= port <= 9100):
                messagebox.showwarning("Invalid Port", "Port must be between 9000 and 9100")
                return

            subprocess.Popen(
                ["kubectl", "port-forward", pod_name, f"{port}:80"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            messagebox.showinfo(
                "Success", f"Proxy started for {pod_name} on port {port}"
            )
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid port number")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start proxy for {pod_name}: {str(e)}")

    def refresh_pod_list(self):
        for widget in self.pods_frame.winfo_children():
            widget.destroy()
        self.port_entries.clear()

        pods = self.fetch_pods()
        for row, pod in enumerate(pods):
            self.create_pod_card(self.pods_frame, pod, row)

    def setup_gui(self):
        # Main container with padding
        main_frame = ttk.Frame(self.root, style="Modern.TFrame", padding="12")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(main_frame,
                               text="Pod Proxy Manager",
                               style="Header.TLabel",
                               font=('Segoe UI', 12, 'bold'))
        title_label.pack(pady=(0, 12))

        # Frame for pods list with scrollbar
        container = ttk.Frame(main_frame, style="Modern.TFrame")
        container.pack(fill=tk.BOTH, expand=True)

        # Canvas for scrolling
        self.canvas = tk.Canvas(container, 
                               background=ModernTheme.BG_COLOR,
                               highlightthickness=0)
        
        scrollbar = ttk.Scrollbar(container, 
                                 orient="vertical", 
                                 command=self.canvas.yview,
                                 style="Modern.Vertical.TScrollbar")
        
        self.pods_frame = ttk.Frame(self.canvas, style="Modern.TFrame")
        self.pods_frame.bind("<MouseWheel>", self.on_mousewheel)

        # Configure the canvas scrolling
        self.pods_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Bind mousewheel to canvas and its frame
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        
        # Create the window in the canvas
        self.canvas.create_window((0, 0), 
                                window=self.pods_frame, 
                                anchor="nw", 
                                width=self.canvas.winfo_reqwidth())
        
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Pack scrollable components
        container.pack(fill=tk.BOTH, expand=True)
        self.canvas.pack(side="left", fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill="y")

        # Refresh button container
        button_frame = ttk.Frame(main_frame, style="Modern.TFrame")
        button_frame.pack(pady=12)
        
        refresh_button = ttk.Button(
            button_frame,
            text="🔄 Refresh Pods",
            style="Modern.TButton",
            command=self.refresh_pod_list
        )
        refresh_button.pack()

        # Initial population of pods
        self.refresh_pod_list()

def main():
    root = tk.Tk()
    root.geometry("415x650")
    app = PodProxyManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()