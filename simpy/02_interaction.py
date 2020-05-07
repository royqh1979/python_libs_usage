import simpy

def charge(env:simpy.Environment,duration):
    yield env.timeout(duration)

def car(env:simpy.Environment):
    while True:
        print(f'{env.now} 开始停车充电')
        charge_duration = 5
        yield env.process(charge(env,charge_duration))

        print(f"{env.now} 开始行驶")
        trip_duration = 2
        yield env.timeout(trip_duration)

env = simpy.Environment()
env.process(car(env))
env.run(until=15)
# class Car:
    # def __init__(self,env:simpy.Environment):
    #     self.env = env
    #     self.action = None
    #
    # def start(self):
    #     if self.action is not None:
    #         raise ValueError("Already started!")
    #     self.action = self.env.process(self.run())
    #
    # def charge(self,duration):
    #
    #
    # def run(self):
    #     while True:
    #         print(f'{self.env.now} 开始停车充电')
    #         charge_duration = 5
    #         yield