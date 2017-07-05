

class Fuzzy():

    def __init__(self, a, b):
        self.a = a
        self.b = b

        self.nh = None
        self.nl = None
        self.z = None
        self.ph = None
        self.pl = None


    def inference(self, obj):

        NH =  max(min(self.nh, obj.z), min(self.z, obj.nh))

        NL = max(min(self.nl, obj.z), min(self.z, obj.nl))

        Z = max(min(self.nl, obj.pl), min(self.z, obj.z), min(self.pl, obj.nl))

        PL = max(min(self.z, obj.pl), min(self.pl, obj.z))

        PH = max(min(self.z, obj.ph), min(self.ph, obj.z))

        return (NH, NL, Z, PL, PH)


    def fuzzifier(self, v):
        # Return 5 values: NH, NL, Z, PL, PH

        if v <= -self.b:
            NH = 1
            NL = 0
            Z = 0
            PL = 0
            PH = 0
        elif v > -self.b and v <= -self.a:
            Z = 0
            PL = 0
            PH = 0
            NH = (v + self.a) / (-self.b+ self.a)
            NL = (v + self.b) / (self.b- self.a)

        elif v > -self.a and v <= 0:
            NH = 0
            PL = 0
            PH = 0
            NL = (v) / (-self.a)
            Z = (v + self.a) / (self.a)

        elif v > 0 and v <= self.a:
            NH = 0
            NL = 0
            PH = 0
            Z = (v - self.a) / (- self.a)
            PL = (v) / (self.a)

        elif v > self.a and v <= self.b:
            NH = 0
            NL = 0
            Z = 0
            PL = (v - self.b) / (self.a - self.b)
            PH = (v - self.a) / (self.b- self.a)

        else: # v > self.b
            NH = 0
            NL = 0
            Z = 0
            PL = 0
            PH = 1

        self.nh = NH
        self.nl = NL
        self.z = Z
        self.ph = PH
        self.pl = PL

