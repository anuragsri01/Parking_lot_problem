"""
A program that runs as a parking lot application taking an input file and collect vechile registration number and driver age,
after that check for the nearest empty slot and alot it to the vechile for parking.
It also check for the parking lot capicity and if the parking lot is full it shows a message "Parking is full".
Build on Python 3.6 and can be run from a terminal.
"""

class ParkingSystem():
    def __init__(self):
        self.parking_lot_created = False
        self.parking_lot_size = 0
        self.parking_lot_available = 0
        self.slot_number_for_car = {}
        self.slot_number_for_age = {}
        self.slot_for_parking_available = []
        self.vechile_age_manager = {}
        self.age_vechile_manager = {}
        self.out_prefix_created_parking = 'Created parking of {} slots'
        self.out_prefix_parked_status = '''Car with vehicle registration number {} has been parked at slot number {}'''
        self.out_prefix_vacating_slot = '''Slot number {} vacated, the car with vehicle registration number {} left the space, the driver of the car was of age {}'''

        self.parking_command_manager_func_mapper = {
            'Park': self.validate_transaction_for_parking,
            'Create_parking_lot': self.validate_transaction_for_creating_slot,
            'Vehicle_registration_number_for_driver_of_age': self.vechile_registration_number_for_age,
            'Slot_numbers_for_driver_of_age': self.slot_for_age,
            'Slot_number_for_car_with_number': self.slot_for_given_car_number,
            'Leave': self.validate_transaction_for_leaving,
        }

    # checking the availability of the parking slot.
    def validate_transaction_for_parking(self, command):
#         Park KA-01-HH-1234 driver_age 21
        if len(self.slot_for_parking_available) == 0:
            return 'Parking is full cannot park any other car'
        else:
            parking_command = command.split(' ')
            if len(parking_command) != 4:
                return 'Error in parking command please check something is wrong'
            else:
                car_number = parking_command[1]
                driver_age = parking_command[3]
                smallest_slot_available = sorted(
                    self.slot_for_parking_available)[0]
                self.slot_for_parking_available.remove(smallest_slot_available)

                self.slot_number_for_age[smallest_slot_available] = driver_age

                self.slot_number_for_car[car_number] = smallest_slot_available

                if self.age_vechile_manager.get(driver_age, 0) == 0:
                    self.age_vechile_manager[driver_age] = []
                self.age_vechile_manager[driver_age].append(car_number)

            return self.out_prefix_parked_status.format(car_number, smallest_slot_available)


    # validating that the certain slot is now empty and can be used.
    def validate_transaction_for_leaving(self, command):
        
        if len(self.slot_for_parking_available) == self.parking_lot_size:
            return 'Error all parking lots are already free'
        else:
            command_leave = command.split(' ')
            if len(command_leave) < 2:
                return 'Error leave command requires slot number'
            else:
                try:
                    slot_number_to_leave = int(command_leave[1])
                    self.slot_for_parking_available.append(
                        slot_number_to_leave)
                    car_number_at_slot = ''
                    for keys,value in self.slot_number_for_car.items():
                        if value == slot_number_to_leave:
                            car_number_at_slot = keys
                            break
                    self.slot_number_for_car.pop(keys)
                    for keys, value in self.age_vechile_manager.items():
                        if car_number_at_slot in set(value):
                            age_of_that_car = keys
                            break
                    return self.out_prefix_vacating_slot.format(slot_number_to_leave, car_number_at_slot, age_of_that_car)
                except Exception as e:
                    return 'Error in vacating for the slot'

    def validate_transaction_for_creating_slot(self, command):
        if self.parking_lot_created:
            return "Error Parking Lot Can not be created again"
        else:
            if 'Create_parking_lot' in command:
                command_parking = command.split(' ')
                if len(command_parking) != 2:
                    return 'Error Creating Parking Lot Command is not correct'
                else:
                    try:
                        parking_lot_size = int(command_parking[1])
                    except Exception as e:
                        return 'Parking Lot size is not valid it should be INTEGER format {}'.format(e)
                    try:
                        self.parking_lot_created = True
                        self.parking_lot_size = parking_lot_size
                        self.slot_for_parking_available = list(range(
                            1, self.parking_lot_size+1))
                    except Exception as e:
                        return 'Something Failed while creating parking slots {}'.format(e)

            return self.out_prefix_created_parking.format(self.parking_lot_size)


    # alotting a parking slot for a certian age.
    def slot_for_age(self, command):
        age_command = command.split(' ')
        if len(age_command) != 2:
            return 'Error in command for fetching Slots for given age'
        else:
            all_slot_for_age = []
            for key, value in self.slot_number_for_age.items():
                if value == age_command[1]:
                    all_slot_for_age.append(key)
           
        return all_slot_for_age


    # checking a slot for a given car number.
    def slot_for_given_car_number(self, command):
        age_command=command.split(' ')
        if len(age_command) != 2:
            return 'Error in command for fetching Slots for given vechile number'
        else:
            if self.slot_number_for_car.get(age_command[1], 0) == 0:
                return 'No Car with given number plate in slot'
            else:
                return self.slot_number_for_car.get(age_command[1], 'null')

    def vechile_registration_number_for_age(self,command):
        vechile_command = command.split(' ')
        if len(vechile_command) != 2:
            return 'Error in command for fetching vechiles for given age'
        else:
            if self.age_vechile_manager.get(vechile_command[1], 0) == 0:
                return 'null'
            else:
                return self.age_vechile_manager.get(vechile_command[1])
    def command_manager(self, command):
        if 'Create_parking_lot' in command:
            return self.parking_command_manager_func_mapper['Create_parking_lot'](command)
        if 'Park' in command:
            return self.parking_command_manager_func_mapper['Park'](command)
        if 'Slot_numbers_for_driver_of_age' in command:
            return self.parking_command_manager_func_mapper['Slot_numbers_for_driver_of_age'](command)
        if 'Leave' in command:
            return self.parking_command_manager_func_mapper['Leave'](command)
        if 'Vehicle_registration_number_for_driver_of_age' in command:
            return self.parking_command_manager_func_mapper['Vehicle_registration_number_for_driver_of_age'](command)
        if 'Slot_number_for_car_with_number' in command:
            return self.parking_command_manager_func_mapper['Slot_number_for_car_with_number'](command)

import sys
inFile = sys.argv[1]
p = ParkingSystem()
with open(inFile,'r') as i:
    lines = i.readlines()
lines = [s[:-1] for s in lines]
for each in lines:
#     print(each)
    output = p.command_manager(str(each))
    if isinstance(output,str) or isinstance(output,int) :
        print(output)
    else:
        print(*output)
#     print('\n\n')