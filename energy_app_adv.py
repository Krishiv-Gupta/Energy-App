import tkinter as tk
from tkinter import messagebox
import openai
from PIL import Image
import customtkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Constants
AVERAGE_SUNLIGHT_HOURS = {
    "Tropical": 6.5,
    "Temperate": 4.5,
    "Polar": 2.5,
}
PANEL_EFFICIENCY = 0.2  # 20%
PANEL_POWER = 330  # Power of one panel in watts
CARBON_EMISSION_FACTORS = {
    "Electricity": 0.4,  # kg CO2 per kWh (global average)
    "Gas": 0.184,  # kg CO2 per kWh
    "Solar": 0,  # Solar is carbon-neutral
}

# Placeholder for user credentials
USER_CREDENTIALS = {
    "admin": "password123",
    "user": "pass456"
}

def verify_login(username, password):
    return USER_CREDENTIALS.get(username) == password

def show_login_screen():
    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()

        if verify_login(username, password):
            frame.destroy()
            menu_frame.pack(fill="x")
            switch_to_home()
        else:
            messagebox.showerror("Login Error", "Invalid username or password.")

    global frame
    side_img_data = Image.open("side-img.png").convert("RGBA").resize((300, 480))
    email_icon_data = Image.open("email-icon.png").convert("RGBA").resize((20, 20))
    password_icon_data = Image.open("password-icon.png").convert("RGBA").resize((17, 17))

    # Create CTkImage objects
    side_img = customtkinter.CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))
    email_icon = customtkinter.CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(20, 20))
    password_icon = customtkinter.CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(17, 17))

    # Left-side image
    customtkinter.CTkLabel(master=app, text="", image=side_img).pack(side="left")

    # Right-side frame
    frame = customtkinter.CTkFrame(master=app, width=300, height=480, fg_color="#ffffff")
    frame.pack_propagate(False)  # Prevent widgets from resizing the frame
    frame.pack(side="right")

    # Welcome text
    customtkinter.CTkLabel(master=frame, text="Welcome to the Energy", text_color="#601E88", 
                        font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
    customtkinter.CTkLabel(master=frame, text="Calculator App!", text_color="#601E88", 
                        font=("Arial Bold", 24)).pack(anchor="w", pady=(0, 5), padx=(25, 0))
    customtkinter.CTkLabel(master=frame, text="Sign in to your account to use the app", text_color="#7E7E7E", 
                        font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

    # Email entry
    customtkinter.CTkLabel(master=frame, text="  Username:", text_color="#601E88", 
                        font=("Arial Bold", 14), image=email_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
    username_entry = customtkinter.CTkEntry(master=frame, width=225, fg_color="#EEEEEE", 
                        border_color="#601E88", border_width=1, text_color="#000000")
    username_entry.pack(anchor="w", padx=(25, 0))

    # Password entry
    customtkinter.CTkLabel(master=frame, text="  Password:", text_color="#601E88", 
                        font=("Arial Bold", 14), image=password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
    password_entry = customtkinter.CTkEntry(master=frame, width=225, fg_color="#EEEEEE", 
                        border_color="#601E88", border_width=1, text_color="#000000", show="*")
    password_entry.pack(anchor="w", padx=(25, 0))

    # Login button
    customtkinter.CTkButton(master=frame, text="Login", fg_color="#601E88", hover_color="#E44982", 
                            font=("Arial Bold", 12), text_color="#ffffff", width=225, command=attempt_login).pack(anchor="w", pady=(40, 0), padx=(25, 0))


def switch_to_solar_calculator():
    clear_window()
    solar_calculator_ui()

def switch_to_home_optimizer():
    clear_window()
    home_optimizer_ui()

def switch_to_carbon_footprint_calculator():
    clear_window()
    carbon_footprint_ui()

def switch_to_home():
    clear_window()
    home_ui()

def clear_window():
    for widget in app.winfo_children():
        if widget != menu_frame:
            widget.destroy()

def plot_graph(consumption, generated):
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))

    # Bar chart
    ax[0].bar(["Consumption", "Generated"], [consumption, generated], color=["red", "green"])
    ax[0].set_title("Daily Energy Comparison")
    ax[0].set_ylabel("kWh")

    # Pie chart
    labels = ["Consumption", "Generated"]
    sizes = [consumption, generated]
    colors = ["red", "green"]
    ax[1].pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors, startangle=90)
    ax[1].set_title("Energy Share")

    plt.tight_layout()
    return fig

def plot_graph2(consumption1,consumption2, consumption3):
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))

    # Bar chart
    ax[0].bar(["Gas", "Electricity", "Solar"], [consumption1, consumption2, consumption3], color=["red", "green", "blue"])
    ax[0].set_title("Daily Energy Comparison")
    ax[0].set_ylabel("kWh")

    # Pie chart
    labels = ["Gas", "Electricity", "Solar"]
    sizes = [consumption1, consumption2, consumption3]
    colors = ["red", "green", "blue"]
    ax[1].pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors, startangle=90)
    ax[1].set_title("Energy Share")

    plt.tight_layout()
    return fig

