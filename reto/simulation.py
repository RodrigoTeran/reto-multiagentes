import agentpy as ap
from random import sample
from collections import Counter

directions = ["N", "S", "E", "W"]


class TrafficLightAgent(ap.Agent):
    def setup(self):
        self.lights = {"N": "red", "S": "red", "E": "red", "W": "red"}
        self.cooldown = self.model.p.light_cooldown
        self.last_change = self.cooldown

    def step(self):
        votes = self.model.getVotes()
        if self.last_change < self.cooldown or not votes:
            self.last_change += 1
            return
        self.last_change = 0

        for dir in self.lights.keys():
            if dir == votes[0]:
                self.lights[dir] = "green"
            else:
                self.lights[dir] = "red"


class VehicleAgent(ap.Agent):
    def setup(self):
        self.direction = "".join(sample(directions, 2))
        self.crossed = False

    def step(self):
        if (
            not self.crossed
            and self.model.trafficLight.lights[self.direction[0]] == "green"
        ):
            self.crossed = True


class CrossModel(ap.Model):
    def setup(self):
        self.trafficLight = TrafficLightAgent(self)
        self.vehicles = ap.AgentList(self, self.p.vehicles, VehicleAgent)
        self.vehicle_rate = self.p.vehicle_rate
        self.last_car = self.vehicle_rate

    def step(self):
        if self.last_car >= self.vehicle_rate:
            for _ in range(self.p.vehicles):
                self.vehicles.append(VehicleAgent(self))
            self.last_car = 0
        else:
            self.last_car += 1

        self.trafficLight.step()
        self.vehicles.step()

    def getVotes(self):
        votes = []
        for vehicle in self.vehicles:
            if vehicle.crossed:
                continue
            votes.append(vehicle.direction[0])

        vote_counter = Counter(votes)

        return [i[0] for i in vote_counter.most_common(4)]

    def end(self):
        self.record("vehicles", len(self.vehicles))
        self.record("crossed", len([i for i in self.vehicles if i.crossed]))


parameters = {"steps": 200, "vehicles": 15, "light_cooldown": 30, "vehicle_rate": 20}
model = CrossModel(parameters)
model.run()
print(f"Vehicles = {model.log['crossed'][0]}/{model.log['vehicles'][0]}")
