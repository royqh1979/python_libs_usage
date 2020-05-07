import simpy

def driver(env,action):
    yield env.timeout(3)
    action.interrupt()

def charge(env:simpy.Environment,duration):
    yield env.timeout(duration)

def car(env:simpy.Environment):
    while True:
        print(f'{env.now} 开始停车充电')
        charge_duration = 5
        try:
            yield env.process(charge(env,charge_duration))
        except simpy.Interrupt:
            print("被中断了。希望电池有电。。。")

        print(f"{env.now} 开始行驶")
        trip_duration = 2
        yield env.timeout(trip_duration)

env = simpy.Environment()
action=env.process(car(env))
env.process(driver(env,action))
env.run(until=15)