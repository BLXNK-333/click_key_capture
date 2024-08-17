import unittest
from src.post_processing.processing_functions import remove_unpaired_down_events


class TestRemoveUnpairedDownEventsWithPressedSet(unittest.TestCase):
    def test_no_unpaired_down_events(self):
        events = [
            ("key_press", "a", 0.1),
            ("key_release", "a", 0.2),
            ("key_press", "b", 0.3),
            ("key_release", "b", 0.4),
        ]
        pressed = set()
        expected = events
        self.assertEqual(remove_unpaired_down_events(events, pressed), expected)

    def test_remove_unpaired_down_key_event(self):
        events = [
            ("key_press", "a", 0.1),
            ("key_press", "b", 0.2),
            ("key_release", "b", 0.3),
            ("key_press", "a", 0.4),
        ]
        pressed = {"a"}
        expected = [
            ("key_press", "a", 0.1),
            ("key_press", "b", 0.2),
            ("key_release", "b", 0.3),
        ]
        self.assertEqual(remove_unpaired_down_events(events, pressed), expected)

    def test_remove_unpaired_down_mouse_event(self):
        events = [
            ("click_down", 100, 200, "left", 0.1),
            ("click_down", 100, 200, "right", 0.2),
            ("click_up", 100, 200, "right", 0.3),
            ("click_down", 100, 200, "left", 0.4),
        ]
        pressed = {"click_left"}
        expected = [
            ("click_down", 100, 200, "left", 0.1),
            ("click_down", 100, 200, "right", 0.2),
            ("click_up", 100, 200, "right", 0.3),
        ]
        self.assertEqual(remove_unpaired_down_events(events, pressed), expected)

    def test_intermixed_events_with_untracked(self):
        events = [
            ("move", 100, 200, 0.05),
            ("key_press", "a", 0.1),
            ("scroll", 627, 271, 0, -1, 0.15),
            ("key_press", "b", 0.2),
            ("key_release", "b", 0.3),
        ]
        pressed = {"a"}
        expected = [
            ("move", 100, 200, 0.05),
            ("scroll", 627, 271, 0, -1, 0.15),
            ("key_press", "b", 0.2),
            ("key_release", "b", 0.3),
        ]
        self.assertEqual(remove_unpaired_down_events(events, pressed), expected)

    def test_no_pressed_set(self):
        events = [
            ("key_press", "a", 0.1),
            ("key_release", "a", 0.2),
            ("key_press", "b", 0.3),
            ("key_release", "b", 0.4),
        ]
        pressed = set()
        expected = events
        self.assertEqual(remove_unpaired_down_events(events, pressed), expected)

    def test_all_unpaired_down_events(self):
        events = [
            ("key_press", "a", 0.1),
            ("key_press", "b", 0.2),
            ("click_down", 100, 200, "left", 0.3),
        ]
        pressed = {"a", "b", "click_left"}
        expected = []
        self.assertEqual(remove_unpaired_down_events(events, pressed), expected)

    def test_shaffle_events(self):
        events = [
            ("move", 603, 455, 0.0077),
            ("click_down", 603, 455, "left", 0.08827),
            ("click_up", 603, 455, "left", 0.4709),
            ("key_press", "Key.ctrl", 0.1338)
        ]
        pressed = {"Key.ctrl"}
        expected = [
            ("move", 603, 455, 0.0077),
            ("click_down", 603, 455, "left", 0.08827),
            ("click_up", 603, 455, "left", 0.4709)
        ]
        self.assertEqual(remove_unpaired_down_events(events, pressed), expected)


if __name__ == '__main__':
    unittest.main()
