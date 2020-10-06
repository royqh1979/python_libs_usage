# The Computer Language Benchmarks Game
# http://benchmarksgame.alioth.debian.org/
#
# originally by Kevin Carson
# modified by Tupteq, Fredrik Johansson, and Daniel Nanz
# modified by Maciej Fijalkowski
# 2to3

from libc.math cimport sqrt

cdef struct body_t:
    double x[3] # position
    double v[3] # velocity
    double m #mass

cdef inline void make_cbodies(list bodies, body_t *cbodies, int num_cbodies):
    cdef body_t *cbody
    cdef int i,n
    n = len(bodies)
    for i in range(n):
        if i>=num_cbodies:
            break
        (x,v,m) = bodies[i]
        cbody = &cbodies[i]
        cbody.x[0],cbody.x[1],cbody.x[2] = x
        cbody.v[0],cbody.v[1],cbody.v[2]=v
        cbody.m = m

cdef inline list make_pybodies(body_t *cbodies, int num_cbodies):
    cdef list pybodies = []
    cdef int i
    for i in range(num_cbodies):
        x = [cbodies[i].x[0],cbodies[i].x[1],cbodies[i].x[2]]
        v = [cbodies[i].v[0],cbodies[i].v[1],cbodies[i].v[2]]
        pybodies.append((x,v,cbodies[i].m))
    return pybodies

def combinations(l):
    result = []
    for x in range(len(l) - 1):
        ls = l[x+1:]
        for y in ls:
            result.append((l[x],y))
    return result

PI = 3.14159265358979323
SOLAR_MASS = 4 * PI * PI
DAYS_PER_YEAR = 365.24
DEF NBODYIES = 5
BODIES = {
        'sun': ([0.0, 0.0, 0.0], [0.0, 0.0, 0.0], SOLAR_MASS),

        'jupiter': ([4.84143144246472090e+00,
            -1.16032004402742839e+00,
            -1.03622044471123109e-01],
            [1.66007664274403694e-03 * DAYS_PER_YEAR,
                7.69901118419740425e-03 * DAYS_PER_YEAR,
                -6.90460016972063023e-05 * DAYS_PER_YEAR],
            9.54791938424326609e-04 * SOLAR_MASS),

        'saturn': ([8.34336671824457987e+00,
            4.12479856412430479e+00,
            -4.03523417114321381e-01],
            [-2.76742510726862411e-03 * DAYS_PER_YEAR,
                4.99852801234917238e-03 * DAYS_PER_YEAR,
                2.30417297573763929e-05 * DAYS_PER_YEAR],
            2.85885980666130812e-04 * SOLAR_MASS),

        'uranus': ([1.28943695621391310e+01,
            -1.51111514016986312e+01,
            -2.23307578892655734e-01],
            [2.96460137564761618e-03 * DAYS_PER_YEAR,
                2.37847173959480950e-03 * DAYS_PER_YEAR,
                -2.96589568540237556e-05 * DAYS_PER_YEAR],
            4.36624404335156298e-05 * SOLAR_MASS),

        'neptune': ([1.53796971148509165e+01,
            -2.59193146099879641e+01,
            1.79258772950371181e-01],
            [2.68067772490389322e-03 * DAYS_PER_YEAR,
                1.62824170038242295e-03 * DAYS_PER_YEAR,
                -9.51592254519715870e-05 * DAYS_PER_YEAR],
            5.15138902046611451e-05 * SOLAR_MASS) 
        }

def advance(double dt,int n, list bodies):
    cdef int i,ii,jj
    cdef dx,dy,dz,mag,b1m,b2m,ds
    cdef body_t *body1
    cdef body_t *body2
    cdef body_t cbodies[NBODYIES]

    make_cbodies(bodies,cbodies,NBODYIES)
    for i in range(n):
        for ii in range(NBODYIES-1):
            body1 = &cbodies[ii]
            for jj in range(ii+1,NBODYIES):
                body2 = &cbodies[jj]
                dx = body1.x[0] - body2.x[0]
                dy = body1.x[1] - body2.x[1]
                dz = body1.x[2] - body2.x[2]
                ds = dx * dx + dy * dy + dz * dz
                mag = dt / (ds*sqrt(ds))
                b1m = body1.m * mag
                b2m = body2.m * mag
                body1.v[0] -= dx * b2m
                body1.v[1] -= dy * b2m
                body1.v[2] -= dz * b2m
                body2.v[0] += dx * b1m
                body2.v[1] += dy * b1m
                body2.v[2] += dz * b1m
        for ii in range(NBODYIES):
            body1 = &cbodies[ii]
            body1.x[0] += dt * body1.v[0]
            body1.x[1] += dt * body1.v[1]
            body1.x[2] += dt * body1.v[2]
    return make_pybodies(cbodies,NBODYIES)


def report_energy(bodies, pairs):

    cdef double e = 0.0

    for (((x1, y1, z1), v1, m1),
            ((x2, y2, z2), v2, m2)) in pairs:
        dx = x1 - x2
        dy = y1 - y2
        dz = z1 - z2
        e -= (m1 * m2) / ((dx * dx + dy * dy + dz * dz) ** 0.5)
    for (r, [vx, vy, vz], m) in bodies:
        e += m * (vx * vx + vy * vy + vz * vz) / 2.
    print("%.9f" % e)

def offset_momentum(ref, bodies):

    px = py = pz = 0.0

    for (r, [vx, vy, vz], m) in bodies:
        px -= vx * m
        py -= vy * m
        pz -= vz * m
    (r, v, m) = ref
    v[0] = px / m
    v[1] = py / m
    v[2] = pz / m

def main(n, bodies=BODIES, ref='sun'):
    system = list(bodies.values())
    pairs = combinations(system)
    offset_momentum(bodies[ref], system)
    report_energy(system, pairs)
    advance(0.01, n, system)
    report_energy(system, pairs)

# if __name__ == '__main__':
#     main(int(sys.argv[1]), bodies=BODIES, ref='sun')

def test_cython():
    main(500000, bodies=BODIES, ref='sun')

