For the automatic creation and sync of .PPL files, used for pump programming

Created by me while under employment with the University of Toronto, as goverened by: University of Toronto Governing Council | Inventions Policy

Below is documentation created by Claude AI:

# pumpz

A Python package for controlling syringe pumps using the PPL pump programming language.

Version: 0.2.0

Author: Faisal Shahbaz

## Installation

```python
>> pip install pumpz

import pumpz as pz
```

## Core Classes

### `masterppl`

A class for managing multiple pumps through a master PPL file.

#### Constructor

```python
masterppl(file, adrs=[])
```

**Parameters:**
- `file`: File object where PPL commands will be written
- `adrs`: List of pump addresses (optional)

#### Attributes
- `file`: File object for writing PPL commands
- `adrs`: List storing pump addresses

#### Methods

##### `add(adr: int, ppl)`
Add a pump configuration to the master file.
- **Parameters:**
  - `adr`: Integer address for the pump
  - `ppl`: pump object containing the pump's configuration
- **Returns:** None
- **Effect:** Writes pump address and configuration to the master file

##### `clearall()`
Clear all pump configurations.
- **Parameters:** None
- **Returns:** None
- **Effect:** Writes clear commands for all registered pump addresses

##### `beepall()`
Trigger beep sound on all pumps.
- **Parameters:** None
- **Returns:** None
- **Effect:** Writes beep commands for all registered pump addresses

##### `quickset(all: dict)`
Quickly configure multiple pumps.
- **Parameters:**
  - `all`: Dictionary mapping pump addresses to their PPL configurations
- **Returns:** None
- **Effect:** Adds all pumps, clears their configurations, and triggers beep

### `pump`

A class representing an individual syringe pump.

#### Constructor

```python
pump(file, dia: float, rate_units: str = 'mm', vol_units: str = '', time: float = 0)
```

**Parameters:**
- `file`: File object for PPL commands
- `dia`: Syringe diameter (0.1-50.0 mm)
- `rate_units`: Flow rate units ('mm' for mL/min, 'um' for μL/min, 'mh' for mL/hr, 'uh' for μL/h)
- `vol_units`: Volume units ('mcL' or 'mL', auto-selected based on diameter if not specified)
- `time`: Initial time in seconds

#### Attributes

##### Core Attributes
- `file`: File object for writing PPL commands
- `dia`: Float storing syringe diameter
- `time`: Float tracking elapsed time
- `rate_units`: String storing current rate units
- `vol_units`: String storing volume units

##### State Tracking
- `loop`: List tracking current loops
- `__dir`: String storing current direction ('inf' or 'wdr')
- `__rat`: Float storing current rate
- `phase_name`: String storing current phase name
- `phase_num`: Integer tracking current phase number
- `phase_ref`: Dictionary mapping phase names to numbers
- `sync_is_useable`: Boolean indicating if sync is available

#### Methods

##### Initialization and Configuration

###### `init(*args)`
Initialize pump(s) with default values.
- **Parameters:**
  - `*args`: Any number of pump objects
- **Returns:** None
- **Effect:** Sets diameter, alarm, buzzer, power failure mode

###### `change_rate_units(rate_units: str)`
Change the flow rate units.
- **Parameters:**
  - `rate_units`: New rate units ('mm', 'um', 'mh', 'uh')
- **Returns:** None
- **Effect:** Updates pump's rate units

###### `label(label: str)`
Label the next phase.
- **Parameters:**
  - `label`: String label for the phase
- **Returns:** The label string
- **Effect:** Sets phase_name for next phase

##### Flow Control

###### `rate(rate: float, vol: float, dir: str)`
Set flow rate, volume, and direction.
- **Parameters:**
  - `rate`: Flow rate in current rate units
  - `vol`: Volume in current volume units
  - `dir`: Direction ('inf' for infuse, 'wdr' for withdraw)
- **Returns:** None
- **Effect:** Configures pump flow and updates timing

###### `pause(length: int, phases = 0)`
Create pause in program execution.
- **Parameters:**
  - `length`: Duration in seconds
  - `phases`: Internal counter for recursive calls
- **Returns:** Number of phases used
- **Effect:** Creates optimal pause sequence

