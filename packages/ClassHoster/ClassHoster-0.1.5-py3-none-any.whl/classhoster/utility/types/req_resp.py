#!/usr/bin/env python3

from dataclasses import dataclass

@dataclass
class GenericRequest:
    function: str
    args    : dict