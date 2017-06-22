from CartPole import CartPole
import matplotlib.pyplot as plt
import numpy as np
from Fuzzifier import Fuzzifier


# f = Fuzzifier(1, 2)
#
# x = np.arange(-4, 4, 0.1)
#
# y11 = []
# y22 = []
# y33 = []
# y44 = []
# y55 = []
#
# for x1 in x:
#     y1, y2, y3, y4, y5 = f.calculateFuzzy(x1)
#
#     y11.append(y1)
#     y22.append(y2)
#     y33.append(y3)
#     y44.append(y4)
#     y55.append(y5)
#
# plt.plot(x, y11, label='NH')
# plt.plot(x, y22, label='NL')
# plt.plot(x, y33, label='Z')
# plt.plot(x, y44, label='PL')
# plt.plot(x, y55, label='PH')
# plt.legend()
# plt.show()

fav = Fuzzifier(0.75, 1.5)
fa = Fuzzifier(1.1, 2.2)

# v = 0.0
# c = -1.0

b_velocity = 40 # B
a_velocity = 20 # A

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

    vel = vel_f[0] * (-3*b_velocity) + vel_f[1] * (-a_velocity) +  vel_f[3] * a_velocity + vel_f[4] * (3*b_velocity)

    cp.set_velocity(vel)

    # if cp.get_position() < 500.0:
    #     c = 1
    # elif cp.get_position() > 500.0:
    #     c = -1
    # v = v + c
    # cp.set_velocity(v)


    print ('v =',vel)
    print ('angle =',cp.get_angle())
    print ('angular_velocity =',cp.get_angular_velocity())
    print('pos', cp.get_position())

