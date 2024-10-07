import customtkinter as ctk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Initialize customtkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Collatz sequence function
def collatz_sequence(n):
    """Generate the Collatz sequence for a given number."""
    sequence = [n]
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        sequence.append(n)
    return sequence

# Function to plot the Collatz sequence in the UI
def plot_collatz(n, color='b', label=None):
    """Plot the Collatz sequence graphically."""
    sequence = collatz_sequence(n)
    global fig, ax, canvas
    if not fig or not ax:
        fig = Figure(figsize=(10, 5), dpi=100)  # Made graph size bigger
        ax = fig.add_subplot(111)
        ax.set_xlabel("Step", fontsize=12)
        ax.set_ylabel("Value", fontsize=12)
        ax.grid(True)
        canvas = FigureCanvasTkAgg(fig, master=frame_plot)
        canvas.get_tk_widget().pack()

    ax.plot(range(1, len(sequence) + 1), sequence, marker='o', linestyle='-', color=color, label=label)
    canvas.draw()

# Function to start the Collatz simulation
def start_simulation():
    """Start the Collatz simulation based on user input."""
    try:
        n = int(entry_number.get())
        if n <= 0:
            raise ValueError
        clear_plot()
        plot_collatz(n, color='#1f77b4')
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a positive integer.")

# Function to clear the plot
def clear_plot():
    """Clear the matplotlib plot."""
    global fig, ax, canvas
    fig, ax, canvas = None, None, None
    for widget in frame_plot.winfo_children():
        widget.destroy()

# Function to export the current graph as an image file
def export_graph():
    """Export the current graph as a PNG image."""
    if fig:
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            fig.savefig(file_path)
            messagebox.showinfo("Export Successful", f"Graph saved to: {file_path}")
    else:
        messagebox.showwarning("No Graph Available", "Generate a graph first before exporting.")

# Function to switch the theme (light/dark)
def switch_theme():
    """Switch between light and dark theme."""
    new_theme = "Dark" if theme_switch_var.get() else "Light"
    ctk.set_appearance_mode(new_theme)

# Real-time simulation variables
is_running = False
current_number = 1

# Function to launch the real-time simulation
def launch_simulation():
    """Launch the Collatz sequence simulation in real-time for consecutive numbers."""
    global is_running, current_number
    if not is_running:
        is_running = True
        current_number = 1
        launch_button.configure(text="Stop Simulation")
        run_simulation()
    else:
        is_running = False
        launch_button.configure(text="Launch Simulation")
        current_label.configure(text="")  # Clear current number display

# Function to iterate through numbers and plot their Collatz sequences dynamically
def run_simulation():
    """Run the Collatz sequence for each number until stopped."""
    global current_number
    if is_running:
        if current_number > 1:
            plot_collatz(current_number - 1, color='#CCCCCC')

        plot_collatz(current_number, color='#FF6347', label=f"Number: {current_number}")
        current_label.configure(text=f"Simulating Collatz sequence for: {current_number}")
        current_number += 1

        # Get speed from the slider and update the delay dynamically
        speed = speed_slider.get()
        root.after(int(speed * 1000), run_simulation)

# Initialize the main window
root = ctk.CTk()
root.title("Collatz Conjecture Simulation")
root.geometry("1100x850")  # Increased window size
fig, ax, canvas = None, None, None

# Input frame for number entry
frame_input = ctk.CTkFrame(root)
frame_input.pack(pady=20)

# Input Label and Entry
entry_label = ctk.CTkLabel(frame_input, text="Enter a starting number:", font=("Arial", 16))
entry_label.pack(side=ctk.LEFT, padx=10)
entry_number = ctk.CTkEntry(frame_input, width=100, font=("Arial", 16))
entry_number.pack(side=ctk.LEFT, padx=10)

# Start Button
start_button = ctk.CTkButton(frame_input, text="Start Simulation", command=start_simulation)
start_button.pack(side=ctk.LEFT, padx=10)

# Launch Button for real-time simulation
launch_button = ctk.CTkButton(frame_input, text="Launch Simulation", command=launch_simulation)
launch_button.pack(side=ctk.LEFT, padx=10)

# Speed Control Slider
speed_slider_label = ctk.CTkLabel(frame_input, text="Simulation Speed", font=("Arial", 16))
speed_slider_label.pack(side=ctk.LEFT, padx=10)
speed_slider = ctk.CTkSlider(frame_input, from_=0.1, to=2.0, number_of_steps=20, width=200)
speed_slider.set(1.0)  # Default speed set to 1.0 seconds
speed_slider.pack(side=ctk.LEFT, padx=10)

# Frame for the plot
frame_plot = ctk.CTkFrame(root)
frame_plot.pack(expand=True, fill="both", pady=20, padx=20)

# Additional Feature Buttons
button_frame = ctk.CTkFrame(root)
button_frame.pack(pady=10)

# Export Graph Button
export_button = ctk.CTkButton(button_frame, text="Export Graph as PNG", command=export_graph)
export_button.pack(side=ctk.LEFT, padx=20)

# Theme Switch
theme_switch_var = ctk.BooleanVar()
theme_switch = ctk.CTkSwitch(button_frame, text="Dark Mode", variable=theme_switch_var, onvalue=True, offvalue=False, command=switch_theme)
theme_switch.pack(side=ctk.LEFT, padx=20)

# Label for displaying the current number in real-time simulation
current_label = ctk.CTkLabel(root, text="", font=("Arial", 16), text_color='#FF6347')
current_label.pack(pady=10)

# Run the main loop
root.mainloop()