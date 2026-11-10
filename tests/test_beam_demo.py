import unittest

from beam_demo import Beam


class BeamTests(unittest.TestCase):
    def setUp(self):
        self.beam = Beam(length_m=2.0, force_n=300.0, young_pa=200e9, inertia_m4=2e-6)

    def test_fixed_end_response_is_zero_except_root_moment(self):
        v, theta, moment = self.beam.response(0.0)
        self.assertEqual(v, 0.0)
        self.assertEqual(theta, 0.0)
        self.assertEqual(moment, 600.0)

    def test_tip_matches_closed_form_deflection_slope_and_zero_moment(self):
        v, theta, moment = self.beam.response(2.0)
        ei = 200e9 * 2e-6
        self.assertAlmostEqual(v, 300.0 * 2.0**3 / (3.0 * ei))
        self.assertAlmostEqual(theta, 300.0 * 2.0**2 / (2.0 * ei))
        self.assertAlmostEqual(moment, 0.0)

    def test_rejects_invalid_position_and_nonpositive_parameters(self):
        with self.assertRaises(ValueError):
            self.beam.response(2.1)
        with self.assertRaises(ValueError):
            Beam(length_m=0, force_n=1, young_pa=1, inertia_m4=1)


if __name__ == "__main__":
    unittest.main()

