import unittest
from src.event_handlers.events import Action
from src.post_processing.processing_functions import get_hot_corner_insert_indices


class TestGetHotCornerInsertIndices(unittest.TestCase):

    def test_empty_events(self):
        events = []
        expected = []
        result = get_hot_corner_insert_indices(events)
        self.assertEqual(result, expected)

    def test_events_no_clicks(self):
        events = [
            (Action.MOVE, 0, 0, 0.1),
            (Action.MOVE, 100, 100, 0.1),
            (Action.MOVE, 0, 0, 0.1),
            (Action.MOVE, 200, 200, 0.1)
        ]
        expected = [0, 2]
        result = get_hot_corner_insert_indices(events)
        self.assertEqual(result, expected)

    def test_events_with_clicks(self):
        events = [
            (Action.MOVE, 0, 0, 0.1),
            (Action.CLICK_DOWN, 50, 50, 0.1),
            (Action.MOVE, 100, 100, 0.1),
            (Action.MOVE, 0, 0, 0.1),
            (Action.CLICK_UP, 150, 150, 0.1),
            (Action.MOVE, 200, 200, 0.1)
        ]
        expected = [3]
        result = get_hot_corner_insert_indices(events)
        self.assertEqual(result, expected)

    def test_corner_with_no_clicks(self):
        events = [
            (Action.MOVE, 0, 0, 0.1),
            (Action.MOVE, 0, 0, 0.1),
            (Action.MOVE, 50, 50, 0.1),
            (Action.MOVE, 0, 0, 0.1),
            (Action.MOVE, 100, 100, 0.1)
        ]
        expected = [0, 3]
        result = get_hot_corner_insert_indices(events)
        self.assertEqual(result, expected)

    def test_corner_with_clicks(self):
        events = [
            (Action.MOVE, 0, 0, 0.1),
            (Action.MOVE, 50, 50, 0.1),
            (Action.CLICK_DOWN, 50, 50, 0.1),
            (Action.MOVE, 0, 0, 0.1),
            (Action.CLICK_UP, 50, 50, 0.1),
            (Action.MOVE, 100, 100, 0.1)
        ]
        expected = [0]
        result = get_hot_corner_insert_indices(events)
        self.assertEqual(result, expected)

    def test_corner_with_esc(self):
        events = [
            (Action.MOVE, 0, 0, 0.1),
            (Action.MOVE, 0, 0, 0.1),
            (Action.KEY_PRESS, "Key.esc", 0.1),
            (Action.CLICK_UP, 50, 50, 0.1)
        ]
        expected = [0]
        result = get_hot_corner_insert_indices(events)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