##### Loop Control

###### `loopstart(count: int)`
Start a loop with specified count.
- **Parameters:**
  - `count`: Number of loop iterations
- **Returns:** None
- **Effect:** Begins a loop sequence (max 3 nested)

###### `loopend()`
End the current loop.
- **Parameters:** None
- **Returns:** None
- **Effect:** Closes current loop sequence

###### `getloop()`
Get current loop multiplication factor.
- **Parameters:** None
- **Returns:** Product of all active loop counts
- **Effect:** None

##### Program Flow Control

###### `jump(phase: str)`
Jump to specified phase.
- **Parameters:**
  - `phase`: Phase number or name
- **Returns:** None
- **Effect:** Creates jump instruction, disables sync

###### `if_low(phase)`
Conditional jump if input is low.
- **Parameters:**
  - `phase`: Target phase
- **Returns:** None
- **Effect:** Creates conditional jump, disables sync

###### `event_trap(phase)`
Set event trap to specified phase.
- **Parameters:**
  - `phase`: Target phase
- **Returns:** None
- **Effect:** Creates event trap, disables sync

###### `event_trap_sq(phase)`
Set sequential event trap.
- **Parameters:**
  - `phase`: Target phase
- **Returns:** None
- **Effect:** Creates sequential event trap, disables sync

###### `event_reset()`
Reset event trap.
- **Parameters:** None
- **Returns:** None
- **Effect:** Resets event trap state

##### Signal and Output Control

###### `beep()`
Trigger beep sound.
- **Parameters:** None
- **Returns:** None
- **Effect:** Triggers pump buzzer

###### `trg(num: int)`
Set trigger.
- **Parameters:**
  - `num`: Trigger number
- **Returns:** None
- **Effect:** Sets specified trigger

###### `out(n)`
Set output signal.
- **Parameters:**
  - `n`: Output value
- **Returns:** None
- **Effect:** Sets output signal state

##### Synchronization

###### `stop(*args)`
Stop pump operation.
- **Parameters:**
  - `*args`: Pump objects to stop
- **Returns:** None
- **Effect:** Stops specified pumps

###### `sync(*args)`
Synchronize multiple pump operations.
- **Parameters:**
  - `*args`: Pump objects to synchronize
- **Returns:** None
- **Effect:** Adds pauses to align pump timing
- **Raises:** Exception if sync is not useable

## Utility Functions

### `decompose_dict(dict: dict)`
Decompose a dictionary into a list of its factors.
- **Parameters:**
  - `dict`: Dictionary of factors and their counts
- **Returns:** List of individual factors
- **Usage:** Internal use for timing calculations

### `factor_check(initial_factor, attempt=0)`
Check and optimize factors for timing calculations.
- **Parameters:**
  - `initial_factor`: Integer or list of factors
  - `attempt`: Recursion counter
- **Returns:** Tuple of optimized factors
- **Usage:** Internal use for pause optimization

## Error Handling

### Common Exceptions

1. **Diameter Error**
   ```python
   if self.dia < 0.1 or self.dia > 50.0:
       raise Exception('Diameter is invalid. Must be between 0.1 - 50.0 mm')
   ```

2. **Loop Nesting Error**
   ```python
   if len(self.loop) > 3:
       raise Exception("Up to three nested loops, you have too many")
   ```

3. **Sync Compatibility Error**
   ```python
   if arg.sync_is_useable == False:
       raise Exception(f'sync isn\'t useable with {arg}')
   ```

## Examples

### Basic Usage

```python
# Create a simple infusion program
with open('pump1.ppl', 'w') as pump_file:
    p1 = Pump(pump_file, dia=14.0, rate_units='mm')
    p1.init()
    p1.rate(1.0, 5.0, 'inf')  # Infuse 5mL at 1mL/min
```

### Multiple Pumps

```python
# Control multiple pumps with synchronization
with open('master.ppl', 'w') as master_file:
    master = masterppl(master_file)
    
    with open('pump1.ppl', 'w') as p1_file:
        p1 = Pump(p1_file, dia=14.0)
        p1.init()
        p1.rate(1.0, 5.0, 'inf')
        
    with open('pump2.ppl', 'w') as p2_file:
        p2 = Pump(p2_file, dia=10.0)
        p2.init()
        p2.rate(0.5, 2.0, 'inf')
    
    Pump.sync(p1, p2)  # Synchronize pump operations
    master.quickset({1: p1, 2: p2})
```

