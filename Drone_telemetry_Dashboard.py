import tkinter as tk
import random
import math

altitude = 50.0
speed_kmph = 0.0
battery = 100.0
latitude = 17.385044
longitude = 78.486671

heading = 0
time_sec = 0

current_display_speed = 0
gps_x, gps_y = 120, 130


#  Window Setup
root = tk.Tk()
root.title("Drone Telemetry - Glass UI")
root.geometry("1000x550")
root.configure(bg="#0b1220")



def glass_panel(parent, width, height):
    panel = tk.Frame(
        parent,
        bg="#111827",
        width=width,
        height=height,
        highlightbackground="#1f2937",
        highlightthickness=1
    )
    panel.pack_propagate(False)
    return panel


# Speedometer 
def draw_meter_background():
    # Speed zones
    meter.create_arc(30, 30, 270, 270, start=240, extent=96,
                     style="arc", width=18, outline="#ef4444")
    meter.create_arc(30, 30, 270, 270, start=336, extent=48,
                     style="arc", width=18, outline="#f97316")
    meter.create_arc(30, 30, 270, 270, start=384, extent=96,
                     style="arc", width=18, outline="#22c55e")

    # Speed numbers
    for value in range(0, 101, 10):
        angle = -120 + (value / 100) * 240
        rad = math.radians(angle)
        x = 150 + 115 * math.cos(rad)
        y = 150 + 115 * math.sin(rad)

        meter.create_text(
            x, y,
            text=str(value),
            fill="white",
            font=("Arial", 9, "bold")
        )


def draw_speed(speed):
    meter.delete("needle")
    meter.delete("speed_text")

    if speed <= 40:
        color = "#22c55e"
    elif speed <= 60:
        color = "#facc15"
    else:
        color = "#ef4444"

    angle = -120 + (speed / 100) * 240
    rad = math.radians(angle)

    x = 150 + 105 * math.cos(rad)
    y = 150 + 105 * math.sin(rad)

    meter.create_line(150, 150, x, y,
                      width=4, fill=color, tags="needle")

    meter.create_oval(140, 140, 160, 160,
                      fill="#111827", outline=color, width=3)

    meter.create_text(150, 200,
                      text=f"{speed:.0f} km/h",
                      fill="white",
                      font=("Arial", 18, "bold"),
                      tags="speed_text")


def animate_speed(target):
    global current_display_speed

    difference = target - current_display_speed
    current_display_speed += difference * 0.08

    draw_speed(current_display_speed)
    root.after(16, lambda: animate_speed(target))


#  GPS Rotation
def rotate_drone(x, y, angle):
    size = 8
    rad = math.radians(angle)

    base_points = [(0, -size), (-size, size), (size, size)]
    rotated = []

    for px, py in base_points:
        rx = px * math.cos(rad) - py * math.sin(rad)
        ry = px * math.sin(rad) + py * math.cos(rad)
        rotated.append((x + rx, y + ry))

    return [coord for point in rotated for coord in point]


 # Main update function
def update():
    global altitude, speed_kmph, battery
    global latitude, longitude, heading
    global time_sec, gps_x, gps_y

    if time_sec >= 30:
        status.config(text="Simulation Completed", fg="#22c55e")
        return

    # Speed 
    if time_sec < 8:
        speed_kmph += random.uniform(6, 9)
    elif time_sec < 22:
        speed_kmph += random.uniform(-3, 3)
    else:
        speed_kmph -= random.uniform(3, 6)

    speed_kmph = max(0, min(speed_kmph, 100))

    # UAltitude
    altitude += random.uniform(-2, 3)
    altitude = max(0, altitude)

    # UBattery
    battery -= 0.2
    battery = max(0, battery)


    bar_height = 200 - (battery * 2)
    battery_canvas.coords(battery_fill, 0, bar_height, 40, 200)

    if battery > 50:
        bar_color = "#22c55e"
    elif battery > 20:
        bar_color = "#f97316"
    else:
        bar_color = "#ef4444"

    battery_canvas.itemconfig(battery_fill, fill=bar_color)

    # movement of GPS
    heading += random.uniform(-10, 10)
    rad = math.radians(heading)
    distance = speed_kmph * 0.04

    gps_x += distance * math.cos(rad)
    gps_y -= distance * math.sin(rad)

    coord_distance = speed_kmph * 0.000001
    latitude += coord_distance * math.cos(rad)
    longitude += coord_distance * math.sin(rad)

    gps_label.config(
        text=f"Lat: {latitude:.6f}\nLon: {longitude:.6f}"
    )

    gps_x = max(40, min(gps_x, 210))
    gps_y = max(50, min(gps_y, 210))

    gps.create_oval(gps_x - 2, gps_y - 2,
                    gps_x + 2, gps_y + 2,
                    fill="#00ffcc", outline="")

    new_shape = rotate_drone(gps_x, gps_y, heading)
    gps.coords(drone, *new_shape)

    alt_label.config(text=f"{altitude:.1f} m")
    bat_label.config(text=f"{battery:.1f} %")

    
    limited_alt = min(altitude, 200)
    altitude_canvas.coords(
        altitude_fill,
        10, 200 - limited_alt,
        50, 200
    )

    animate_speed(speed_kmph)

    time_sec += 1
    root.after(1000, update)


