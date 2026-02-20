from decimal import Decimal, ROUND_HALF_UP

from django.shortcuts import render

from .forms import CompoundInterestForm
from .services import calculate_compound_interest


def format_brl(value: Decimal) -> str:
    rounded = value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    raw = f"{rounded:,.2f}"
    return f"R$ {raw.replace(',', 'X').replace('.', ',').replace('X', '.')}"


def build_summary(months: int, future_value: Decimal) -> str:
    if months % 12 == 0:
        years = months // 12
        unit = "ano" if years == 1 else "anos"
        return f"Em {years} {unit}, seu investimento pode chegar a {format_brl(future_value)}."
    unit = "mes" if months == 1 else "meses"
    return f"Em {months} {unit}, seu investimento pode chegar a {format_brl(future_value)}."


def index(request):
    result = None

    if request.method == "POST":
        if request.POST.get("action") == "clear":
            form = CompoundInterestForm()
        else:
            form = CompoundInterestForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                calculation = calculate_compound_interest(
                    principal=data["principal"],
                    monthly_contribution=data["aporte_mensal"],
                    rate_percent=data["taxa"],
                    rate_period=data["taxa_periodo"],
                    duration=data["prazo"],
                    duration_period=data["prazo_periodo"],
                )
                result = {
                    "future_value": format_brl(calculation["future_value"]),
                    "total_invested": format_brl(calculation["total_invested"]),
                    "interest_earned": format_brl(calculation["interest_earned"]),
                    "summary": build_summary(calculation["months"], calculation["future_value"]),
                }
    else:
        form = CompoundInterestForm()

    return render(request, "calculadora/index.html", {"form": form, "result": result})
