# gui/app.py
"""GUI application for Chrommin"""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

class ChromminApp:
    """Graphical user interface for Chrommin"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Chrommin - Multi-Account Automation")
        self.root.geometry("600x400")
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Chrommin Configuration", font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Number of bots
        ttk.Label(main_frame, text="Number of Bots:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.bot_count = tk.IntVar(value=5)
        bot_spinbox = ttk.Spinbox(main_frame, from_=1, to=100, textvariable=self.bot_count, width=10)
        bot_spinbox.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Headless mode
        self.headless_var = tk.BooleanVar(value=False)
        headless_check = ttk.Checkbutton(main_frame, text="Run in background (headless)", variable=self.headless_var)
        headless_check.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Wallet automation
        self.wallet_var = tk.BooleanVar(value=True)
        wallet_check = ttk.Checkbutton(main_frame, text="Enable wallet automation", variable=self.wallet_var)
        wallet_check.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Humanization
        self.humanize_var = tk.BooleanVar(value=True)
        humanize_check = ttk.Checkbutton(main_frame, text="Humanize inputs", variable=self.humanize_var)
        humanize_check.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        start_btn = ttk.Button(button_frame, text="Start Chrommin", command=self.start_chrommin)
        start_btn.pack(side=tk.LEFT, padx=5)
        
        stop_btn = ttk.Button(button_frame, text="Stop", command=self.stop_chrommin)
        stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Status
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, foreground="green")
        status_label.grid(row=6, column=0, columnspan=2, pady=10)
        
    def start_chrommin(self):
        """Start the Chrommin automation"""
        self.status_var.set("Starting...")
        
        # Save configuration
        from config.manager import ConfigManager
        config = ConfigManager.load_config()
        config._data.update({
            'num_bots': self.bot_count.get(),
            'headless': self.headless_var.get(),
            'wallet_automation': self.wallet_var.get(),
            'humanize_inputs': self.humanize_var.get()
        })
        config.save()
        
        # Start the automation engine in a separate thread
        import threading
        thread = threading.Thread(target=self.run_automation, daemon=True)
        thread.start()
        
        self.status_var.set("Running")
        
    def run_automation(self):
        """Run the automation engine"""
        import asyncio
        from core.engine import AutomationEngine
        
        async def main():
            engine = AutomationEngine()
            await engine.start()
            
        asyncio.run(main())
        
    def stop_chrommin(self):
        """Stop the Chrommin automation"""
        self.status_var.set("Stopping...")
        # Implementation would signal the engine to stop
        self.status_var.set("Stopped")
        
    def run(self):
        """Run the GUI application"""
        self.root.mainloop()