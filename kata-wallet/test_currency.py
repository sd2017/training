import random
import pytest

from exchange_rates import fixed_exchange_rates
from currency import EUR, USD, XBT


def any_amount():
    return random.randint(1, 10000)


def test_precision_should_round_to_nearest_value():
    assert EUR.amount(1.234) == EUR(1.23)
    assert EUR.amount(1.235) == EUR(1.24)
    assert EUR.amount(1.236) == EUR(1.24)


def test_eur_should_have_2_digits_precision():
    assert EUR.amount(0.01) == EUR(0.01)
    assert EUR.amount(0.001) == EUR(0)


def test_usd_should_have_3_digits_precision():
    assert USD.amount(0.001) == USD(0.001)
    assert USD.amount(0.0001) == USD(0)


def test_xbt_should_have_8_digits_precision():
    assert XBT.amount(0.00000001) == XBT(0.00000001)
    assert XBT.amount(0.000000001) == XBT(0)


def test_money_should_be_addable_when_same_currency():
    assert EUR(2) + EUR(3) == EUR(5)


def test_money_should_have_a_neutral_element_for_add():
    element = EUR(any_amount())
    neutral = EUR(0)
    assert neutral + element == element + neutral == element


def test_money_should_be_assosiative_for_add():
    x = EUR(any_amount())
    y = EUR(any_amount())
    z = EUR(any_amount())
    assert (x + y) + z == x + (y + z) == x + y + z


def test_money_should_raise_error_when_currency_mismatch():
    with pytest.raises(TypeError) as exception:
        _ = EUR(any_amount()) + USD(any_amount())
    assert str(exception.value) == 'Mismatch currency, expected EUR got USD'


def test_money_should_be_changed_with_an_exchange_rate():
    assert EUR(10).change(USD, fixed_exchange_rates("1 EUR = 1.19 USD")) == USD(11.9)
