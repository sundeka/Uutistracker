from src.abstractions.apiresponse import APIResponse
from datetime import datetime
from src.uutistracker import Uutistracker

def test_sorter(mocker):
    mocker.patch('src.implementations.iltasanomat.Iltasanomat', return_value=None)
    tracker = Uutistracker()
    unsorted_mock_feed = [
        APIResponse("a", "a", datetime(2022, 6, 6, 12, 54, 0)),
        APIResponse("b", "b", datetime(2021, 6, 6, 12, 54, 0)),
        APIResponse("c", "c", datetime(2023, 6, 6, 12, 54, 0))
    ]
    sorted_mock_feed = [
        APIResponse("b", "b", datetime(2021, 6, 6, 12, 54, 0)),
        APIResponse("a", "a", datetime(2022, 6, 6, 12, 54, 0)),
        APIResponse("c", "c", datetime(2023, 6, 6, 12, 54, 0))
    ]
    tracker_sorted = tracker.sort(unsorted_mock_feed)
    for a, b in zip(sorted_mock_feed, tracker_sorted):
        assert a.time == b.time