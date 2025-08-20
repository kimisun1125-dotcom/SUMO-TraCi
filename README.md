<img width="209" height="105" alt="image" src="https://github.com/user-attachments/assets/99ead5bc-f0d1-4a0a-ae4b-3e37a250d745" /># SUMO Simulation Platform Setup

## 1. Install SUMO

* Download and install **SUMO 1.13.0** (or later) from the official website:
  👉 [https://sumo.dlr.de/docs/Downloads.php](https://sumo.dlr.de/docs/Downloads.php)

* After installation, you will have two main applications:

  * **sumo-gui** (graphical simulation interface)
  * **netedit** (network editing tool)

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
