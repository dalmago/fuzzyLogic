from CartPole import CartPole

v = 0.0
c = -1.0

cp = CartPole()
while cp.running:
    cp.step(1.0/60.0)
    cp.events()
    if cp.get_position() < 500.0:
        c = 1
    elif cp.get_position() > 500.0:
        c = -1
    v = v + c
    cp.set_velocity(v)
    print 'v =',v
    print 'angle =',cp.get_angle()
    print 'angular_velocity =',cp.get_angular_velocity()

