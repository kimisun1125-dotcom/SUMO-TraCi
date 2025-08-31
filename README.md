# SUMO Simulation Platform Setup

## 1. Install SUMO

* Download and install **SUMO 1.13.0** (or later) from the official website:
  👉 [https://sumo.dlr.de/docs/Downloads.php](https://sumo.dlr.de/docs/Downloads.php)

* After installation, you will have two main applications:

  * **sumo-gui** (graphical simulation interface)
  * **netedit** (network editing tool)
<img width="209" height="105" alt="image" src="https://github.com/user-attachments/assets/99ead5bc-f0d1-4a0a-ae4b-3e37a250d745" />
---

## 2. Install Python

* Download Python from [python.org](https://www.python.org/downloads/)
* Ensure Python is added to your PATH environment.

---

## 3. Text Editor (Optional but Recommended)

* Install [Notepad++](https://notepad-plus-plus.org/) or use any preferred code editor (e.g., VS Code).

---


## 4. Project Directory Structure

```bash
SUMO-Simulation-Project/
│
├── data/                # Store downloaded OSM or tutorial files here
│   ├── pittsburgh/       # Example region: West East End Bridge
│   │   ├── osm.net.xml   # Network file generated from osmWebWizard
│   │   ├── osm.poly.xml  # Additional polygon data (e.g. buildings, POIs)
│   │   ├── osm.sumocfg   # Main SUMO config file for running the scenario
│   │   └── ...
│   └── other_region/     # You can add more regions here
│
├── scripts/              # Place your custom Python scripts here
│   └── run_simulation.py
│
└── README.md
```

---

## 5. Build the Simulation Platform

### Example: Pittsburgh West East End Bridge
<img width="240" height="377" alt="image" src="https://github.com/user-attachments/assets/b06a5ea4-3052-43bc-aeae-ff9212751af9" />
<img width="216" height="397" alt="image" src="https://github.com/user-attachments/assets/ce884c93-00c8-4611-961f-ce4a5ff08666" />
<img width="240" height="377" alt="image" src="https://github.com/user-attachments/assets/bc092697-8351-4d14-81be-5b5e76f9500f" />

I have selected the **West East End Bridge, Pittsburgh** as the simulation region.

If you want to change the region:

1. Navigate to the SUMO installation folder.
2. Open and run the following script:

```bash
python tools/osmWebWizard.py
```

3. The script will automatically open a browser interface where you can:

   * Search for a location directly on **OpenStreetMap**, or
   * Select from predefined areas.

---

## 6. Run the Simulation

* If you used `tools/osmWebWizard.py`, it will automatically generate the SUMO scenario.
* The generated files will be saved under your selected directory (e.g., `data/pittsburgh/`).
* Open the `.sumocfg` file with **sumo-gui** and click **Run** ▶️ to start the simulation.
---

✅ Done! You now have a running SUMO simulation platform with the flexibility to choose any area from OpenStreetMap.

https://github.com/user-attachments/assets/4e01ef28-6b31-4780-bcad-9a833614b625
------
🚦 TraCI & SUMO Interaction

After setting up the basic SUMO environment, you can use TraCI (Traffic Control Interface) to interact with the running SUMO simulation in real-time.
The following example shows how to retrieve a vehicle’s speed and position step by step.

🔑 Example 1: Retrieve Vehicle Speed and Position
Code Structure (Steps 1–9)

Import modules – os, sys for path and environment handling.

Set SUMO_HOME – Ensure the SUMO tools path is declared.

Import TraCI module – Provides the interface to communicate with SUMO.

Configure SUMO parameters – Load your .sumocfg file with sumo-gui.

Start connection – Launch SUMO and establish TraCI connection.

Define variables – Initialize placeholders for speed and other metrics.

Define functions – This part is flexible: you can modify it to get speed, position, delays, collisions, or any other vehicle-related data.

Simulation loop – Step through the simulation and extract information at each time step.

Close connection – Safely disconnect from SUMO once simulation ends.
import os
import sys

# Step 2: Establish SUMO_HOME
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")

# Step 3: Import TraCI
import traci

# Step 4: SUMO configuration
Sumo_config = [
    'sumo-gui',
    '-c', 'Traci.sumocfg',
    '--step-length', '0.05',
    '--delay', '1000',
    '--lateral-resolution', '0.1'
]

# Step 5: Start SUMO–TraCI connection
traci.start(Sumo_config)

# Step 6: Define variables
vehicle_speed = 0
total_speed = 0

# Step 7: Define function (can be extended for other info)
def get_vehicle_data(veh_id):
    if veh_id in traci.vehicle.getIDList():
        speed = traci.vehicle.getSpeed(veh_id)
        position = traci.vehicle.getPosition(veh_id)
        return speed, position
    return None, None

# Step 8: Simulation loop
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    speed, position = get_vehicle_data('veh1')
    if speed is not None:
        total_speed += speed
        print(f"Vehicle speed: {speed:.2f} m/s, position: {position}")

# Step 9: Close connection
traci.close()
✅ You can modify Step 7 (get_vehicle_data) to extract other details such as waiting time, lane ID, CO₂ emissions, etc.
