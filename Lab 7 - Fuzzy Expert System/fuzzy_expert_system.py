"""
Python script for fuzzy modelling of traffic light
controller.
:author: jimil
"""

"""
Model the given triangular membership of fuzzy input
and output variables.
"""
def triangular_function(x, low, mid, high):
    if x <= low:
        return 0.0
    elif x >= high:
        return 0.0
    elif low < x <= mid:
        return round((x - low) / (mid - low), 4)
    elif mid < x < high:
        return round((high - x) / (high - mid), 4)

"""
Arrival input fuzzy variable
"""
def get_arrival_membership(x):
    arrival = {"Few": 0.0, "Many": 0.0, "Too Many": 0.0}
    if 0 <= x <= 4:
        arrival["Few"] = triangular_function(x, 0.0, 2.0, 4.0)
    if 2 <= x <= 4:
        arrival["Many"] = triangular_function(x, 2.0, 4.0, 6.0)
    if 4 <= 6:
        arrival["Too Many"] = triangular_function(x, 4.0, 6.0, 6.0)
    return arrival

"""
Queue input fuzzy variable
"""
def get_queue_membership(x):
    queue = {"Small": 0.0, "Medium": 0.0, "Large": 0.0}
    if 0 <= x <= 4:
        queue["Small"] = triangular_function(x, 0.0, 2.0, 4.0)
    if 2 <= x <= 4:
        queue["Medium"] = triangular_function(x, 2.0, 4.0, 6.0)
    if 4 <= 6:
        queue["Large"] = triangular_function(x, 4.0, 6.0, 6.0)
    return queue

arrival = get_arrival_membership(4.8)
queue = get_queue_membership(2.0)
print("Arrival Membership: ", arrival)
print("Queue Membership  : ", queue)

inference_system = {"Small":  {"Few": "Short",  "Many": "Medium", "Too Many": "Medium"},
 "Medium": {"Few": "Longer", "Many": "Short",  "Too Many": "Medium"},
 "Large":  {"Few": "Longer", "Many": "Medium", "Too Many": "Short"}}

max_val = float("-inf")
output_var = ["Short", 0.0]
for arrival_var in arrival:
    for queue_var in queue:
        rule_val = round(min(arrival[arrival_var], queue[queue_var]), 2)
        if rule_val > max_val:
            output_var[0] = inference_system[queue_var][arrival_var]
            output_var[1] = rule_val
            max_val = rule_val
print("[OUTPUT]: [Extension Linguistic, Extension Membership] = ", output_var)

"""
defuzzification of fuzzy output
"""
def fuzzy_to_crisp(x, low, high):
    if x > 0.5:
        return low + x * (high - low)
    else:
        return high - x * (high - low)

extension_val = 0.0
if output_var[0] == "Short":
    extension_val = fuzzy_to_crisp(output_var[1], 0.0, 4.0)
elif output_var[0] == "Medium":
    extension_val = fuzzy_to_crisp(output_var[1], 2.0, 6.0)
elif output_var[0] == "Longer":
    extension_val = fuzzy_to_crisp(output_var[1], 4.0, 6.0)
print("[SIGNAL]: " + output_var[0] + " Extension with Value =", extension_val)

traffic = {"north": {"arrival": 3.4, "queue": 4.6},
           "south": {"arrival": 1.4, "queue": 2.6},
           "east" : {"arrival": 1.8, "queue": 2.8},
           "west" : {"arrival": 5.8, "queue": 1.9}}

for path in traffic:
   
    print("\n# -------- DECISION MAKING: " + path + " -------- #")
   
    print("\nINPUT STATE:")
    print("\nNorth: Arrival = " + str(traffic["north"]["arrival"]) + ", Queue = " + str(traffic["north"]["queue"]))    
    print("South: Arrival = " + str(traffic["south"]["arrival"]) + ", Queue = " + str(traffic["south"]["queue"]))
    print("East: Arrival = " + str(traffic["east"]["arrival"]) + ", Queue = " + str(traffic["east"]["queue"]))
    print("West: Arrival = " + str(traffic["west"]["arrival"]) + ", Queue = " + str(traffic["west"]["queue"]))
   
    # Fuzzifier
    arrival = get_arrival_membership(traffic[path]["arrival"])
    queue = get_queue_membership(traffic[path]["queue"])
   
    # Inference System
    max_val = -99
    output_var = ["Short", 0.0]
    for arrival_var in arrival:
        for queue_var in queue:
            rule_val = round(min(arrival[arrival_var], queue[queue_var]), 2)
            if rule_val > max_val:
                output_var[0] = inference_system[queue_var][arrival_var]
                output_var[1] = rule_val
                max_val = rule_val
               
    # Defuzzify
    extension_val = 0.0
    if output_var[0] == "Short":
        extension_val = fuzzy_to_crisp(output_var[1], 0.0, 4.0)
    elif output_var[0] == "Medium":
        extension_val = fuzzy_to_crisp(output_var[1], 2.0, 6.0)
    elif output_var[0] == "Longer":
        extension_val = fuzzy_to_crisp(output_var[1], 4.0, 6.0)
   
    print("\nOUTPUT STATE:\n")
    print(output_var[0] + " Extension with Value =", extension_val)
   
    # Simulation
    for path2 in traffic:
        if path != path2:
            traffic[path]["queue"] += round((extension_val * 0.25), 4)
            traffic[path]["queue"] += round((extension_val * 0.25), 4)
            traffic[path]["queue"] += round((extension_val * 0.25), 4)
        else:
            traffic[path]["queue"] = 0
