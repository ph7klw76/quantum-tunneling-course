import unittest
import numpy as np
from course.physics import *

class BarrierTests(unittest.TestCase):
    def test_default_independent_ode(self):
        self.assertAlmostEqual(transmission(),numerical_transmission(),places=10)
    def test_parameter_grid_unitarity_and_closed_form(self):
        for V in [.2,1.,3.]:
            for fraction in [.01,.2,.5,.9,.9999]:
                for a in [0,.05,.45,1.5]:
                    E = V*fraction
                    r,A,B,t = amplitudes(E,V,a)
                    self.assertAlmostEqual(abs(t)**2+abs(r)**2,1.,places=11)
                    self.assertAlmostEqual(abs(t)**2,transmission(E,V,a),places=11)
    def test_boundary_continuity(self):
        E,V,a = .5,1.,.45
        r,A,B,t = amplitudes(E,V,a); k,q = np.sqrt(E/C),np.sqrt((V-E)/C)
        d = np.exp(-q*a)
        np.testing.assert_allclose([1+r,1j*k*(1-r),A*d+B,q*(-A*d+B)],
                                   [A+B*d,q*(-A+B*d),t,1j*k*t],atol=1e-13)
    def test_current_is_constant_not_density(self):
        x=np.linspace(-1,1.4,301); p,d=wavefunction(x)
        np.testing.assert_allclose(np.imag(p.conj()*d),np.sqrt(.5/C)*transmission(),atol=1e-12)
    def test_numerical_grid(self):
        for E,V,a in [(.1,1,.2),(.8,1,.5),(.4,2,.6)]:
            self.assertAlmostEqual(transmission(E,V,a),numerical_transmission(E,V,a),places=9)
    def test_limits_and_units(self):
        self.assertAlmostEqual(C,.0380998211,places=9)
        self.assertEqual(transmission(a=0),1)
        self.assertEqual(transmission(a=1000),0)
        self.assertGreater(transmission(a=.2),transmission(a=.8))
        self.assertGreater(transmission(E=.8),transmission(E=.2))
    def test_domain(self):
        for args in [(0,1,.4),(1,1,.4),(.5,1,-.2),(.5,np.nan,.4)]:
            with self.assertRaises(ValueError): transmission(*args)

if __name__=='__main__': unittest.main()
