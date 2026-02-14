import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import io
import threading

class WeatherApp:

    def __init__(self, root):

        self.root = root
        self.root.title("☁️ Weather App")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#f8f9ff")   # Pastel Background

        # 🔑 YOUR API KEY
        self.api_key = "a5b82a6f39d0c0e69942b6c32d263631"

        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.icon_url = "https://openweathermap.org/img/wn/{}@2x.png"

        self.units = "metric"
        self.unit_symbol = "°C"

        self.setup_ui()
        self.get_weather("Mangalore,IN")


    # ================= UI =================

    def setup_ui(self):

        # Title
        tk.Label(
            self.root,
            text="🌤️ Weather Dashboard",
            font=("Segoe UI", 24, "bold"),
            bg="#f8f9ff",
            fg="#5f3dc4"
        ).pack(pady=20)


        # Search Box
        search_frame = tk.Frame(self.root, bg="#f8f9ff")
        search_frame.pack(pady=10)

        self.city_entry = tk.Entry(
            search_frame,
            font=("Segoe UI", 12),
            width=22,
            justify="center",
            bd=0,
            bg="white"
        )
        self.city_entry.pack(side="left", padx=8, ipady=6)
        self.city_entry.insert(0, "Mangalore,IN")


        tk.Button(
            search_frame,
            text="Search",
            command=self.get_weather_manual,
            font=("Segoe UI", 11, "bold"),
            bg="#b197fc",
            fg="white",
            bd=0,
            width=8
        ).pack(side="left", padx=5)


        self.unit_btn = tk.Button(
            search_frame,
            text="°F",
            command=self.toggle_units,
            font=("Segoe UI", 10, "bold"),
            bg="#63e6be",
            fg="#063",
            bd=0,
            width=5
        )
        self.unit_btn.pack(side="left", padx=5)


        # Card (Main Panel)
        self.card = tk.Frame(
            self.root,
            bg="white",
            bd=0
        )
        self.card.pack(pady=25, padx=30, fill="both", expand=True)


        # Location
        self.location_lbl = tk.Label(
            self.card,
            text="Loading...",
            font=("Segoe UI", 20, "bold"),
            bg="white",
            fg="#343a40"
        )
        self.location_lbl.pack(pady=15)


        # Icon + Temp
        mid_frame = tk.Frame(self.card, bg="white")
        mid_frame.pack(pady=10)

        self.icon_lbl = tk.Label(
            mid_frame,
            text="🌥️",
            font=("Segoe UI", 55),
            bg="white"
        )
        self.icon_lbl.pack(side="left", padx=15)


        self.temp_lbl = tk.Label(
            mid_frame,
            text="--°C",
            font=("Segoe UI", 46, "bold"),
            bg="white",
            fg="#ff922b"
        )
        self.temp_lbl.pack(side="left")


        # Condition
        self.condition_lbl = tk.Label(
            self.card,
            text="",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg="#868e96"
        )
        self.condition_lbl.pack(pady=5)


        # Info Panel
        info_frame = tk.Frame(self.card, bg="#f1f3ff")
        info_frame.pack(pady=20, padx=25, fill="x")


        self.humidity_lbl = tk.Label(
            info_frame,
            font=("Segoe UI", 12, "bold"),
            bg="#f1f3ff",
            fg="#495057"
        )
        self.humidity_lbl.grid(row=0, column=0, padx=20, pady=10)


        self.wind_lbl = tk.Label(
            info_frame,
            font=("Segoe UI", 12, "bold"),
            bg="#f1f3ff",
            fg="#495057"
        )
        self.wind_lbl.grid(row=1, column=0, padx=20, pady=10)


        self.pressure_lbl = tk.Label(
            info_frame,
            font=("Segoe UI", 12, "bold"),
            bg="#f1f3ff",
            fg="#495057"
        )
        self.pressure_lbl.grid(row=2, column=0, padx=20, pady=10)


        # Status
        self.status_lbl = tk.Label(
            self.card,
            text="Ready",
            font=("Segoe UI", 11, "italic"),
            bg="white",
            fg="#51cf66"
        )
        self.status_lbl.pack(pady=15)


        # Footer
        tk.Label(
            self.root,
            text="Designed with 💙",
            font=("Segoe UI", 9),
            bg="#f8f9ff",
            fg="#adb5bd"
        ).pack(pady=8)


    # ================= WEATHER =================

    def get_weather_manual(self):

        city = self.city_entry.get().strip()

        if ",IN" not in city.upper():
            city = f"{city},IN"

        self.get_weather(city)


    def get_weather(self, city):

        self.status_lbl.config(text="Fetching...")
        self.root.update()


        def fetch():

            try:

                url = f"{self.base_url}/weather?q={city}&appid={self.api_key}&units={self.units}"

                r = requests.get(url, timeout=10)
                data = r.json()

                if data.get("cod") == 200:
                    self.root.after(0, lambda: self.display_weather(data))
                else:
                    self.root.after(0, lambda: self.show_error(data))

            except Exception as e:

                msg = str(e)
                self.root.after(0, lambda m=msg: self.show_network_error(m))


        threading.Thread(target=fetch, daemon=True).start()


    def display_weather(self, data):

        city = data["name"]
        country = data["sys"]["country"]

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]

        desc = data["weather"][0]["description"]
        icon = data["weather"][0]["icon"]


        self.location_lbl.config(text=f"{city}, {country}")
        self.temp_lbl.config(text=f"{temp:.1f}{self.unit_symbol}")
        self.condition_lbl.config(text=desc.title())

        self.humidity_lbl.config(text=f"💧 Humidity: {humidity}%")
        self.wind_lbl.config(text=f"💨 Wind: {wind} km/h")
        self.pressure_lbl.config(text=f"📊 Pressure: {pressure} hPa")

        self.status_lbl.config(text="Updated ✓")

        self.load_icon(icon)


    def load_icon(self, code):

        def load():

            try:

                url = self.icon_url.format(code)

                r = requests.get(url, timeout=6)

                img = Image.open(io.BytesIO(r.content))
                img = img.resize((80, 80), Image.Resampling.LANCZOS)

                photo = ImageTk.PhotoImage(img)

                self.icon_lbl.config(image=photo, text="")
                self.icon_lbl.image = photo

            except:
                self.icon_lbl.config(text="🌥️")


        threading.Thread(target=load, daemon=True).start()


    # ================= UNITS =================

    def toggle_units(self):

        if self.units == "metric":

            self.units = "imperial"
            self.unit_symbol = "°F"
            self.unit_btn.config(text="°C")

        else:

            self.units = "metric"
            self.unit_symbol = "°C"
            self.unit_btn.config(text="°F")


        city = self.city_entry.get().strip()

        if city:
            self.get_weather(city)


    def show_error(self, data):

        msg = data.get("message", "Error")
        messagebox.showerror("Error", msg)


    def show_network_error(self, msg):

        messagebox.showerror("Network Error", msg)



# ================= RUN =================

if __name__ == "__main__":

    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
