import agentpy as ap
from random import *
from collections import Counter
from owlready2 import *

def runModel():
    # Ontology using Owlready2
    onto = get_ontology("file:///content/cars_onto.owl")

    #opening the ontology
    with onto:

        #My SuperClass
        class Agent(Thing):
            pass

        class TrafficLight(Agent):
            pass

        class Car(Agent):
            pass

        class Direction(Thing):
            pass

        class Color(Thing):
            pass
        
        class has_color(DataProperty, FunctionalProperty):
            domain = [Color]
            range = [str]

        class current_color(ObjectProperty):
            domain = [TrafficLight]
            range = [Color]
        
        class has_origin(DataProperty, FunctionalProperty):
            domain = [Direction]
            range = [str]

        class has_destination(DataProperty, FunctionalProperty):
            domain = [Direction]
            range = [str]
        
        class current_direction(ObjectProperty, FunctionalProperty):
            domain = [Car]
            range = [Color] 
        
        class has_crossed(DataProperty, FunctionalProperty):
            domain = [Car]
            range = [bool] 

    # Map direction to its traffic light index
    DIR_TO_INDEX = {"N": 0, "E": 1, "S": 2, "W": 3}
    
    # Map direction to the cars internal directions for 3D
    DIR_TO_CAR_STREET = {"N": 3, "E": 4, "S": 1, "W": 2}

    class TrafficLightAgent(ap.Agent):
        def setup(self):
            # Intantiate 4 ontology instances of class TrafficLight to
            # represent the 4 traffic lights in the simulation.
            # indexes: facing north, east, south, west
            self.lights = [TrafficLight(current_color=[Color(has_color="red")]), 
                        TrafficLight(current_color=[Color(has_color="red")]), 
                        TrafficLight(current_color=[Color(has_color="red")]), 
                        TrafficLight(current_color=[Color(has_color="red")])] 
                
            
        def step(self):
            votes, lights_with_cars = self.model.getVotes()
            if not lights_with_cars:
                return

            # Change traffic lights colors depending on the most voted
            self.model.event['traffice_light_colors'] = ['red', 'red', 'red', 'red']
            self.model.new_event = True
            
            # Which 2 lights should be considered.
            if votes[0] > votes[1]:
                potential_lights = ["N", "S"]
            else:
                potential_lights = ["E", "W"]
            
            for dir in potential_lights:
                index = DIR_TO_INDEX[dir]
                if dir not in lights_with_cars: #No car voted for this option.
                    self.lights[index].current_color[0].has_color = "red"
                    continue
                # First choose the most voted traffic light to go green.
                self.lights[index].current_color[0].has_color = "green"
                self.model.event['traffice_light_colors'][index] = "green" # Used to later display simulation  in 3d
            

    class VehicleAgent(ap.Agent):
        def setup(self):
            # This includes left turn.
            # directions = sample(DIR_TO_INDEX.keys(), 2) 
            
            # Choose origin and destination excluding left turns
            origin = choice(list(DIR_TO_CAR_STREET.keys()))
            valid_destinations = {"S":["W","N"],"W":["N","E"],"N":["S","E"],"E":["S","W"]}
            destination = choice(valid_destinations[origin])
            
            
            new_direction = Direction(has_origin=origin,has_destination=destination)
            self.car = Car(current_direction=new_direction, has_crossed=False)

        def step(self):
            corresponding_light_index = DIR_TO_INDEX[self.car.current_direction.has_origin]
            if (not self.car.has_crossed and self.model.event and 
                self.model.event['traffice_light_colors'][corresponding_light_index]  == "green"):
                self.car.has_crossed = True


    class CrossModel(ap.Model):
        def setup(self):
            self.trafficLight = TrafficLightAgent(self)
            self.vehicles = ap.AgentList(self, 0, VehicleAgent)
            self.vehicle_rate = self.p.vehicle_rate
            self.new_cars_cooldown = self.vehicle_rate
            # Used to store events in order to later run simulation in 3D
            self.event = {}
            self.new_event = False
    
        def step(self):
            # Add more cars to simulation
            if self.new_cars_cooldown >= self.vehicle_rate:
                self.event['cars_to_add'] = []
                self.new_event = True
                for _ in range(randint(3, self.p.vehicles)): # Amount of new cars is random
                    new_car = VehicleAgent(self)
                    self.vehicles.append(new_car)
                    self.event['cars_to_add'].append((DIR_TO_CAR_STREET[new_car.car.current_direction.has_origin], 
                                                      DIR_TO_CAR_STREET[new_car.car.current_direction.has_destination]))
                # Make car cooldown random
                self.new_cars_cooldown = randint(0, self.vehicle_rate)
            else:
                self.new_cars_cooldown += 1

            self.trafficLight.step()
            self.vehicles.step()

        def getVotes(self):
            votes = [0, 0] # N + S, E + W
            lights_with_cars = set()
            for vehicle in self.vehicles:
                if vehicle.car.has_crossed:
                    continue
                if vehicle.car.current_direction.has_origin == "N" or vehicle.car.current_direction.has_origin == "S":
                    votes[0] += 1
                else:
                    votes[1] += 1
                    
                # used to know if there are cars in both directions to know if both lights should turn green.
                lights_with_cars.add(vehicle.car.current_direction.has_origin)
            return votes, lights_with_cars

        def update(self):
            self.record("vehicles", len(self.vehicles))
            self.record("crossed", len([i for i in self.vehicles if i.car.has_crossed]))
            
            # 3D simulation
            if self.new_event:
                self.record("events", self.event)
                self.new_event = False
                self.event = {}

        def end(self):
            print("Finished Simultion!")

    parameters = {"steps": 150, "vehicles": 12, "vehicle_rate": 5}
    model = CrossModel(parameters)
    model.run()
    print(f"Vehicles = {model.log['crossed'][-1]}/{model.log['vehicles'][-1]}")
    output = [event for event in model.log['events'] if event is not None]
    print('\n\n'.join(map(str, output)))
    return output

if __name__ == '__main__':
    runModel()