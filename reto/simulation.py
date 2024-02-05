import agentpy as ap
from random import sample
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
            self.cooldown = self.model.p.light_cooldown
            self.last_change = self.cooldown
            # Intantiate 4 ontology instances of class TrafficLight to
            # represent the 4 traffic lights in the simulation.
            # indexes: facing north, east, south, west
            self.lights = [TrafficLight(current_color=[Color(has_color="red")]), 
                        TrafficLight(current_color=[Color(has_color="red")]), 
                        TrafficLight(current_color=[Color(has_color="red")]), 
                        TrafficLight(current_color=[Color(has_color="red")])] 
                
            
        def step(self):
            votes = self.model.getVotes()
            if self.last_change < self.cooldown or not votes:
                self.last_change += 1
                return
            self.last_change = 0

            # Change traffic lights colors depending on the most voted
            self.model.event['traffice_light_colors'] = ['red', 'red', 'red', 'red']
            self.model.new_event = True
            for dir in DIR_TO_INDEX.keys():
                if dir == votes[0]:
                    self.lights[DIR_TO_INDEX[dir]].current_color[0].has_color = "green"
                    self.model.event['traffice_light_colors'][DIR_TO_INDEX[dir]] = "green" # Used to later display simulation  in 3d
                else:
                    self.lights[DIR_TO_INDEX[dir]].current_color[0].has_color = "red"

    class VehicleAgent(ap.Agent):
        def setup(self):
            directions = sample(DIR_TO_INDEX.keys(), 2)
            new_direction = Direction(has_origin=directions[0],has_destination=directions[1])
            
            self.car = Car(current_direction=new_direction, has_crossed=False)

        def step(self):
            corresponding_light_index = DIR_TO_INDEX[self.car.current_direction.has_origin]
            if (not self.car.has_crossed and 
                self.model.trafficLight.lights[corresponding_light_index].current_color[0].has_color == "green"):
                self.car.has_crossed = True


    class CrossModel(ap.Model):
        def setup(self):
            self.trafficLight = TrafficLightAgent(self)
            self.vehicles = ap.AgentList(self, self.p.vehicles, VehicleAgent)
            self.vehicle_rate = self.p.vehicle_rate
            self.last_car = self.vehicle_rate
            # Used to store events in order to later run simulation in 3D
            self.event = {}
            self.new_event = False

        def step(self):
            # Add more cars to simulation
            if self.last_car >= self.vehicle_rate:
                self.event['cars_to_add'] = []
                self.new_event = True
                for _ in range(self.p.vehicles//3):
                    new_car = VehicleAgent(self)
                    self.vehicles.append(new_car)
                    self.event['cars_to_add'].append((DIR_TO_CAR_STREET[new_car.car.current_direction.has_origin], 
                                                      DIR_TO_CAR_STREET[new_car.car.current_direction.has_destination]))
                self.last_car = 0
            else:
                self.last_car += 1

            self.trafficLight.step()
            self.vehicles.step()

        def getVotes(self):
            votes = []
            for vehicle in self.vehicles:
                if vehicle.car.has_crossed:
                    continue
                votes.append(vehicle.car.current_direction.has_origin)

            vote_counter = Counter(votes)

            return [i[0] for i in vote_counter.most_common(4)]

        def update(self):
            self.record("vehicles", len(self.vehicles))
            self.record("crossed", len([i for i in self.vehicles if i.car.has_crossed]))
            
            # 3D simulation
            if self.new_event:
                self.record("events", self.event)
                print('\n\n')
                print(self.event)
                self.new_event = False
                self.event = {}

        def end(self):
            print("Finished Simultion!")

    parameters = {"steps": 100, "vehicles": 10, "light_cooldown": 30, "vehicle_rate": 15}
    model = CrossModel(parameters)
    model.run()
    print(f"Vehicles = {model.log['crossed'][-1]}/{model.log['vehicles'][-1]}")
    output = [event for event in model.log['events'] if event is not None]
    print('\n\n'.join(map(str, output)))
    return output

if __name__ == '__main__':
    runModel()