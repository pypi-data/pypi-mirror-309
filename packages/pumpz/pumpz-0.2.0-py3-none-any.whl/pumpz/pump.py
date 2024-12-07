import math
import sympy
from typing import TextIO, List, Dict, Optional, Union
from .utilities import decompose_dict, factor_check

"""
Much thanks to claude.ai for editing and adding comments/docstrings
Code is otherwise original, by me
"""

class Pump:
    """
    Controller class for individual syringe pumps.
    
    Attributes:
        file (TextIO): File object for writing pump commands
        dia (float): Diameter of syringe in mm
        rate_units (str): Units for flow rate ('mm', 'um', 'mh', 'uh')
        vol_units (str): Units for volume ('mcL', 'mL')
        time (float): Current time in seconds
        loop (List[int]): Stack of current loop counts
        phase_name (str): Current phase label
        phase_num (int): Current phase number
        phase_ref (Dict[str, int]): Dictionary mapping phase names to numbers
        sync_is_useable (bool): Whether sync functionality can be used
    """
    
    VALID_RATE_UNITS = {'mm', 'um', 'mh', 'uh'}
    VALID_VOL_UNITS = {'mcL', 'mL'}
    
    def __init__(
        self,
        file: TextIO,
        dia: float,
        rate_units: str = 'mm',
        vol_units: str = '',
        time: float = 0,
    ):
        """
        Initialize a new Pump controller.
        
        Args:
            file: File object for writing pump commands
            dia: Diameter of syringe in mm (0.1 to 50.0)
            rate_units: Flow rate units ('mm'=mL/min, 'um'=μL/min, 'mh'=mL/hr, 'uh'=μL/hr)
            vol_units: Volume units ('mcL' or 'mL', auto-selected if empty)
            time: Initial time in seconds
            
        Raises:
            ValueError: If diameter is invalid or units are incorrect
            TypeError: If file is not a file object
        """
        if not hasattr(file, 'write'):
            raise TypeError("file must be a writable file object")
        self.file = file

        if not isinstance(dia, (int, float)):
            raise TypeError("Diameter must be a number")
        if dia < 0.1 or dia > 50.0:
            raise ValueError('Diameter must be between 0.1 - 50.0 mm')
        self.dia = round(dia, 1)
        
        if not isinstance(time, (int, float)):
            raise TypeError("Time must be a number")
        self.time = round(time, 1)

        if rate_units not in self.VALID_RATE_UNITS:
            raise ValueError(f"rate_units must be one of {self.VALID_RATE_UNITS}")
        self.rate_units = rate_units
        
        self.loop: List[int] = []
        
        # Auto-select volume units based on diameter if not specified
        if vol_units == '':
            self.vol_units = 'mcL' if self.dia >= 14.0 else 'mL'
        else:
            if vol_units not in self.VALID_VOL_UNITS:
                raise ValueError(f"vol_units must be one of {self.VALID_VOL_UNITS}")
            self.vol_units = vol_units

        self.__dir = ''  # Current direction ('inf' or 'wdr')
        self.__rat = 0   # Current rate
        self.phase_name = ''
        self.phase_num = 1
        self.phase_ref: Dict[str, int] = {}
        self.sync_is_useable = True

    @staticmethod
    def init(*pumps: 'Pump') -> None:
        """
        Initialize multiple pumps with default values.
        
        Args:
            *pumps: Variable number of Pump objects to initialize
        """
        for pump in pumps:
            if not isinstance(pump, Pump):
                raise TypeError("All arguments must be Pump objects")
            pump.file.write(f"dia {pump.dia}\nal 1\nbp 1\nPF 0\n")

    def _phase_to_string(self, phase: Union[int, str]) -> str:
        """
        Convert a phase number or name to a two-digit string.
        
        Args:
            phase: Phase number (1-98) or phase name
            
        Returns:
            Two-digit string representation of phase number
            
        Raises:
            ValueError: If phase number is invalid
            KeyError: If phase name is not found
        """
        if isinstance(phase, int):
            if not (0 < phase < 99):
                raise ValueError('Phase number must be between 1 and 98')
            return str(phase).zfill(2)
        elif isinstance(phase, str):
            if phase not in self.phase_ref:
                raise KeyError(f'Phase name "{phase}" not found')
            return str(self.phase_ref[phase]).zfill(2)
        else:
            raise TypeError("Phase must be an integer or string")

    def _phase(self) -> None:
        """Write current phase to file and update phase tracking."""
        self.file.write(f'\nphase {self.phase_name}\n')
        if self.phase_name:
            self.phase_ref[self.phase_name] = self.phase_num
        self.phase_name = ''
        self.phase_num += 1
    
    def label(self, label: str) -> str:
        """
        Label the following phase with a custom name.
        
        Args:
            label: Custom name for the phase
            
        Returns:
            The input label string
            
        Raises:
            TypeError: If label is not a string
        """
        if not isinstance(label, str):
            raise TypeError("Label must be a string")
        self.phase_name = label
        return label

    def change_rate_units(self, rate_units: str) -> None:
        """
        Change the flow rate units for the pump.
        
        Args:
            rate_units: New rate units ('mm', 'um', 'mh', 'uh')
            
        Raises:
            ValueError: If rate_units is invalid
        """
        if rate_units not in self.VALID_RATE_UNITS:
            raise ValueError(f"rate_units must be one of {self.VALID_RATE_UNITS}")
        self.rate_units = rate_units

    def rate(self, rate: float, vol: float, direction: str) -> None:
        """
        Set pump flow rate, volume, and direction.
        
        Args:
            rate: Flow rate in current rate_units
            vol: Volume to pump in current vol_units
            direction: Pump direction ('inf' for infuse, 'wdr' for withdraw)
            
        Raises:
            ValueError: If direction is invalid or rate/volume are negative
            TypeError: If rate or volume are not numbers
        """
        if not isinstance(rate, (int, float)) or not isinstance(vol, (int, float)):
            raise TypeError("Rate and volume must be numbers")
        if rate <= 0 or vol <= 0:
            raise ValueError("Rate and volume must be positive")
        if direction not in ('inf', 'wdr'):
            raise ValueError("Direction must be 'inf' or 'wdr'")

        self._phase()
        self.__dir = direction
        self.__rat = rate

        self.file.write(f"fun rat\nrat {rate} {self.rate_units}\nvol {vol}\ndir {direction}\n")

        # Calculate time based on volume units and rate units
        v = vol / 1000 if self.vol_units == 'mcL' else vol
        
        time_factors = {
            'mm': v / rate * 60,
            'um': v * 1000 / rate * 60,
            'mh': v / rate * 3600,
            'uh': v * 1000 / rate * 3600
        }
        
        self.time += time_factors[self.rate_units] * self.getloop()

    def beep(self) -> None:
        """Write a beep command to the pump."""
        self._phase()
        self.file.write('fun bep\n')

    def pause(self, length: int, phases: int = 0) -> int:
        """
        Add pause phases to the pump program.
        
        Args:
            length: Pause duration in seconds
            phases: Internal counter for recursive calls
            
        Returns:
            Number of phases used to implement the pause
            
        Raises:
            ValueError: If length is negative
            TypeError: If length is not an integer
        """
        if not isinstance(length, int):
            raise TypeError("Pause length must be an integer")
        if length < 0:
            raise ValueError("Pause length must be non-negative")
            
        if length <= 99:
            self._phase()
            self.file.write(f"fun pas {length}\n")
            self.time += length * self.getloop()
            return phases + 1
            
        elif length <= 99 * 3:
            phases += self.pause(99)
            return phases + self.pause(length - 99)
            
        else:
            multiples = factor_check(decompose_dict(sympy.factorint(length)))
            if multiples != (0, 0) and len(multiples) <= 3:
                for i in range(len(multiples) - 1):
                    self.loopstart(multiples[1 + i])
                    phases += 1
                self.pause(multiples[0])
                for i in range(len(multiples) - 1):
                    self.loopend()
                    phases += 1
            else:
                phases += self.pause(length % 50)
                length -= length % 50
                phases += self.pause(length)
        return phases

    def subprogram_label(self, label: int) -> None:
        """
        Define a subprogram start label.
        
        Args:
            label: Label number (0-99)
            
        Raises:
            ValueError: If label is out of range
        """
        if not isinstance(label, int) or not (0 <= label <= 99):
            raise ValueError("Label must be an integer between 0 and 99")
        self._phase()
        self.file.write(f'fun prl {str(label).zfill(2)}\n')

    def subprogram_select(self) -> None:
        """Write a subprogram selection input command."""
        self._phase()
        self.file.write('fun pri')

    def loopstart(self, count: int) -> None:
        """
        Start a loop with specified count.
        
        Args:
            count: Number of loop iterations
            
        Raises:
            ValueError: If count is negative or if nested too deeply
            TypeError: If count is not an integer
        """
        if not isinstance(count, int):
            raise TypeError("Loop count must be an integer")
        if count <= 0:
            raise ValueError("Loop count must be positive")
            
        self.loop.append(count)
        if len(self.loop) > 3:
            raise ValueError("Maximum of three nested loops exceeded")
        self._phase()
        self.file.write("fun lps\n")

    def loopend(self) -> None:
        """
        End the current loop.
        
        Raises:
            ValueError: If no loop is active
        """
        if not self.loop:
            raise ValueError("No active loop to end")
        self.file.write(f"\nphase\nfun lop {self.loop.pop()}\n")

    def getloop(self) -> int:
        """
        Get the total number of iterations for current nested loops.
        
        Returns:
            Product of all active loop counts
        """
        return sympy.prod(self.loop)

    def jump(self, phase: Union[int, str]) -> None:
        """
        Add a jump command to specified phase.
        
        Args:
            phase: Phase number or label to jump to
            
        Note:
            This command makes sync functionality unusable
        """
        self._phase()
        self.sync_is_useable = False
        self.file.write(f'fun jmp {self._phase_to_string(phase)}')

    def if_low(self, phase: Union[int, str]) -> None:
        """
        Add a conditional jump if TTL is low.
        
        Args:
            phase: Phase number or label to jump to
            
        Note:
            This command makes sync functionality unusable
        """
        self.sync_is_useable = False
        self._phase()
        self.file.write(f'fun if {self._phase_to_string(phase)}')

    def event_trap(self, phase: Union[int, str]) -> None:
        """
        Add an event trap command.
        
        Args:
            phase: Phase number or label to jump to on event
            
        Note:
            This command makes sync functionality unusable
        """
        self.sync_is_useable = False
        self._phase()
        self.file.write(f'fun evn {self._phase_to_string(phase)}')

    def event_trap_sq(self, phase: Union[int, str]) -> None:
        """
        Add a square wave event trap command.
        
        Args:
            phase: Phase number or label to jump to on event
            
        Note:
            This command makes sync functionality unusable
        """
        self.sync_is_useable = False
        self._phase()
        self.file.write(f'fun evs {self._phase_to_string(phase)}')

    def event_reset(self) -> None:
        """Add an event reset command."""
        self._phase()
        self.file.write('fun evr')

    def trg(self, num: int) -> None:
        """
        Add a trigger command.
        
        Args:
            num: Trigger number
            
        Raises:
            TypeError: If num is not an integer
        """
        if not isinstance(num, int):
            raise TypeError("Trigger number must be an integer")
        self._phase()
        self.file.write(f'fun trg {num}')

    def out(self, n: int) -> None:
        """
        Add an output command.
        
        Args:
            n: Output value
            
        Raises:
            TypeError: If n is not an integer
        """
        if not isinstance(n, int):
            raise TypeError("Output value must be an integer")
        self._phase()
        self.file.write(f'fun out {n}')

    @staticmethod
    def stop(*pumps: 'Pump') -> None:
        """
        Add stop commands to multiple pumps.
        
        Args:
            *pumps: Variable number of Pump objects to stop
        """
        for pump in pumps:
            if not isinstance(pump, Pump):
                raise TypeError("All arguments must be Pump objects")
            pump._phase()
            pump.file.write("fun stp\n")

    @staticmethod
    def sync(*pumps: 'Pump') -> None:
        """
        Synchronize multiple pumps by adding pauses to match the longest running pump.
        
        Args:
            *pumps: Variable number of Pump objects to synchronize
            
        Raises:
            ValueError: If any pump has sync_is_useable set to False
        """
        if not all(isinstance(p, Pump) for p in pumps):
            raise TypeError("All arguments must be Pump objects")
            
        max_time = max(p.time for p in pumps)
        
        for pump in pumps:
            if not pump.sync_is_useable:
                raise ValueError(f'Sync isn\'t useable with pump (contains jump or event commands)')
            time_diff = max_time - pump.time
            if time_diff > 0:
                pump.pause(math.ceil(time_diff))