def solar_calculator_ui():
    app.geometry("1000x900")
    

    customtkinter.set_appearance_mode("light")

    sidebar_frame = customtkinter.CTkFrame(master=app, fg_color="#2A8C55",  width=176, height=650, corner_radius=0)
    sidebar_frame.pack_propagate(0)
    sidebar_frame.pack(fill="y", anchor="w", side="left")

    logo_img_data = Image.open("logo.png")
    logo_img = customtkinter.CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(77.68, 85.42))

    customtkinter.CTkLabel(master=sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")

    analytics_img_data = Image.open("analytics_icon.png")
    analytics_img = customtkinter.CTkImage(dark_image=analytics_img_data, light_image=analytics_img_data)

    customtkinter.CTkButton(master=sidebar_frame, image=analytics_img, text="Home", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w", command=switch_to_home).pack(anchor="center", ipady=5, pady=(60, 0))

    package_img_data = Image.open("package_icon.png")
    package_img = customtkinter.CTkImage(dark_image=package_img_data, light_image=package_img_data)

    customtkinter.CTkButton(master=sidebar_frame, image=package_img, text="Solar Calculator", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w", command=switch_to_solar_calculator).pack(anchor="center", ipady=5, pady=(16, 0))

    list_img_data = Image.open("list_icon.png")
    list_img = customtkinter.CTkImage(dark_image=list_img_data, light_image=list_img_data)
    customtkinter.CTkButton(master=sidebar_frame, image=list_img, text="Home Optimiser", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w", command=switch_to_home_optimizer).pack(anchor="center", ipady=5, pady=(16, 0))

    returns_img_data = Image.open("returns_icon.png")
    returns_img = customtkinter.CTkImage(dark_image=returns_img_data, light_image=returns_img_data)
    customtkinter.CTkButton(master=sidebar_frame, image=returns_img, text="Carbon Footprint", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w", command=switch_to_carbon_footprint_calculator).pack(anchor="center", ipady=5, pady=(16, 0))

    def calculate_and_plot():
        try:
            location = location_var.get()
            panel_power = int(panel_power_entry.get())
            num_panels = int(num_panels_entry.get())
            consumption = float(consumption_entry.get())

            sunlight_hours = AVERAGE_SUNLIGHT_HOURS[location]
            total_power = num_panels * panel_power
            total_energy = total_power * sunlight_hours * PANEL_EFFICIENCY
            total_energy_kwh = total_energy / 1000

            result_label.configure(text=f"Estimated Daily Energy Generation: {total_energy_kwh:.2f} kWh")

            fig = plot_graph(consumption / 30, total_energy_kwh)
            canvas = FigureCanvasTkAgg(fig, master=app)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(pady=10)
            canvas.draw()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numerical inputs.")

    location_label = customtkinter.CTkLabel(app, text="Select Location:", text_color="#fff", font=("Arial", 18))
    location_label.pack(pady=5)
    location_var = customtkinter.StringVar(value="Tropical")
    location_menu = customtkinter.CTkOptionMenu(app, variable=location_var, values=list(AVERAGE_SUNLIGHT_HOURS.keys()))
    location_menu.pack(pady=5)


    panel_power_label = customtkinter.CTkLabel(app, text="Enter Panel Power(W):", text_color="#fff", font=("Arial", 18))
    panel_power_label.pack(pady=5)
    panel_power_entry = customtkinter.CTkEntry(app)
    panel_power_entry.pack(pady=5)

    num_panels_label = customtkinter.CTkLabel(app, text="Enter Number of Panels:", text_color="#fff", font=("Arial", 18))
    num_panels_label.pack(pady=5)
    num_panels_entry = customtkinter.CTkEntry(app)
    num_panels_entry.pack(pady=5)

    consumption_label = customtkinter.CTkLabel(app, text="Enter Monthly Consumption (kWh):", text_color="#fff", font=("Arial", 18))
    consumption_label.pack(pady=5)
    consumption_entry = customtkinter.CTkEntry(app)
    consumption_entry.pack(pady=5)

    calculate_button = customtkinter.CTkButton(app, text="Calculate and Plot", command=calculate_and_plot, fg_color="#2A8C55")
    calculate_button.pack(pady=10)

    result_label = customtkinter.CTkLabel(app, text="", font=customtkinter.CTkFont(size=18), text_color="#fff")
    result_label.pack(pady=10)

def home_optimizer_ui():
    app.geometry("1000x900")
    

    customtkinter.set_appearance_mode("light")

    sidebar_frame = customtkinter.CTkFrame(master=app, fg_color="#2A8C55",  width=176, height=650, corner_radius=0)
    sidebar_frame.pack_propagate(0)
    sidebar_frame.pack(fill="y", anchor="w", side="left")

    logo_img_data = Image.open("logo.png")
    logo_img = customtkinter.CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(77.68, 85.42))

    customtkinter.CTkLabel(master=sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")

    analytics_img_data = Image.open("analytics_icon.png")
    analytics_img = customtkinter.CTkImage(dark_image=analytics_img_data, light_image=analytics_img_data)

    customtkinter.CTkButton(master=sidebar_frame, image=analytics_img, text="Home", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w", command=switch_to_home).pack(anchor="center", ipady=5, pady=(60, 0))

    package_img_data = Image.open("package_icon.png")
    package_img = customtkinter.CTkImage(dark_image=package_img_data, light_image=package_img_data)

    customtkinter.CTkButton(master=sidebar_frame, image=package_img, text="Solar Calculator", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w", command=switch_to_solar_calculator).pack(anchor="center", ipady=5, pady=(16, 0))

    list_img_data = Image.open("list_icon.png")
    list_img = customtkinter.CTkImage(dark_image=list_img_data, light_image=list_img_data)
    customtkinter.CTkButton(master=sidebar_frame, image=list_img, text="Home Optimiser", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w", command=switch_to_home_optimizer).pack(anchor="center", ipady=5, pady=(16, 0))

    returns_img_data = Image.open("returns_icon.png")
    returns_img = customtkinter.CTkImage(dark_image=returns_img_data, light_image=returns_img_data)
    customtkinter.CTkButton(master=sidebar_frame, image=returns_img, text="Carbon Footprint", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w", command=switch_to_carbon_footprint_calculator).pack(anchor="center", ipady=5, pady=(16, 0))

    def submit_answers():
        try:
            house_size = float(house_size_entry.get())
            num_appliances = int(num_appliances_entry.get())
            energy_type = energy_type_var.get()

            if not energy_type:
                raise ValueError("Please select an energy type.")

            solution = get_energy_optimization_solution(house_size, num_appliances, energy_type)

            messagebox.showinfo("Optimization Solution", solution)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid inputs.")

    house_size_label = customtkinter.CTkLabel(app, text="Enter House Size (m²):", text_color="#fff", font=("Arial", 18))
    house_size_label.pack(pady=5)
    house_size_entry = customtkinter.CTkEntry(app)
    house_size_entry.pack(pady=5)

    num_appliances_label = customtkinter.CTkLabel(app, text="Enter Number of Appliances:", text_color="#fff", font=("Arial", 18))
    num_appliances_label.pack(pady=5)
    num_appliances_entry = customtkinter.CTkEntry(app)
    num_appliances_entry.pack(pady=5)

    energy_type_label = customtkinter.CTkLabel(app, text="Select Energy Type:", text_color="#fff", font=("Arial", 18))
    energy_type_label.pack(pady=5)
    energy_type_var = customtkinter.StringVar(value="Electrical")
    energy_type_menu = customtkinter.CTkOptionMenu(app, variable=energy_type_var, values=["Electricity", "Gas", "Solar"])
    energy_type_menu.pack(pady=5)

    submit_button = customtkinter.CTkButton(app, text="Submit", command=submit_answers , fg_color="#2A8C55")
    submit_button.pack(pady=10)

def carbon_footprint_ui():
    app.geometry("1000x900")
    

    customtkinter.set_appearance_mode("light")

    sidebar_frame = customtkinter.CTkFrame(master=app, fg_color="#2A8C55",  width=176, height=650, corner_radius=0)
    sidebar_frame.pack_propagate(0)
    sidebar_frame.pack(fill="y", anchor="w", side="left")

    logo_img_data = Image.open("logo.png")
    logo_img = customtkinter.CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(77.68, 85.42))

    customtkinter.CTkLabel(master=sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")

    analytics_img_data = Image.open("analytics_icon.png")
    analytics_img = customtkinter.CTkImage(dark_image=analytics_img_data, light_image=analytics_img_data)

    customtkinter.CTkButton(master=sidebar_frame, image=analytics_img, text="Home", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w", command=switch_to_home).pack(anchor="center", ipady=5, pady=(60, 0))

    package_img_data = Image.open("package_icon.png")
    package_img = customtkinter.CTkImage(dark_image=package_img_data, light_image=package_img_data)

    customtkinter.CTkButton(master=sidebar_frame, image=package_img, text="Solar Calculator", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w", command=switch_to_solar_calculator).pack(anchor="center", ipady=5, pady=(16, 0))

    list_img_data = Image.open("list_icon.png")
    list_img = customtkinter.CTkImage(dark_image=list_img_data, light_image=list_img_data)
    customtkinter.CTkButton(master=sidebar_frame, image=list_img, text="Home Optimiser", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w", command=switch_to_home_optimizer).pack(anchor="center", ipady=5, pady=(16, 0))

    returns_img_data = Image.open("returns_icon.png")
    returns_img = customtkinter.CTkImage(dark_image=returns_img_data, light_image=returns_img_data)
    customtkinter.CTkButton(master=sidebar_frame, image=returns_img, text="Carbon Footprint", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w", command=switch_to_carbon_footprint_calculator).pack(anchor="center", ipady=5, pady=(16, 0))


    def calculate_carbon_footprint():
        try:
            energy_consumed1 = float(energy_consumed_entry1.get())
            energy_consumed2 = float(energy_consumed_entry2.get())
            energy_consumed3 = float(energy_consumed_entry3.get())

            carbon_footprint1 = energy_consumed1 * 0.4
            carbon_footprint2 = energy_consumed2 * 0.184
            carbon_footprint3 = energy_consumed3 * 0
            carbon_footprint = carbon_footprint1 + carbon_footprint2 + carbon_footprint3
            result_label.config(text=f"Estimated Carbon Footprint: {carbon_footprint:.2f} kg CO2")

            fig = plot_graph2(energy_consumed1, energy_consumed2, energy_consumed3)
            canvas = FigureCanvasTkAgg(fig, master=app)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(pady=10)
            canvas.draw()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid inputs.")

    energy_consumed_label1 = customtkinter.CTkLabel(app, text="Enter Energy Consumption (kWh) for Gas:", text_color="#fff", font=("Arial", 18))
    energy_consumed_entry1 = customtkinter.CTkEntry(app)
    energy_consumed_label2 = customtkinter.CTkLabel(app, text="Enter Energy Consumption (kWh) for Electricity:", text_color="#fff", font=("Arial", 18))
    energy_consumed_entry2 = customtkinter.CTkEntry(app)
    energy_consumed_label3 = customtkinter.CTkLabel(app, text="Enter Energy Consumption (kWh) for Solar:", text_color="#fff", font=("Arial", 18))
    energy_consumed_entry3 = customtkinter.CTkEntry(app)
    energy_consumed_label1.pack(pady=10)
    energy_consumed_entry1.pack(pady=10)
    energy_consumed_label2.pack(pady=10)
    energy_consumed_entry2.pack(pady=10)
    energy_consumed_label3.pack(pady=10)
    energy_consumed_entry3.pack(pady=10)

    calculate_button = customtkinter.CTkButton(app, text="Calculate Carbon Footprint", command=calculate_carbon_footprint, fg_color="#2A8C55")
    calculate_button.pack(pady=10)

    result_label = customtkinter.CTkLabel(app, text="", text_color="#fff", font=("Arial", 18))
    result_label.pack(pady=10)

def get_energy_optimization_solution(house_size, num_appliances, energy_type):
    try:
        openai.api_key = ""
        prompt = (
            f"Optimize energy usage for a house of {house_size} square meters with {num_appliances} appliances using {energy_type} energy."
        )

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200
        )

        return response.choices[0].text.strip()
    except Exception as e:
        return (
            "An error occurred while fetching optimization tips. Here are some general suggestions:\n"
            "- Consider upgrading to energy-efficient appliances.\n"
            "- Use smart thermostats and lighting controls to reduce energy consumption.\n"
            "- Install insulation and weatherstripping to reduce heating and cooling costs.\n"
            "- Explore solar energy as a renewable option.\n"
            "- Use LED lighting, which consumes less energy and lasts longer."
        )

# Main Application
app = tk.Tk()
app.title("Energy App")
app.geometry("600x480")

menu_frame = tk.Frame(app, bg="lightgray", height=1)

menu_buttons = [
    ("Home", switch_to_home),
    ("Solar Calculator", switch_to_solar_calculator),
    ("Home Optimizer", switch_to_home_optimizer),
    ("Carbon Footprint Calculator", switch_to_carbon_footprint_calculator)
]



def home_ui():
    app.geometry("1000x900")
    

    customtkinter.set_appearance_mode("light")

    sidebar_frame = customtkinter.CTkFrame(master=app, fg_color="#2A8C55",  width=176, height=650, corner_radius=0)
    sidebar_frame.pack_propagate(0)
    sidebar_frame.pack(fill="y", anchor="w", side="left")

    logo_img_data = Image.open("logo.png")
    logo_img = customtkinter.CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(77.68, 85.42))

    customtkinter.CTkLabel(master=sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")

    analytics_img_data = Image.open("analytics_icon.png")
    analytics_img = customtkinter.CTkImage(dark_image=analytics_img_data, light_image=analytics_img_data)

    customtkinter.CTkButton(master=sidebar_frame, image=analytics_img, text="Home", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w", command=switch_to_home).pack(anchor="center", ipady=5, pady=(60, 0))

    package_img_data = Image.open("package_icon.png")
    package_img = customtkinter.CTkImage(dark_image=package_img_data, light_image=package_img_data)

    customtkinter.CTkButton(master=sidebar_frame, image=package_img, text="Solar Calculator", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w", command=switch_to_solar_calculator).pack(anchor="center", ipady=5, pady=(16, 0))

    list_img_data = Image.open("list_icon.png")
    list_img = customtkinter.CTkImage(dark_image=list_img_data, light_image=list_img_data)
    customtkinter.CTkButton(master=sidebar_frame, image=list_img, text="Home Optimiser", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w", command=switch_to_home_optimizer).pack(anchor="center", ipady=5, pady=(16, 0))

    returns_img_data = Image.open("returns_icon.png")
    returns_img = customtkinter.CTkImage(dark_image=returns_img_data, light_image=returns_img_data)
    customtkinter.CTkButton(master=sidebar_frame, image=returns_img, text="Carbon Footprint", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w", command=switch_to_carbon_footprint_calculator).pack(anchor="center", ipady=5, pady=(16, 0))

    home_label = tk.Label(app, text="Welcome to the Energy Calculator App", font=("Arial", 24))
    home_label.pack(pady=20)
    home_img_data = Image.open("home_icon.jpeg")
    home_img = customtkinter.CTkImage(dark_image=home_img_data, light_image=home_img_data, size=(600,500))
    customtkinter.CTkLabel(master=app, image=home_img, text="", fg_color="transparent", anchor="w").pack(anchor="center", ipady=5, pady=(16, 0))


show_login_screen()
app.mainloop()
