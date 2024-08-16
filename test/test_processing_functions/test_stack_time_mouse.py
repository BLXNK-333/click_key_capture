import unittest
from src.post_processing.processing_functions import stack_time_mouse


class TestStackTimeMouse(unittest.TestCase):

    def test_empty_input(self):
        self.assertEqual(stack_time_mouse([]), [])

    def test_single_move_event(self):
        events = [("move", 100, 200, 0.5)]
        expected = [("move", 100, 200, 0.5)]
        self.assertEqual(stack_time_mouse(events), expected)

    def test_multiple_move_events_same_position(self):
        events = [
            ("move", 100, 200, 0.2),
            ("move", 100, 200, 0.3),
        ]
        expected = [("move", 100, 200, 0.5)]
        self.assertEqual(stack_time_mouse(events), expected)

    def test_multiple_move_events_different_positions(self):
        events = [
            ("move", 100, 200, 0.2),
            ("move", 150, 250, 0.3),
        ]
        expected = [
            ("move", 100, 200, 0.2),
            ("move", 150, 250, 0.3),
        ]
        self.assertEqual(stack_time_mouse(events), expected)

    def test_non_move_event_included(self):
        events = [
            ("move", 100, 200, 0.2),
            ("click", 150, 250, 0.0),
        ]
        expected = [
            ("move", 100, 200, 0.2),
            ("click", 150, 250, 0.0),
        ]
        self.assertEqual(stack_time_mouse(events), expected)

    def test_mixed_events(self):
        events = [
            ("move", 100, 200, 0.2),
            ("move", 100, 200, 0.3),
            ("click", 150, 250, 0.0),
            ("move", 150, 250, 0.1),
        ]
        expected = [
            ("move", 100, 200, 0.5),
            ("click", 150, 250, 0.0),
            ("move", 150, 250, 0.1),
        ]
        self.assertEqual(stack_time_mouse(events), expected)

    def test_non_move(self):
        events = [
            ("key_press", "Key.cmd", 0.001),
            ("key_release", "Key.cmd", 0.001),
            ("scroll", 100, 100, 0, -1, 0.02)
        ]
        expected = [
            ("key_press", "Key.cmd", 0.001),
            ("key_release", "Key.cmd", 0.001),
            ("scroll", 100, 100, 0, -1, 0.02)
        ]
        self.assertEqual(stack_time_mouse(events), expected)


if __name__ == '__main__':
    unittest.main()
