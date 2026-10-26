import unittest

from seafloor import generate_frames, analyze_frames


class SeafloorTests(unittest.TestCase):
    def test_stable_frames_show_no_change(self):
        original, later = generate_frames("Stable seabed")
        finding, _ = analyze_frames(original, later)
        self.assertEqual(finding.changed_pixels, 0)
        self.assertIsNone(finding.bounding_box)

    def test_displacement_detected(self):
        before, after = generate_frames("Sediment displacement")
        finding, _ = analyze_frames(before, after)
        self.assertGreater(finding.changed_percent, 0.1)
        self.assertIsNotNone(finding.bounding_box)
        self.assertLess(finding.changed_percent, 15)

    def test_receding_cover_detected(self):
        before, after = generate_frames("Sediment recedes near cable")
        finding, _ = analyze_frames(before, after)
        self.assertGreater(finding.changed_pixels, 0)

    def test_unknown_scenario_rejected(self):
        with self.assertRaises(ValueError):
            generate_frames("Moonbase")


if __name__ == "__main__":
    unittest.main()
