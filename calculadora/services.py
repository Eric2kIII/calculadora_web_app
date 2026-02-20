from decimal import Decimal, getcontext


getcontext().prec = 28

TWELVE = Decimal("12")
ONE = Decimal("1")
ZERO = Decimal("0")


def to_monthly_rate(rate_percent: Decimal, rate_period: str) -> Decimal:
    rate_decimal = rate_percent / Decimal("100")
    if rate_period == "anual":
        return (ONE + rate_decimal) ** (ONE / TWELVE) - ONE
    return rate_decimal


def to_months(duration: int, duration_period: str) -> int:
    if duration_period == "anos":
        return duration * 12
    return duration


def calculate_compound_interest(
    principal: Decimal,
    monthly_contribution: Decimal,
    rate_percent: Decimal,
    rate_period: str,
    duration: int,
    duration_period: str,
) -> dict:
    monthly_rate = to_monthly_rate(rate_percent, rate_period)
    months = to_months(duration, duration_period)

    factor = (ONE + monthly_rate) ** months
    fv_principal = principal * factor

    if monthly_rate == ZERO:
        fv_contributions = monthly_contribution * Decimal(months)
    else:
        fv_contributions = monthly_contribution * ((factor - ONE) / monthly_rate)

    total_future_value = fv_principal + fv_contributions
    total_invested = principal + (monthly_contribution * Decimal(months))
    interest_earned = total_future_value - total_invested

    return {
        "months": months,
        "monthly_rate": monthly_rate,
        "future_value": total_future_value,
        "total_invested": total_invested,
        "interest_earned": interest_earned,
    }
