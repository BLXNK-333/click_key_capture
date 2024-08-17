import unittest
from src.post_processing.processing_functions import remove_unpaired_up_events


class TestRemoveUnpairedUpEvents(unittest.TestCase):
    def test_remove_key_events(self):
        events = [
            ("key_press", "a", 0.1),
            ("key_release", "a", 0.2),
            ("key_press", "b", 0.3),
            ("key_release", "b", 0.4),
            ("key_release", "c", 0.5),  # Непарное событие
        ]
        expected = [
            ("key_press", "a", 0.1),
            ("key_release", "a", 0.2),
            ("key_press", "b", 0.3),
            ("key_release", "b", 0.4),
        ]
        self.assertEqual(remove_unpaired_up_events(events), expected)

    def test_remove_mouse_events(self):
        events = [
            ("click_down", 100, 200, "left", 0.1),
            ("click_up", 100, 200, "left", 0.2),
            ("click_down", 100, 200, "right", 0.3),
            ("click_up", 100, 200, "left", 0.4),  # Непарное событие
            ("click_up", 100, 200, "right", 0.5)
        ]
        expected = [
            ("click_down", 100, 200, "left", 0.1),
            ("click_up", 100, 200, "left", 0.2),
            ("click_down", 100, 200, "right", 0.3),
            ("click_up", 100, 200, "right", 0.5)
        ]
        self.assertEqual(remove_unpaired_up_events(events), expected)

    def test_move_and_scroll_events(self):
        events = [
            ("move", 100, 200, 0.1),
            ("scroll", 627, 271, 0, -1, 0.05),
            ("key_press", "a", 0.3),
            ("key_release", "a", 0.4),
        ]
        expected = [
            ("move", 100, 200, 0.1),
            ("scroll", 627, 271, 0, -1, 0.05),
            ("key_press", "a", 0.3),
            ("key_release", "a", 0.4),
        ]
        self.assertEqual(remove_unpaired_up_events(events), expected)

    def test_empty_events(self):
        events = []
        expected = []
        self.assertEqual(remove_unpaired_up_events(events), expected)

    def test_all_unpaired_events(self):
        events = [
            ("key_release", "Key.ctrl", 0.02),
            ("key_release", "Key.space", 1.05),
            ("click_up", 100, 200, "left", 0.2),
            ("key_release", "a", 0.03),
        ]
        expected = []
        self.assertEqual(remove_unpaired_up_events(events), expected)


if __name__ == '__main__':
    unittest.main()