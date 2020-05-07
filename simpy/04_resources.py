import simpy


def car(env,name,bcs:simpy.Resource,driving_time,charge_duration):
    # simulate driving to the BCS
    yield env.timeout(driving_time)
    print('%s arriving at %d' % (name, env.now))

    #Request one of its charging spots
    with bcs.request() as req:
        yield req

        # charge the battery
        print('%s starting to charge at %s' % (name, env.now))
        yield env.timeout(charge_duration)
        print('%s leaving the bcs at %s' % (name, env.now))


env = simpy.Environment()
# battery charge station
bcs = simpy.Resource(env,capacity=2)
for i in range(4):
    env.process(car(env,f"Car {i}", bcs, i*2 ,5))

env.run(until=30)