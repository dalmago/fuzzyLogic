from CartPole import CartPole
from Fuzzifier import Fuzzifier


fav = Fuzzifier(1, 3.5)
fa = Fuzzifier(0.08, 1.5)

# v = 0.0
# c = -1.0

b_velocity = 900 # B
a_velocity = 400 # A

cp = CartPole()
cp.set_velocity(-1)

while cp.running:
    cp.step(1.0/60.0)
    cp.events()

    ang_vel = cp.get_angular_velocity()
    angle = cp.get_angle()

    fav.calculateFuzzy(ang_vel)
    fa.calculateFuzzy(angle)

    vel_f = fav.combineFuzzy(fa)

    vel = vel_f[0] * (-b_velocity) + vel_f[1] * (-a_velocity) +  vel_f[3] * a_velocity + vel_f[4] * (b_velocity)

    cp.set_velocity(-vel)


    print ('v =',vel)
    print ('angle =',cp.get_angle())
    print ('angular_velocity =',cp.get_angular_velocity())
    #print('pos', cp.get_position())
    print("vel fuzzy:", vel_f)
    print("--------")

