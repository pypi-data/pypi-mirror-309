#!/usr/bin/env python3
import random

from classhoster.public.robot_api import whats_my_name
from classhoster.public.robot_api import add_to_bucket
from classhoster.public.robot_api import get_seconds_passed

who_was_here = whats_my_name()
items_in_bucket = add_to_bucket(1)
seconds = get_seconds_passed()

print(who_was_here)
print(f"{seconds} seconds have passed.")
print(f"There are {items_in_bucket} items in the bucket")