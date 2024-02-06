import agentpy as ap
from random import *
from collections import Counter
from owlready2 import *
import matplotlib.pyplot as plt
import numpy as np

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
    
    # map animation direction to agent direction
    CAR_STREET_TO_DIR = {3: "N", 4: "E", 1: "S", 2: "W"}

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
            
            # Which direction-pair's lights should be considered.
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
        #setup() end $$$$$$$$$
            
        def setup(self, origin):
            # 'N'||'W'||'S'||'E' - direction from which the car arrives
            origin = CAR_STREET_TO_DIR[origin]
            
            #from the valid destinations for the origin one gets selected
            valid_destinations = {"S":["W","N"],"W":["N","E"],"N":["S","E"],"E":["S","W"]}
            destination = choice(valid_destinations[origin])
            
            new_direction = Direction(has_origin=origin,has_destination=destination)
            self.car = Car(current_direction=new_direction, has_crossed=False)
        #setup(origin) end $$$$$$$$$$
            

        def step(self):
            corresponding_light_index = DIR_TO_INDEX[self.car.current_direction.has_origin]
            if (not self.car.has_crossed and self.model.event and 
                self.model.event['traffice_light_colors'][corresponding_light_index]  == "green"):
                self.car.has_crossed = True


    class CrossModel(ap.Model):
        def setup(self):
            self.trafficLight = TrafficLightAgent(self)             #the trafficLight agent which coordinates the car agents
            self.vehicles = ap.AgentList(self, 0, VehicleAgent)     #list of generated car agents
            self.vehicle_rate = self.p.vehicle_rate                 #[int,int,int,int], each origin direction rate of 'arrival' to crossing
            self.new_cars_cooldown = 0                              #steps between car generation
            
            # Used to store events in order to later run simulation in 3D
            self.event = {}
            self.new_event = False
        #setup() end $$$$$$$$$$$$
    
        # Add more cars to simulation
        def step(self):
            #checks steps from last addition, adds when reaches cooldown, cooldown best = 0 so as to add each step to keep population
            if self.new_cars_cooldown >= self.p.new_cars_cooldown:

                # event to generate animation
                self.event['cars_to_add'] = []
                self.new_event = True
                
                # generation is indivial for each origin direction
                for n in range(4):
                    # Amount of new cars is random, takes the origin direction vehicle_rate and multiplies it to vary amount each time
                    for _ in range(randint(1, self.p.vehicles)*self.vehicle_rate[n]):
                        #adds new car with n+1 origin direction(takes 1-4 values, n goes 0-3)
                        new_car = VehicleAgent(self, n+1)
                        self.vehicles.append(new_car)
                        self.event['cars_to_add'].append((DIR_TO_CAR_STREET[new_car.car.current_direction.has_origin], 
                                                        DIR_TO_CAR_STREET[new_car.car.current_direction.has_destination])) #adds each new car to event
                        
            # Resets and increases car generation cooldown counter
                self.new_cars_cooldown = 0
            else:
                self.new_cars_cooldown += 1

            #agents' steps
            self.trafficLight.step()
            self.vehicles.step()
        #step() end $$$$$$$$$$$$

        #gets each vehicle's origin direction
        def getVotes(self):
            votes = [0, 0] # [N + S, E + W], keeps each direction-pair's votes count
            lights_with_cars = set() # {'dir','dir',...}, used to know which lights have vehicles waiting so when no vehicles wait they stay red even if their direction-pair goes green
            for vehicle in self.vehicles:
                if vehicle.car.has_crossed: #vehicles that have crossed dont vote
                    continue
                if vehicle.car.current_direction.has_origin == "N" or vehicle.car.current_direction.has_origin == "S":
                    votes[0] += 1
                else:
                    votes[1] += 1
                
                lights_with_cars.add(vehicle.car.current_direction.has_origin) #compiles populated origin directions
            return votes, lights_with_cars
        #getVotes() end $$$$$$$$$$$$$$$

        def update(self):
            total_vehicles = len(self.vehicles)
            crossed = len([i for i in self.vehicles if i.car.has_crossed])
            self.record("vehicles", total_vehicles)
            self.record("crossed", crossed)
            if total_vehicles:
                self.record("utility", round(crossed/total_vehicles, 2))
            
            # 3D simulation
            if self.new_event:
                self.record("events", self.event)
                self.new_event = False
                self.event = {}
        #update() end $$$$$$$$$$$$$$$$$$

        def end(self):
            print("Finished Simulation!")

    #steps: steps in simulation
    #vehicles: max multiplier on vehicle rate(1-vehicle)
    #vehicle_rate: rate of vehicle generation on each direction
    #cooldown: best at 0, steps until new generations
    parameters = {"steps": 50, "vehicles": 1, "vehicle_rate": [5,1,3,1], "new_cars_cooldown": 0}
    
    model = CrossModel(parameters)
    model.run()
    
    #Extract data from the Model records (the utility):
    utility = model.log['utility']
    time = np.arange(0, len(utility), 1)

    # Plot the data
    plt.plot(time, utility, marker='o', linestyle='-')

    # Add labels and title
    plt.xlabel('Time (steps)')
    plt.title('Utility (Total Vehicules/Crossed)')

    # Show the plot
    plt.show()    
    
    print(f"Vehicles = {model.log['crossed'][-1]}/{model.log['vehicles'][-1]}")
    output = [event for event in model.log['events'] if event is not None]
    #print('\n\n'.join(map(str, output)))
    return output

if __name__ == '__main__':
    runModel()