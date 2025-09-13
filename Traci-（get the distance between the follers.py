# Step 1: Add modules to provide access to specific libraries and functions
import os  # Module provides functions to handle file paths, directories, environment variables
import sys  # Module provides access to Python-specific system parameters and functions

# Step 2: Establish path to SUMO (SUMO_HOME)
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")

# Step 3: Add Traci module to provide access to specific libraries and functions
import traci  # Static network information (such as reading and analyzing network files)

# Step 4: Define Sumo configuration
Sumo_config = [
    'sumo-gui',
    '-c', 'Traci.sumocfg',
    '--step-length', '0.05',
    '--delay', '1000',
    '--lateral-resolution', '0.1'
]

# Step 5: Open connection between SUMO and Traci
traci.start(Sumo_config)

# Step 6: Define Variables
vehicle_speed = 0
total_speed = 0

# Step 7: Define Functions
# ---------------------------------------------------------------------------
# We provide helpers to get the leader (front vehicle) and follower (back vehicle)
# distances for a given vehicle ID. Distances follow SUMO definitions:
#  - Leader gap is returned by traci.vehicle.getLeader(vehID, dist)
#  - Follower gap is returned by traci.vehicle.getFollower(vehID, dist)
# If no leader/follower exists, we return None for that field.

LOOK_FRONT = 200.0  # meters to look ahead for leader (can be tuned)
LOOK_BACK  = 200.0  # meters to look back for follower (can be tuned)

def get_front_back(veh_id, look_front=LOOK_FRONT, look_back=LOOK_BACK):
    """
    Return a dict with front/back vehicle IDs and gaps (meters) for veh_id.
    {
        'front_id': str | None,
        'front_gap': float | None,
        'back_id': str | None,
        'back_gap': float | None
    }
    """
    info = {'front_id': None, 'front_gap': None, 'back_id': None, 'back_gap': None}

    # Front (leader)
    try:
        leader = traci.vehicle.getLeader(veh_id, look_front)
        # If a leader exists, SUMO returns (vehID, gap); otherwise returns None
        if leader is not None:
            info['front_id'], info['front_gap'] = leader[0], float(leader[1])
    except traci.TraCIException:
        pass

    # Back (follower)
    try:
        fol_id, fol_gap = traci.vehicle.getFollower(veh_id, look_back)
        # If no follower, fol_id is an empty string; unify to None
        if fol_id != "":
            info['back_id'], info['back_gap'] = fol_id, float(fol_gap)
    except traci.TraCIException:
        pass

    return info

def _fmt(x, nd=2):
    try:
        return f"{float(x):.{nd}f}"
    except Exception:
        return "NA"

def print_front_back(veh_id, look_front=LOOK_FRONT, look_back=LOOK_BACK):
    """Pretty-print leader/follower information for veh_id."""
    fb = get_front_back(veh_id, look_front, look_back)
    f_id = fb['front_id'] if fb['front_id'] is not None else "None"
    b_id = fb['back_id']  if fb['back_id']  is not None else "None"
    f_gap = _fmt(fb['front_gap'])
    b_gap = _fmt(fb['back_gap'])
    print(f"[{veh_id}] FRONT={f_id} (gap={f_gap} m) | BACK={b_id} (gap={b_gap} m)")
# ---------------------------------------------------------------------------

# Step 8: Take simulation steps until there are no more vehicles in the network
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()  # Move simulation forward 1 step
    # Here you can decide what to do with simulation data at each step
    if 'veh1' in traci.vehicle.getIDList():
        vehicle_speed = traci.vehicle.getSpeed('veh1')
        total_speed = total_speed + vehicle_speed

        # NEW: print front/back distances of veh1 at every step
        print_front_back('veh1')           # <-- (1) show distances
        # fb = get_front_back('veh1')      # <-- (2) alternatively get raw dict for your logic

    # step_count = step_count + 1
    print(f"Vehicle speed: {vehicle_speed} m/s")

# Step 9: Close connection between SUMO and Traci
traci.close()
