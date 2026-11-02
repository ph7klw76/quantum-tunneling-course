"""Lossless equal-lead rectangular barrier; energies eV, positions nm.

Scattering states have unit incident amplitude, not unit integrated probability.
The API deliberately restricts energies to 0 < E < V0.
"""
import numpy as np

HBAR = 1.054571817e-34  # J s (CODATA rounded)
EV = 1.602176634e-19   # J / eV, exact
M_E = 9.1093837139e-31 # kg, CODATA 2022
NM = 1e-9
C = HBAR**2 / (2 * M_E * EV * NM**2)  # eV nm^2

def validate(E, V0, a):
    if not all(np.isfinite(v) for v in (E, V0, a)):
        raise ValueError('Parameters must be finite.')
    if not 0 < E < V0 or a < 0:
        raise ValueError('Require 0 < E < V0 and a >= 0 nm.')

def transmission(E=0.5, V0=1., a=0.45):
    """Exact transmission, evaluated in log space to avoid thick-barrier overflow."""
    validate(E, V0, a)
    if a == 0:
        return 1.
    z = np.sqrt((V0-E)/C)*a
    log_sinh = z + np.log(-np.expm1(-2*z)) - np.log(2.)
    log_term = 2*np.log(V0) + 2*log_sinh - np.log(4*E*(V0-E))
    return float(np.exp(-np.logaddexp(0., log_term)))

def amplitudes(E=0.5, V0=1., a=0.45):
    """Solve four continuity equations. Returns r, A, B, t.

    psi_left = exp(ikx) + r exp(-ikx)
    psi_inside = A exp(-kappa x) + B exp(kappa (x-a))
    psi_right = t exp(ik(x-a)). Both internal basis functions stay bounded.
    """
    validate(E, V0, a)
    k, q = np.sqrt(E/C), np.sqrt((V0-E)/C)
    d = np.exp(-q*a)
    matrix = np.array([[1,-1,-d,0],[-1j*k,q,-q*d,0],
                       [0,d,1,-1],[0,-q*d,q,-1j*k]], dtype=complex)
    rhs = np.array([-1,-1j*k,0,0], dtype=complex)
    return np.linalg.solve(matrix, rhs)

def wavefunction(x, E=0.5, V0=1., a=0.45):
    """psi and spatial derivative, x in nm; derivative per nm."""
    x = np.asarray(x, dtype=float)
    r,A,B,t = amplitudes(E,V0,a)
    k,q = np.sqrt(E/C),np.sqrt((V0-E)/C)
    p,d = np.empty(x.shape,complex),np.empty(x.shape,complex)
    left,inside,right = x<0,(x>=0)&(x<=a),x>a
    u,v = np.exp(1j*k*x[left]),r*np.exp(-1j*k*x[left])
    p[left],d[left] = u+v,1j*k*(u-v)
    u,v = A*np.exp(-q*x[inside]),B*np.exp(q*(x[inside]-a))
    p[inside],d[inside] = u+v,q*(-u+v)
    p[right] = t*np.exp(1j*k*(x[right]-a)); d[right] = 1j*k*p[right]
    return p,d

def numerical_transmission(E=.5,V0=1.,a=.45,rtol=1e-10):
    """Independent ODE integration backwards from a right-going exit state.

    For very opaque barriers cancellation limits accuracy; use modest widths
    for this pedagogical cross-check, not as an all-regime production solver.
    """
    from scipy.integrate import solve_ivp
    validate(E,V0,a)
    if a == 0: return 1.
    k = np.sqrt(E/C)
    sol = solve_ivp(lambda x,y:[y[1],(V0-E)/C*y[0]], (a,0),
                    np.array([1,1j*k]),rtol=rtol,atol=rtol*0.01)
    if not sol.success: raise RuntimeError(sol.message)
    p,d = sol.y[:,-1]
    incoming = (p+d/(1j*k))/2
    return float(1/abs(incoming)**2)
