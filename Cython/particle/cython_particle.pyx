


cdef class Particle:
    """
    Hei hei
    """
    cdef public double mass
    cdef readonly double position
    cdef double velocity

    def __init__(self,m,p,v):
        """
        Test Init
        :param m: m1
        :param p: p1
        :param v: v1
        """
        self.mass = m
        self.position = p
        self.velocity = v

