import simpy

def car(env:simpy.Environment):
    while True:
        print(f"{env.now}开始停车")
        parking_duration = 5
        yield env.timeout(parking_duration)

        print(f"{env.now}开始开车")
        trip_duration = 2
        yield env.timeout(trip_duration)

env = simpy.Environment()
env.process(car(env))
env.run(until=30)