# Layout 
title = tk.Label(root,
                 text="DRONE TELEMETRY DASHBOARD",
                 font=("Arial", 20, "bold"),
                 fg="#38bdf8",
                 bg="#0b1220")
title.pack(pady=15)

main = tk.Frame(root, bg="#0b1220")
main.pack()

# Left panel
left = glass_panel(main, 250, 400)
left.grid(row=0, column=0, padx=20)

tk.Label(left, text="Altitude",
         fg="#9ca3af", bg="#111827").pack(anchor="w", padx=15)

alt_label = tk.Label(left, fg="white",
                     bg="#111827", font=("Arial", 14))
alt_label.pack(anchor="w", padx=15, pady=5)

altitude_canvas = tk.Canvas(left, width=60, height=200,
                            bg="#1e293b", highlightthickness=0)
altitude_canvas.pack(pady=10)

altitude_fill = altitude_canvas.create_rectangle(
    10, 200, 50, 200, fill="#38bdf8"
)

for val in range(0, 201, 50):
    altitude_canvas.create_text(
        55, 200 - val,
        text=str(val),
        fill="white",
        font=("Arial", 8)
    )

tk.Label(left, text="Battery",
         fg="#9ca3af", bg="#111827").pack(anchor="w", padx=15)

bat_label = tk.Label(left, fg="white",
                     bg="#111827", font=("Arial", 14))
bat_label.pack(anchor="w", padx=15, pady=5)

battery_canvas = tk.Canvas(left, width=40, height=200,
                           bg="#1e293b", highlightthickness=0)
battery_canvas.pack(pady=10)

battery_fill = battery_canvas.create_rectangle(
    0, 0, 40, 200, fill="#22c55e"
)

# Speed panel
mid = glass_panel(main, 320, 400)
mid.grid(row=0, column=1, padx=20)

meter = tk.Canvas(mid, width=300, height=300,
                  bg="#111827", highlightthickness=0)
meter.pack(pady=20)

draw_meter_background()

# GPS panel
right = glass_panel(main, 300, 400)
right.grid(row=0, column=2, padx=20)

gps = tk.Canvas(right, width=250, height=250,
                bg="#111827", highlightthickness=0)
gps.pack(pady=20)

gps_label = tk.Label(right,
                     text="Lat: 0.000000\nLon: 0.000000",
                     fg="white",
                     bg="#111827",
                     font=("Arial", 11))
gps_label.pack(pady=5)

gps.create_rectangle(20, 20, 230, 230, outline="#334155")

gps.create_text(125, 8, text="N", fill="#38bdf8", font=("Arial", 12, "bold"))
gps.create_text(125, 242, text="S", fill="#38bdf8", font=("Arial", 12, "bold"))
gps.create_text(242, 125, text="E", fill="#38bdf8", font=("Arial", 12, "bold"))
gps.create_text(8, 125, text="W", fill="#38bdf8", font=("Arial", 12, "bold"))

gps.create_line(125, 20, 125, 230, fill="#1f2937", dash=(4, 2))
gps.create_line(20, 125, 230, 125, fill="#1f2937", dash=(4, 2))

drone = gps.create_polygon(
    gps_x, gps_y - 8,
    gps_x - 6, gps_y + 6,
    gps_x + 6, gps_y + 6,
    fill="#00ffcc"
)

status = tk.Label(root,
                  text="Live Telemetry Running...",
                  fg="#facc15",
                  bg="#0b1220",
                  font=("Arial", 12))
status.pack(pady=15)

update()
root.mainloop()
