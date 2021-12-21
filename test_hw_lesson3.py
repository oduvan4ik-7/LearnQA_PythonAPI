# python -m pytest -s test_hw_lesson3.py -k phrase
def test_phrase():
    phrase = input("Set a phrase with max len 15 characters: ")
    length = len(phrase)

    assert length <= 15, f"Your phrase has length={length}, which is longer than 15 characters"

