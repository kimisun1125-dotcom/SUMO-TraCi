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
import traci

# Step 4: Define SUMO configuration
Sumo_config = [
    'sumo-gui',
    '-c', 'Test1.sumocfg',
    '--step-length', '0.05',
    '--delay', '1000',
    '--lateral-resolution', '0.1'
]

# Step 5: Open connection between SUMO and Traci
traci.start(Sumo_config)

# Step 6: Define Variables
# Dictionary that maps TLSID + direction to a desired phase index
desired_phase_mapping = {
    'Node2_EW': 0,  # EW represents Eastbound-Westbound
    'Node2_NS': 2,  # NS represents Northbound-Southbound
    'Node5_EW': 0,  # EW represents Eastbound-Westbound
    'Node5_NS': 2,  # NS represents Northbound-Southbound
    # Add any other traffic lights in the route of emergency vehicles as needed
}

adjusted_tls = {}  # keep track of adjusted traffic lights to avoid repeated short-cycling
step = 0

# Step 7: Define Functions Determine if the emergency vehicle is on a north-south edge or east-west edge
    #based on the naming convention of the edges.
def get_emergency_vehicle_direction(vehicle_id):
    current_edge = traci.vehicle.getRoadID(vehicle_id).lower()
    print(f"Vehicle {vehicle_id} is on edge {current_edge}")
    if 'nb' in current_edge or 'sb' in current_edge:
        return 'NS'
    elif 'eb' in current_edge or 'wb' in current_edge:
        return 'EW'
    else:
        return None

def process_emergency_vehicles(desired_phase_mapping, adjusted_tls, step):
    """
    This function identifies emergency vehicles, adjusts traffic lights 
    for them if needed, and resets traffic lights when no longer in use.
    
    :param desired_phase_mapping: dict mapping "TLSID_direction" -> desired phase index
    :param adjusted_tls: dict tracking which traffic lights have been adjusted 
                        and what phase they're supposed to be in
    :param step: current simulation step counter
    :return: updated step counter
    """
    # Identify emergency vehicles
    emergency_vehicles = [
        veh for veh in traci.vehicle.getIDList()
        if traci.vehicle.getTypeID(veh) == "emergency"
    ]

    # Track which TLS are actively handled this step
    active_tls = set()

    for veh in emergency_vehicles:
        direction = get_emergency_vehicle_direction(veh)
        if direction:
            next_tls = traci.vehicle.getNextTLS(veh)
            print(f"next_tls for {veh}: {next_tls}")

            if next_tls:
                tls_info = next_tls[0]
                tlsID, linkIndex, distance, state = tls_info

                # Construct traffic light key (e.g. "Node2_EW")
                tl_key = f"{tlsID}_{direction}"
                desired_phase = desired_phase_mapping.get(tl_key)

                if desired_phase is not None:
                    current_phase = traci.trafficlight.getPhase(tlsID)
                    print(f"TLS {tlsID}, Current phase: {current_phase}, "
                          f"Desired phase: {desired_phase}")

                    # Mark this traffic light as active (emergency vehicle approaching)
                    active_tls.add(tlsID)

                    # Check if we have already adjusted this traffic light 
                    # for the desired phase
                    if tlsID not in adjusted_tls or adjusted_tls[tlsID] != desired_phase:
                        adjusted_tls[tlsID] = desired_phase  # Record desired phase
                        if current_phase == desired_phase:
                            # Extend the green phase if it's already in the correct one
                            new_duration = max(20, traci.trafficlight.getPhaseDuration(tlsID) + 10)
                            traci.trafficlight.setPhaseDuration(tlsID, new_duration)
                            print(f"Extended phase {current_phase} of {tlsID} to "
                                  f"{new_duration} seconds")
                        else:
                            # Shorten the current phase to get to desired phase sooner
                            traci.trafficlight.setPhaseDuration(tlsID, 0.1)
                            print(f"Shortened phase {current_phase} of {tlsID} to 1 second")

    # Reset traffic lights to normal operation if no emergency vehicle is approaching
    for tlsID in list(adjusted_tls.keys()):
        if tlsID not in active_tls:
            del adjusted_tls[tlsID]
            print(f"Resetting traffic light {tlsID} to normal operation.")

    step += 1
    return step

# Step 8: Take simulation steps until there are no more vehicles in the network
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()  # Move simulation forward by 1 step
    # Process emergency vehicles
    step = process_emergency_vehicles(desired_phase_mapping, adjusted_tls, step)

# Step 9: Close connection between SUMO and Traci
traci.close()
