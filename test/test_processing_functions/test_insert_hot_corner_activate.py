import unittest
from src.post_processing.processing_functions import insert_hot_corner_activate


class TestInsertHotCornerActivate(unittest.TestCase):
    def test_activate_hot_corner(self):
        events = [
            ("move", 0, 0, 0.01),
            ("move", 10, 10, 0.02),
            ("move", 0, 0, 0.03),
            ("move", 0, 0, 0.04)
        ]
        expected = [
            ("move", 0, 0, 0.01),
            ("key_press", "Key.cmd", 0.0005),
            ("key_release", "Key.cmd", 0.0005),
            ("move", 10, 10, 0.019),
            ("move", 0, 0, 0.03),
            ("key_press", "Key.cmd", 0.0005),
            ("key_release", "Key.cmd", 0.0005),
            ("move", 0, 0, 0.039)
        ]
        result = insert_hot_corner_activate(events)
        self.assertEqual(result, expected)

    def test_no_activation_if_not_at_0_0(self):
        events = [
            ("move", 10, 10, 0.01),
            ("move", 20, 20, 0.02)
        ]
        expected = [
            ("move", 10, 10, 0.01),
            ("move", 20, 20, 0.02)
        ]
        result = insert_hot_corner_activate(events)
        self.assertEqual(result, expected)

    def test_only_once_activate_hot_corner(self):
        events = [
            ("move", 0, 0, 0.01),
            ("move", 0, 0, 0.02)
        ]
        expected = [
            ("move", 0, 0, 0.01),
            ("key_press", "Key.cmd", 0.0005),
            ("key_release", "Key.cmd", 0.0005),
            ("move", 0, 0, 0.019)
        ]
        result = insert_hot_corner_activate(events)
        self.assertEqual(result, expected)

    def test_mixed_events(self):
        events = [
            ("move", 0, 0, 0.01),
            ("click", "left", 0.01),
            ("move", 0, 0, 0.02),
            ("move", 0, 0, 0.03)
        ]
        expected = [
            ("move", 0, 0, 0.01),
            ("key_press", "Key.cmd", 0.0005),
            ("key_release", "Key.cmd", 0.0005),
            ("click", "left", 0.009),
            ("move", 0, 0, 0.02),
            ("key_press", "Key.cmd", 0.0005),
            ("key_release", "Key.cmd", 0.0005),
            ("move", 0, 0, 0.029)
        ]
        result = insert_hot_corner_activate(events)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
