import unittest
from src.post_processing.processing_functions import stack_time_keyboard


class TestStackTimeKeyboard(unittest.TestCase):
    def test_single_key_press_release(self):
        events = [
            ("key_press", "a", 0.1),
            ("key_press", "a", 0.2),
            ("key_release", "a", 0.3),
        ]
        expected = [
            ("key_press", "a", 0.3),
            ("key_release", "a", 0.3),
        ]
        self.assertEqual(stack_time_keyboard(events), expected)

    def test_multiple_keys(self):
        events = [
            ("key_press", "a", 0.1),
            ("key_press", "a", 0.2),
            ("key_release", "a", 0.3),
            ("key_press", "b", 0.1),
            ("key_release", "b", 0.2),
        ]
        expected = [
            ("key_press", "a", 0.3),
            ("key_release", "a", 0.3),
            ("key_press", "b", 0.1),
            ("key_release", "b", 0.2),
        ]
        self.assertEqual(stack_time_keyboard(events), expected)

    def test_alternating_key_presses(self):
        events = [
            ("key_press", "a", 0.1),
            ("key_release", "a", 0.2),
            ("key_press", "b", 0.3),
            ("key_release", "b", 0.4),
            ("key_press", "a", 0.1),
            ("key_release", "a", 0.2),
        ]
        expected = [
            ("key_press", "a", 0.1),
            ("key_release", "a", 0.2),
            ("key_press", "b", 0.3),
            ("key_release", "b", 0.4),
            ("key_press", "a", 0.1),
            ("key_release", "a", 0.2),
        ]
        self.assertEqual(stack_time_keyboard(events), expected)

    def test_no_events(self):
        events = []
        expected = []
        self.assertEqual(stack_time_keyboard(events), expected)

    def test_intermixed_non_key_events(self):
        events = [
            ("move", 100, 200, 0.05),
            ("key_press", "a", 0.1),
            ("key_press", "a", 0.2),
            ("scroll", 627, 271, 0, -1, 0.1),
            ("key_release", "a", 0.3),
            ("key_release", "a", 0.4),
            ("click_down", 100, 200, "left", 0.1),
            ("click_up", 100, 200, "left", 0.2),
        ]
        expected = [
            ("move", 100, 200, 0.05),
            ("key_press", "a", 0.3),
            ("scroll", 627, 271, 0, -1, 0.1),
            ("key_release", "a", 0.7),
            ("click_down", 100, 200, "left", 0.1),
            ("click_up", 100, 200, "left", 0.2),
        ]
        self.assertEqual(stack_time_keyboard(events), expected)

    def test_only_non_key_events(self):
        events = [
            ("move", 100, 200, 0.05),
            ("scroll", 627, 271, 0, -1, 0.1),
            ("click_down", 100, 200, "left", 0.1),
            ("click_up", 100, 200, "left", 0.2),
        ]
        expected = [
            ("move", 100, 200, 0.05),
            ("scroll", 627, 271, 0, -1, 0.1),
            ("click_down", 100, 200, "left", 0.1),
            ("click_up", 100, 200, "left", 0.2),
        ]
        self.assertEqual(stack_time_keyboard(events), expected)

    def test_simultaneous_presses(self):
        events = [
            ("key_press", "a", 0.1),
            ("key_press", "a", 0.2),
            ("key_press", "b", 0.4),
            ("key_press", "a", 0.3),
            ("key_press", "a", 0.4),
            ("key_release", "b", 0.2),
            ("key_release", "a", 0.4),
        ]
        expected = [
            ("key_press", "a", 0.3),
            ("key_press", "b", 0.4),
            ("key_press", "a", 0.7),
            ("key_release", "b", 0.2),
            ("key_release", "a", 0.4),
        ]
        self.assertEqual(stack_time_keyboard(events), expected)


if __name__ == '__main__':
    unittest.main()
