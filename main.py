# created by JavaD 
# discord id : javadsd.04
# teamspeak ip : bt69.ir 
# mywebsite address : https://www.javadsd.ir/


import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import re
import threading
import socket
import os
import sys
import ctypes

class DNSChangerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DNS Changer By JavaD")
        self.root.geometry("550x500")
        self.root.resizable(True, True)
        
        
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
            
        
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TLabel', font=('Arial', 10))
        
        
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        
        step1_frame = ttk.LabelFrame(main_frame, text="Select Network Interface")
        step1_frame.pack(fill=tk.X, padx=5, pady=5)
        
        interface_frame = ttk.Frame(step1_frame)
        interface_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(interface_frame, text="Network Interface:").pack(side=tk.LEFT, padx=5)
        
        self.interface_var = tk.StringVar()
        self.interface_combo = ttk.Combobox(interface_frame, textvariable=self.interface_var, state="readonly", width=40)
        self.interface_combo.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        refresh_button = ttk.Button(interface_frame, text="Refresh", command=self.refresh_interfaces)
        refresh_button.pack(side=tk.LEFT, padx=5)
        
        current_dns_frame = ttk.Frame(step1_frame)
        current_dns_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(current_dns_frame, text="Current DNS:").pack(side=tk.LEFT, padx=5)
        
        self.current_dns_var = tk.StringVar()
        self.current_dns_var.set("Unknown")
        ttk.Label(current_dns_frame, textvariable=self.current_dns_var).pack(side=tk.LEFT, padx=5)
        
        self.current_dns_button = ttk.Button(current_dns_frame, text="Check Current DNS", command=self.show_current_dns)
        self.current_dns_button.pack(side=tk.RIGHT, padx=5)
        
        step2_frame = ttk.LabelFrame(main_frame, text="Enter DNS Settings")
        step2_frame.pack(fill=tk.X, padx=5, pady=5)
        
        dns_entry_frame = ttk.Frame(step2_frame)
        dns_entry_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(dns_entry_frame, text="Primary DNS:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.preferred_dns_entry = ttk.Entry(dns_entry_frame, width=15)
        self.preferred_dns_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.preferred_dns_entry.insert(0, "8.8.8.8")
        
        ttk.Label(dns_entry_frame, text="Secondary DNS:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.alternate_dns_entry = ttk.Entry(dns_entry_frame, width=15)
        self.alternate_dns_entry.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
        self.alternate_dns_entry.insert(0, "8.8.4.4")
        
        presets_frame = ttk.LabelFrame(step2_frame, text="DNS Lists")
        presets_frame.pack(fill=tk.X, padx=5, pady=5)
        
        preset_row1 = ttk.Frame(presets_frame)
        preset_row1.pack(fill=tk.X, padx=5, pady=2)
        
        preset_row2 = ttk.Frame(presets_frame)
        preset_row2.pack(fill=tk.X, padx=5, pady=2)
        
        dns_presets = [
            
            ("Google", "8.8.8.8", "8.8.4.4", preset_row1),
            ("Cloudflare", "1.1.1.1", "1.0.0.1", preset_row1),
            ("OpenDNS", "208.67.222.222", "208.67.220.220", preset_row1),
            ("Quad9", "9.9.9.9", "149.112.112.112", preset_row1),
            ("Electro", "78.157.42.100", "78.157.42.101", preset_row2),
            ("Radar", "10.202.10.10", "10.202.10.11", preset_row2),
            ("Shecan", "178.22.122.100", "185.51.200.2", preset_row2),
            ("AdGuard", "94.140.14.14", "94.140.15.15", preset_row2)
        ]
        
        self.preset_buttons = []
        for name, primary, secondary, parent_frame in dns_presets:
            btn = ttk.Button(parent_frame, text=name, 
                              command=lambda p=primary, s=secondary, n=name: self.set_preset(p, s, n))
            btn.pack(side=tk.LEFT, padx=5, pady=2, expand=True, fill=tk.X)
            self.preset_buttons.append(btn)
        
        step3_frame = ttk.LabelFrame(main_frame, text="Apply DNS Settings")
        step3_frame.pack(fill=tk.X, padx=5, pady=5)
        
        actions_frame = ttk.Frame(step3_frame)
        actions_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.set_dns_button = ttk.Button(actions_frame, text="Apply DNS Settings", command=self.set_dns)
        self.set_dns_button.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        self.reset_dns_button = ttk.Button(actions_frame, text="Reset to Automatic DNS", command=self.reset_dns)
        self.reset_dns_button.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        self.test_dns_button = ttk.Button(actions_frame, text="Test DNS Connection", command=self.test_dns)
        self.test_dns_button.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        status_frame = ttk.LabelFrame(main_frame, text="Status and Logs")
        status_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        status_indicator_frame = ttk.Frame(status_frame)
        status_indicator_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(status_indicator_frame, text="Status:").pack(side=tk.LEFT, padx=5)
        
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_label = ttk.Label(status_indicator_frame, textvariable=self.status_var, foreground="blue")
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        self.log_area = scrolledtext.ScrolledText(status_frame, width=60, height=10, wrap=tk.WORD)
        self.log_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log_area.config(state=tk.DISABLED)
        
        self.refresh_interfaces()

    def log(self, message):
        """Add message to log area"""
        self.log_area.config(state=tk.NORMAL)
        self.log_area.insert(tk.END, f"{message}\n")
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)

    def set_status(self, message, is_error=False):
        """Update status text with color based on type"""
        self.status_var.set(message)
        color = "red" if is_error else "blue"
        self.status_label.configure(foreground=color)

    def refresh_interfaces(self):
        """Get all network interfaces and update the dropdown"""
        self.set_status("Refreshing network interfaces...")
        
        try:
           
            output = subprocess.run(['netsh', 'interface', 'show', 'interface'], 
                                    capture_output=True, text=True, encoding='utf-8')
            
            
            interfaces = []
            lines = output.stdout.splitlines()
            
            for line in lines[3:]:  
                if line.strip():
                    parts = re.split(r'\s{2,}', line.strip())
                    if len(parts) >= 4:
                        status, name = parts[1], parts[3]
                        if status == "Connected":
                            interfaces.append(name)
            
            if interfaces:
                self.interface_combo['values'] = interfaces
                self.interface_combo.current(0)
                self.set_status(f"Found {len(interfaces)} connected interfaces")
                self.log(f"Available network interfaces: {', '.join(interfaces)}")
                
                self.show_current_dns()
            else:
                self.interface_combo['values'] = [""]
                self.set_status("No connected network interfaces found!", True)
                self.log("WARNING: No connected network interfaces found!")
        
        except Exception as e:
            self.set_status(f"Error retrieving network interfaces", True)
            self.log(f"ERROR: {str(e)}")
            messagebox.showerror("Error", f"Error retrieving network interfaces:\n{str(e)}")
    
    def validate_ip(self, ip):
        """Validate if the string is a valid IP address"""
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False
    
    def set_preset(self, primary, secondary, name=""):
        """Set DNS fields to preset values"""
        self.preferred_dns_entry.delete(0, tk.END)
        self.preferred_dns_entry.insert(0, primary)
        
        self.alternate_dns_entry.delete(0, tk.END)
        self.alternate_dns_entry.insert(0, secondary)
        
        if name:
            self.log(f"Selected {name} DNS preset: {primary}, {secondary}")
        else:
            self.log(f"Selected DNS preset: {primary}, {secondary}")
    
    def set_dns(self):
        """Set DNS for the selected interface"""
        interface_name = self.interface_var.get()
        preferred_dns = self.preferred_dns_entry.get().strip()
        alternate_dns = self.alternate_dns_entry.get().strip()
        
        if not interface_name:
            messagebox.showerror("Error", "Please select a network interface!")
            return
        
        if not preferred_dns:
            messagebox.showerror("Error", "Please enter a Primary DNS address!")
            return
        
        if not self.validate_ip(preferred_dns):
            messagebox.showerror("Error", f"Invalid Primary DNS address: {preferred_dns}")
            return
        
        if alternate_dns and not self.validate_ip(alternate_dns):
            messagebox.showerror("Error", f"Invalid Secondary DNS address: {alternate_dns}")
            return
        
        self.set_buttons_state(tk.DISABLED)
        self.set_status("Setting DNS addresses...")
        
        def run_dns_change():
            try:
                subprocess.run(['ipconfig', '/flushdns'], 
                              capture_output=True, check=True)
                
                result1 = subprocess.run(['netsh', 'interface', 'ipv4', 'set', 'dns', 
                                        f'name="{interface_name}"', 'static', preferred_dns], 
                                        capture_output=True, text=True, check=True)
                
                self.log(f"Primary DNS set: {preferred_dns}")
                
                if alternate_dns:
                    result2 = subprocess.run(['netsh', 'interface', 'ipv4', 'add', 'dns', 
                                            f'name="{interface_name}"', alternate_dns, 'index=2'], 
                                            capture_output=True, text=True, check=True)
                    self.log(f"Secondary DNS set: {alternate_dns}")
                
                self.root.after(0, lambda: self.set_status(f"DNS settings applied successfully on {interface_name}"))
                self.root.after(0, lambda: messagebox.showinfo("Success", f"DNS settings successfully applied on {interface_name}!"))
                self.root.after(0, lambda: self.set_buttons_state(tk.NORMAL))
                self.root.after(0, self.show_current_dns)
            
            except subprocess.CalledProcessError as e:
                error_msg = f"Error setting DNS: {e.stderr if hasattr(e, 'stderr') else str(e)}"
                self.root.after(0, lambda: self.log(error_msg))
                self.root.after(0, lambda: self.set_status("Error applying DNS settings", True))
                self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
                self.root.after(0, lambda: self.set_buttons_state(tk.NORMAL))
        
        threading.Thread(target=run_dns_change, daemon=True).start()
    
    def reset_dns(self):
        """Reset DNS to DHCP (automatic) for the selected interface"""
        interface_name = self.interface_var.get()
        
        if not interface_name:
            messagebox.showerror("Error", "Please select a network interface!")
            return
        
        self.set_buttons_state(tk.DISABLED)
        self.set_status("Resetting DNS to automatic (DHCP)...")
        
        def run_dns_reset():
            try:
                subprocess.run(['ipconfig', '/flushdns'], 
                              capture_output=True, check=True)
                
                result = subprocess.run(['netsh', 'interface', 'ipv4', 'set', 'dns', 
                                       f'name="{interface_name}"', 'dhcp'], 
                                       capture_output=True, text=True, check=True)
                
                self.root.after(0, lambda: self.log(f"DNS reset to automatic (DHCP) for {interface_name}"))
                self.root.after(0, lambda: self.set_status(f"DNS successfully reset to automatic"))
                self.root.after(0, lambda: messagebox.showinfo("Success", f"DNS for {interface_name} has been reset to automatic (DHCP)!"))
                self.root.after(0, lambda: self.set_buttons_state(tk.NORMAL))
                self.root.after(0, self.show_current_dns)
            
            except subprocess.CalledProcessError as e:
                error_msg = f"Error resetting DNS: {e.stderr if hasattr(e, 'stderr') else str(e)}"
                self.root.after(0, lambda: self.log(error_msg))
                self.root.after(0, lambda: self.set_status("Error resetting DNS", True))
                self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
                self.root.after(0, lambda: self.set_buttons_state(tk.NORMAL))
        
        threading.Thread(target=run_dns_reset, daemon=True).start()
    
    def test_dns(self):
        """Test DNS connectivity by pinging common domains"""
        self.set_status("Testing DNS connectivity...")
        self.set_buttons_state(tk.DISABLED)
        
        def run_dns_test():
            test_domains = ["google.com", "cloudflare.com", "microsoft.com"]
            results = []
            
            for domain in test_domains:
                try:
                    self.root.after(0, lambda d=domain: self.log(f"Testing connection to {d}..."))
                    
                    start_time = socket.getdefaulttimeout()
                    socket.setdefaulttimeout(3)
                    ip = socket.gethostbyname(domain)
                    socket.setdefaulttimeout(start_time)
                    
                    ping_param = '-n' if os.name == 'nt' else '-c'
                    ping_result = subprocess.run(['ping', ping_param, '1', domain], 
                                               capture_output=True, text=True)
                    
                    if ping_result.returncode == 0:
                        results.append((domain, True, ip))
                        self.root.after(0, lambda d=domain, i=ip: self.log(f"✓ Connection to {d} ({i}) successful"))
                    else:
                        results.append((domain, False, ip))
                        self.root.after(0, lambda d=domain: self.log(f"✗ Connection to {d} failed (DNS resolved but ping failed)"))
                
                except socket.gaierror:
                    results.append((domain, False, None))
                    self.root.after(0, lambda d=domain: self.log(f"✗ Failed to resolve {d} (DNS lookup failed)"))
                except Exception as e:
                    results.append((domain, False, None))
                    self.root.after(0, lambda d=domain, e=str(e): self.log(f"✗ Error testing {d}: {e}"))
            
            success_count = sum(1 for _, success, _ in results if success)
            if success_count == len(test_domains):
                status_msg = "DNS test successful! All domains accessible"
                self.root.after(0, lambda: self.set_status(status_msg))
                self.root.after(0, lambda: self.log(f"Result: {status_msg}"))
            elif success_count > 0:
                status_msg = f"DNS test partially successful ({success_count}/{len(test_domains)} domains accessible)"
                self.root.after(0, lambda: self.set_status(status_msg))
                self.root.after(0, lambda: self.log(f"Result: {status_msg}"))
            else:
                status_msg = "DNS test failed! Unable to access any domains"
                self.root.after(0, lambda: self.set_status(status_msg, True))
                self.root.after(0, lambda: self.log(f"Result: {status_msg}"))
            
            self.root.after(0, lambda: self.set_buttons_state(tk.NORMAL))
        
        threading.Thread(target=run_dns_test, daemon=True).start()
    
    def show_current_dns(self):
        """Show current DNS settings for the selected interface"""
        interface_name = self.interface_var.get()
        
        if not interface_name:
            self.current_dns_var.set("No interface selected")
            return
        
        self.set_status(f"Checking current DNS settings for {interface_name}...")
        
        def run_get_dns():
            try:
                result = subprocess.run(['netsh', 'interface', 'ipv4', 'show', 'dns', interface_name], 
                                       capture_output=True, text=True)
                
                if result.returncode == 0:
                    dns_output = result.stdout
                    self.root.after(0, lambda: self.log(f"Current DNS settings for {interface_name}:"))
                    self.root.after(0, lambda: self.log(dns_output))
                    
                    if "DHCP" in dns_output:
                        self.root.after(0, lambda: self.current_dns_var.set("Automatic (DHCP)"))
                        self.root.after(0, lambda: self.set_status(f"Current DNS: Automatic (DHCP)"))
                    else:
                        dns_servers = re.findall(r'DNS servers configured through STATIC.+?: ([\d\.]+)', dns_output)
                        if dns_servers:
                            servers_str = ", ".join(dns_servers)
                            self.root.after(0, lambda: self.current_dns_var.set(servers_str))
                            self.root.after(0, lambda: self.set_status(f"Current DNS: {servers_str}"))
                        else:
                            self.root.after(0, lambda: self.current_dns_var.set("Could not determine"))
                            self.root.after(0, lambda: self.set_status(f"Could not determine current DNS"))
                else:
                    self.root.after(0, lambda: self.log(f"Error retrieving DNS information"))
                    self.root.after(0, lambda: self.current_dns_var.set("Error retrieving"))
                    self.root.after(0, lambda: self.set_status("Error retrieving DNS information", True))
            
            except Exception as e:
                self.root.after(0, lambda: self.log(f"Error: {str(e)}"))
                self.root.after(0, lambda: self.current_dns_var.set("Error"))
                self.root.after(0, lambda: self.set_status("Error retrieving DNS information", True))
        
        threading.Thread(target=run_get_dns, daemon=True).start()
    
    def set_buttons_state(self, state):
        """Enable or disable all buttons"""
        self.set_dns_button['state'] = state
        self.reset_dns_button['state'] = state
        self.test_dns_button['state'] = state
        self.current_dns_button['state'] = state
        for button in self.preset_buttons:
            button['state'] = state

def check_admin():
    """Check if the application is running with admin privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def main():
    try:
        if not check_admin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        else:
            root = tk.Tk()
            app = DNSChangerApp(root)
            root.mainloop()
    except Exception as e:
        messagebox.showerror("Application Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()

# created by JavaD 
# discord id : javadsd.04
# teamspeak ip : bt69.ir 
# mywebsite address : https://www.javadsd.ir/
