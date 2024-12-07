"""
masterppl.py - Master PPL file handler for syringe pump control

This module provides the masterppl class for managing multiple syringe pumps through
a master PPL (Pump Protocol Language) file. Based on the format developed by
Tim Burgess for SyringePumpPro.

Classes:
    masterppl: Manages multiple pump configurations in a master PPL file

Author: Faisal Shahbaz
Based on: SyringePumpPro by Tim Burgess (https://SyringePumpPro.com)
"""

from .utilities import decompose_dict, factor_check

class masterppl:
    """
    Master PPL file handler for controlling multiple syringe pumps.
    
    This class manages multiple pump configurations through a master PPL file,
    allowing coordinated control of multiple pumps with different addresses.
    
    Attributes:
        file: File object for writing PPL commands
        adrs (list): List of pump addresses being controlled
        
    Example:
        >>> with open('master.ppl', 'w') as master_file:
        ...     master = masterppl(master_file)
        ...     master.add(1, pump1)
        ...     master.add(2, pump2)
        ...     master.quickset({1: pump1, 2: pump2})
    """
    
    def __init__(self, file, adrs=[]):
        """
        Initialize master PPL controller.
        
        Args:
            file: File object for writing PPL commands
            adrs (list, optional): Initial list of pump addresses. Defaults to empty list.
        """
        self.file = file
        self.adrs = adrs

    def add(self, adr: int, ppl):
        """
        Add a pump configuration to the master file.
        
        Args:
            adr (int): Address to assign to the pump
            ppl: pump object containing the pump's configuration
            
        Effect:
            Writes pump address and configuration commands to master file
        """
        self.adrs.append(adr)
        self.file.write(f"Set adr={adr}\n")
        self.file.write(f"call {ppl.file.name}\n")

    def clearall(self):
        """
        Clear all pump configurations.
        
        Writes clear infusion (cldinf), clear withdrawal (cldwdr),
        and disable (dis) commands for all registered pump addresses.
        """
        for adr in self.adrs:
            self.file.write(f"{adr}cldinf\n{adr}cldwdr\n{adr}dis\n")

    def beepall(self):
        """
        Trigger beep sound on all registered pumps.
        """
        for adr in self.adrs:
            self.file.write(f"{adr}buz13\n")
    
    def quickset(self, all: dict):
        """
        Quickly configure multiple pumps.
        
        Args:
            all (dict): Dictionary mapping pump addresses to their PPL configurations
            
        Effect:
            Adds all pumps, clears their configurations, and triggers beep
        """
        for tuples in all.items():
            self.add(*tuples)
        self.clearall()
        self.beepall()
