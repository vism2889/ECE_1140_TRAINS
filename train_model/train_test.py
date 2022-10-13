from train import Train
import time


t = Train(5, 'blue')

start_time = time.time()

t.dispatch()
print(t.curr_power)
count = 0
while True:
    # if time.time() - start_time > 1:
    p = 120000
    print('setting power')
    t.set_power(p)

    elapsed_time = time.time()-start_time
    km_h = (t.curr_vel * 3600)/1000
    print(f'At time: {elapsed_time}')
    print(f'current force: {t.curr_force}')
    print(f'current power: {t.curr_power}')
    print(f'current velocity: {km_h}')
    print(f'current acceleration: {t.curr_accel}')
    print(f'current position: {t.curr_pos}\n\n')

    count += 2
    if time.time()-start_time > 300:
        break


