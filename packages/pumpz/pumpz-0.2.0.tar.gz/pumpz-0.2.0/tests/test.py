import pumpz as pz
import math

# Create file handles for PPL output
f_aq = open("aq.ppl", "w")
f_org = open("org.ppl", "w")
f_master = open("master.ppl", "w")

# Initialize two pumps with identical configuration
aq = pz.Pump(f_aq, 26.59, "mm", "mL")   # Pump for aqueous solution
org = pz.Pump(f_org, 26.59, "mm", "mL")  # Pump for organic solution

# Create master controller and configure both pumps
master = pz.masterppl(f_master)
master.quickset({0: org, 1: aq})  # Assign addresses 0 and 1

# Initialize both pumps with default settings
pz.Pump.init(aq, org)

# Initial withdrawal phase - both pumps
aq.rate(22, 20, "wdr")
org.rate(22, 20, "wdr")

# Aqueous pump infusion with delay
aq.rate(10, 20, "inf")
aq.pause(5 * 60)  # 5 minute pause
pz.Pump.sync(aq, org)  # Synchronize pumps

# Organic pump infusion with timing calculation
org.rate(10, 20, "inf")
t0 = math.ceil(org.time)  # Store current time
org.pause(60)  # 1 minute pause
pz.Pump.sync(aq, org)

# Withdrawal phase with calculated pause
aq.rate(22, 50, "wdr")
org.rate(22, 50, "wdr")
t1 = math.ceil(org.time)
pause_length = t0 + 500 - t1  # Calculate required pause
if pause_length < 0:
    print("Error: timing is incompatible")
org.pause(pause_length)
pz.Pump.sync(aq, org)

# Repeated infusion/withdrawal cycle
aq.loopstart(2)
org.loopstart(2)

aq.rate(22, 50, "inf")
org.rate(22, 50, "inf")
aq.rate(22, 50, "wdr")
org.rate(22, 50, "wdr")

aq.loopend()
org.loopend()

# Final infusion
aq.rate(22, 50, "inf")
org.rate(22, 50, "inf")

# Stop
pz.Pump.stop(aq,org)