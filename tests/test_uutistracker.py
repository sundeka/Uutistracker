from src.abstractions.apiresponse import APIResponse
from datetime import datetime
from src.uutistracker import Uutistracker

def test_sort(mocker):
    mocker.patch('src.implementations.iltasanomat.Iltasanomat', return_value=None)
    tracker = Uutistracker()
    unsorted_mock_feed = [
        APIResponse("a", "a", datetime(2022, 6, 6, 12, 54, 0)),
        APIResponse("b", "b", datetime(2021, 6, 6, 12, 54, 0)),
        APIResponse("c", "c", datetime(2023, 6, 6, 12, 54, 0))
    ]
    sorted_mock_feed = [
        APIResponse("b", "b", datetime(2023, 6, 6, 12, 54, 0)),
        APIResponse("a", "a", datetime(2022, 6, 6, 12, 54, 0)),
        APIResponse("c", "c", datetime(2021, 6, 6, 12, 54, 0))
    ]
    tracker_sorted = tracker.sort(unsorted_mock_feed)
    for a, b in zip(sorted_mock_feed, tracker_sorted):
        assert a.time == b.time

def test_check_new_headlines_no_previous(mocker):
    # When there are no pre-existing headlines, 
    # consider all of the updated headlines as new headlines
    mocker.patch('src.implementations.iltasanomat.Iltasanomat', return_value=None)
    tracker = Uutistracker()
    tracker.feed_current = [
        APIResponse("b", "b", datetime(2021, 6, 6, 12, 54, 0)),
        APIResponse("a", "a", datetime(2022, 6, 6, 12, 54, 0)),
        APIResponse("c", "c", datetime(2023, 6, 6, 12, 54, 0))
    ]
    tracker.feed_previous = []
    new_headlines = tracker.check_new_headlines()
    assert new_headlines == tracker.feed_current

def test_check_new_headlines(mocker):
    mocker.patch('src.implementations.iltasanomat.Iltasanomat', return_value=None)
    tracker = Uutistracker()
    tracker.feed_current = [
        APIResponse("b", "b", datetime(2021, 6, 6, 12, 54, 0)),
        APIResponse("a", "a", datetime(2022, 6, 6, 12, 54, 0)),
        APIResponse("c", "c", datetime(2023, 6, 6, 12, 54, 0))
    ]
    tracker.feed_previous = [
        APIResponse("c", "c", datetime(2023, 6, 6, 12, 54, 0))
    ]
    new_headlines = tracker.check_new_headlines()
    for a, b in zip(new_headlines, [
        APIResponse("b", "b", datetime(2021, 6, 6, 12, 54, 0)),
        APIResponse("a", "a", datetime(2022, 6, 6, 12, 54, 0)),
    ]):
        assert a.time == b.time

