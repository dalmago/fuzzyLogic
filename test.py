from CartPole import CartPole
from Fuzzy import Fuzzy


fav = Fuzzy(1, 3.5)
fa = Fuzzy(0.08, 1.5)

b_velocity = 900 # B
a_velocity = 400 # A

cp = CartPole()
cp.set_velocity(-1)

while cp.running:
    cp.step(1.0/60.0)
    cp.events()

    ang_vel = cp.get_angular_velocity()
    angle = cp.get_angle()

    fav.fuzzifier(ang_vel)
    fa.fuzzifier(angle)

    vel_f = fav.inference(fa)

    # defuzzifier
    vel = vel_f[0] * (-b_velocity) + vel_f[1] * (-a_velocity) +  vel_f[3] * a_velocity + vel_f[4] * (b_velocity)

    cp.set_velocity(-vel)


    print ('v =', -vel)
    print("vel fuzzy:", vel_f)
    print ('angle =',cp.get_angle())
    print ('angular_velocity =',cp.get_angular_velocity())
    #print('pos', cp.get_position())
    print("--------")

