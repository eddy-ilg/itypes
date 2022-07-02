#!/usr/bin/env python3

### --------------------------------------- ###
### Part of iTypes                          ###
### (C) 2022 Eddy ilg (me@eddy-ilg.net)     ###
### MIT License                             ###
### See https://github.com/eddy-ilg/itypes  ###
### --------------------------------------- ###

from itypes import bind_to_instance

class Car:
    def __init__(self, make, color):
        self._make = make
        self._color = color

red_audi = Car("Audi", "Red")
blue_ford = Car("Ford", "Blue")

#
# Bind a new method to Car class:
#
def print_car_info(self):
    print(f"car info: {self._color} {self._make}")

Car.print_info = print_car_info

red_audi.print_info()
blue_ford.print_info()

#
# Bind a new method to red_audi instance:
#
def drive_fast(self):
    print(f"{self._color} {self._make} drives fast!")

bind_to_instance(red_audi, drive_fast, 'drive_fast')

red_audi.drive_fast()
# This causes an error:
# blue_ford.drive_fast()