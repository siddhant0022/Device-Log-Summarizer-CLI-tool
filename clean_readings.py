# Section 1 - Clean and normalize sensor readings

def clean_readings(values):
    """Takes a list of mixed values and returns a list of cleaned floats.

    - converts to float where possible
    - drops None, unconvertible values and negatives
    - caps anything above 500.0 at 500.0
    """
    cleaned = []

    # if the input is None or not a list/tuple, just return empty list
    if not isinstance(values, (list, tuple)):
        return cleaned

    for v in values:
        if v is None:
            continue
        # bool is technically an int in python, so skip it
        if isinstance(v, bool):
            continue
        try:
            num = float(v)
        except (ValueError, TypeError):
            continue

        # float("nan") converts fine but is not a real reading
        if num != num:
            continue
        if num < 0:
            continue
        if num > 500.0:
            num = 500.0
        cleaned.append(num)

    return cleaned


def run_tests():
    # test 1: mixed input
    assert clean_readings(["12.5", None, -3, "abc", 600, 40]) == [12.5, 500.0, 40.0]

    # test 2: empty list
    assert clean_readings([]) == []

    # test 3: everything invalid
    assert clean_readings([None, "xyz", -1, "-9.5"]) == []

    # test 4: edge values (0 is valid, exactly 500 stays 500)
    assert clean_readings([0, "500", "500.1"]) == [0.0, 500.0, 500.0]

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()
