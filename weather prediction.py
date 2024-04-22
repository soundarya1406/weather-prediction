import tkinter as tk
import requests
from PIL import Image, ImageTk
from io import BytesIO
from datetime import datetime
import matplotlib.pyplot as plt

def get_weather(city):
    api_key = "9f6e03eadbda07742960fd8116d0cefa"
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] == "200":
            return data["list"]
        else:
            return {"error": data["message"]}
    except Exception as e:
        return {"error": "An error occurred while fetching weather data"}

def update_weather():
    city = city_entry.get()
    weather_info = get_weather(city)
    if "error" in weather_info:
        result_label.config(text=weather_info["error"], fg="red")
    else:
        # Assuming the first entry in weather_info contains the current weather data
        current_weather = weather_info[0]
        temperature = current_weather.get("main", {}).get("temp")
        description = current_weather.get("weather", [{}])[0].get("description")
        humidity = current_weather.get("main", {}).get("humidity")
        wind_speed = current_weather.get("wind", {}).get("speed")
        
        if temperature is not None:
            result_label.config(text=f"Temperature: {temperature}°C\n"
                                      f"Description: {description}\n"
                                      f"Humidity: {humidity}%\n"
                                      f"Wind Speed: {wind_speed} m/s", fg="black")
        else:
            result_label.config(text="Temperature data not available.", fg="red")



def plot_graph(weather_data):
    timestamps = []
    temperatures = []
    
    for entry in weather_data:
        if "main" in entry and "temp" in entry["main"] and "dt" in entry:
            timestamps.append(datetime.fromtimestamp(entry["dt"]))
            temperatures.append(entry["main"]["temp"])

    if timestamps and temperatures:
        plt.figure(figsize=(8, 4))
        plt.plot(timestamps, temperatures, marker='o', linestyle='-')
        plt.title("Hourly Temperature")
        plt.xlabel("Time")
        plt.ylabel("Temperature (°C)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Convert the plot to an image
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        
        # Convert image buffer to tkinter-compatible image
        img = Image.open(buffer)
        return ImageTk.PhotoImage(img)
    else:
        return None

def display_graph():
    city = city_entry.get()
    weather_data = get_weather(city)
    
    if "error" in weather_data:
        result_label.config(text=weather_data["error"], fg="red")
    else:
        graph_image = plot_graph(weather_data)
        if graph_image:
            graph_label.config(image=graph_image)
            graph_label.image = graph_image  # Keep a reference to avoid garbage collection
            result_label.config(text="", fg="black")
        else:
            result_label.config(text="Temperature data not available for plotting.", fg="red")

# Create tkinter window
window = tk.Tk()
window.title("Weather Application")
window.geometry("800x600")

# Create city input label and entry
city_label = tk.Label(window, text="Enter City:", font=("Arial", 12))
city_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

city_entry = tk.Entry(window, font=("Arial", 12))
city_entry.grid(row=0, column=1, padx=5, pady=5)

# Create update button
update_button = tk.Button(window, text="Update Weather", command=update_weather, font=("Arial", 12))
update_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

# Create graph button
graph_button = tk.Button(window, text="Display Graph", command=display_graph, font=("Arial", 12))
graph_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# Create graph label
graph_label = tk.Label(window)
graph_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Create result label to display weather information
result_label = tk.Label(window, text="", font=("Arial", 12), wraplength=600, justify="left")
result_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Start the tkinter event loop
window.mainloop()
