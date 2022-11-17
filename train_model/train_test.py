from train import Train
import time


t = Train()

# t.launch_ui()

val = 2

# t.launch_ui()

start_time = time.time()

t.dispatch()
time.sleep(val)
count = 0
while True:
    # if time.time() - start_time > 1:
    p = 120000
    print('setting power')
    t.set_power(p)
    time.sleep(val)

    # print(f'At time: {elapsed_time}')
    # print(f'current force: {t.curr_force}')
    # print(f'current power: {t.curr_power}')
    # print(f'current velocity: {km_h}')
    # print(f'current acceleration: {t.curr_accel}')
    # print(f'current position: {t.curr_pos}\n\n')

    count += 2
    if time.time()-start_time > 15:
        print("Turning on service brake")
        t.service_brake = True
        t.set_power(120000)
        int_time = time.time()

        while True:
            time.sleep(0.5)
            if t.pm.curr_vel >0:
                t.pm.serv_brake()
        # while True:

        #     if time.time() - int_time > 1:
        #         print(f'Current speed of train is: {t.pm.curr_speed}')
            
        #     if t.pm.curr_speed <= 0:
        #         break

        break


