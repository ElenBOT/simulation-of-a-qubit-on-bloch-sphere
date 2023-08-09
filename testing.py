import blochsimu as bs

dt = 5e-4 # sampling time for numerical integral

# d  / x \   / -G2  -d   I\ / x \   /   0   \ 
#----| y | = |  d  -G2  -Q| | y | + |   0   |
# dt \ z /   \ -I   Q  -G1/ \ z /   \ G1*z0 /
# default physical arguments:
phy_args = {
    'u0': (0.0, 0.0, 1.0),
    'z0': 1.0,
    'I' : 0,
    'Q' : 0,
    'd' : 0,
    'G1': 0,
    'G2': 0,
}
# G is short for Gamma. 
# G1: relaxation
# G2: decoherence
# Gp: dephaseing
Gp = 0.5
G1 = 0.5
G2 = Gp + G1/2
# Note : I = 1.58 for 1s to achieve pi/2-pluse,
#        I = 1.58 for 2s to achieve pi-pluse
expe = bs.ExpScheme(**phy_args)
expe.sequence = (
    bs.Section(s=1, I=1.58), # pi pluse of I
    bs.Section(s=3, d=0, G1=G1, G2=G2) # wait for qubit drops back to ground state.
)
u_sol, u_sol_section = bs.blochsolve(expe, dt)
bs.blochdrawer.plot(u_sol, block=True)