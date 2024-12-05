#!/usr/bin/env python3

from classhoster.utility.tools.timer import Timer

class ZixClass:
    @staticmethod
    def whats_my_name():
        return "Zix Was Here"

class TimeClass:
    def __init__(self):
        self.seconds_passed = 0
        self.timer = Timer(1.0, self._increment_seconds)
        self.timer.start()

    def _increment_seconds(self):
        self.seconds_passed += 1

    def get_seconds_passed(self):
        return self.seconds_passed

class BucketClass:
    def __init__(self):
        self.things = 0
    def add_to_bucket(self, things: int):
        self.things += things
        return self.things
    def sub_from_bucket(self, things: int):
        self.things -= things
        return self.things