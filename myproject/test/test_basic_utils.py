from myproject.basic_utils import multiply_ten

def test_multiply_ten():
    assert multiply_ten(3) == 30
    assert multiply_ten(-1) == -10