### Complex Program

```python
# Create a program with loops and events
with open('complex.ppl', 'w') as pump_file:
    p = pump(pump_file, dia=14.0)
    p.init()
    
    p.label("start")
    p.loopstart(5)  # Repeat 5 times
    p.rate(1.0, 1.0, 'inf')
    p.pause(30)
    p.rate(1.0, 1.0, 'wdr')
    p.loopend()
    
    p.event_trap("start")  # Jump to start on event
    p.beep()  # Signal completion
```


## Complete Working Example

This section demonstrates a complete example of controlling two pumps with synchronized operations.

### Example Setup

```python
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
```

### Program Flow

```python
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
```

### Generated Output Files

#### master.ppl
```ppl
Set adr=0
call org.ppl
Set adr=1
call aq.ppl
0cldinf
0cldwdr
0dis
1cldinf
1cldwdr
1dis
0buz13
1buz13
```

#### aq.ppl (Pump 1)
```ppl
dia 26.6
al 1
bp 1
PF 0

phase 
fun rat
rat 22 mm
vol 20
dir wdr

phase 
fun rat
rat 10 mm
vol 20
dir inf

phase 
fun lps

phase 
fun pas 60

phase
fun lop 5

phase 
fun pas 99

phase 
fun pas 81

phase 
fun rat
rat 22 mm
vol 50
dir wdr

phase 
fun lps

phase 
fun pas 5

phase
fun lop 61

phase 
fun lps

phase 
fun rat
rat 22 mm
vol 50
dir inf

phase 
fun rat
rat 22 mm
vol 50
dir wdr

phase
fun lop 2

phase 
fun rat
rat 22 mm
vol 50
dir inf

phase 
fun stp
```

#### org.ppl (Pump 0)
```ppl
dia 26.6
al 1
bp 1
PF 0

phase 
fun rat
rat 22 mm
vol 20
dir wdr

phase 
fun lps

phase 
fun pas 60

phase
fun lop 7

phase 
fun rat
rat 10 mm
vol 20
dir inf

phase 
fun pas 60

phase 
fun rat
rat 22 mm
vol 50
dir wdr

phase 
fun lps

phase 
fun pas 16

phase
fun lop 19

phase 
fun lps

phase 
fun rat
rat 22 mm
vol 50
dir inf

phase 
fun rat
rat 22 mm
vol 50
dir wdr

phase
fun lop 2

phase 
fun rat
rat 22 mm
vol 50
dir inf

phase 
fun stp
```

### Key Features Demonstrated

1. **Pump Synchronization**
   - Both pumps are initialized with identical configurations
   - Operations are synchronized using `pump.sync()`
   - Timing calculations ensure proper coordination

2. **Complex Flow Control**
   - Multiple rate changes
   - Withdrawal and infusion operations
   - Nested loops for repeated operations
   - Calculated pauses for timing alignment

3. **Master Control**
   - Multiple pump management through master PPL file
   - Address assignment and initialization
   - Coordinated start/stop operations

4. **Timing Management**
   - Use of mathematical calculations for pause lengths
   - Error checking for timing compatibility
   - Synchronized operations across multiple pumps

### Usage Notes

1. The example uses two identical pumps with 26.59mm diameter syringes
2. Flow rates are specified in mL/min (mm units)
3. Volumes are specified in mL
4. The program includes error checking for timing compatibility
5. The master PPL file coordinates both pumps through address assignments 0 and 1

This example demonstrates many of the package's key features including:
- Multi-pump coordination
- Complex timing calculations
- Loop operations
- Rate control
- Direction control
- Error checking
- Master/slave configuration

## Credits

All code is original by me, Faisal Shahbaz, except where edited by Claude AI

Documentation was written by Claude AI and edited by me

masterppl class based on the default master PPL file format by Tim Burgess, SyringePumpPro (https://SyringePumpPro.com)