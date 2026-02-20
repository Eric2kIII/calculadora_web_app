from decimal import Decimal

from django import forms


class CompoundInterestForm(forms.Form):
    TAXA_PERIODO_CHOICES = (
        ("mensal", "Ao mes"),
        ("anual", "Ao ano"),
    )
    PRAZO_PERIODO_CHOICES = (
        ("meses", "Meses"),
        ("anos", "Anos"),
    )

    principal = forms.DecimalField(
        label="Aporte inicial",
        min_value=Decimal("0"),
        decimal_places=2,
        max_digits=16,
        initial=Decimal("0"),
    )
    aporte_mensal = forms.DecimalField(
        label="Aporte mensal (opcional)",
        min_value=Decimal("0"),
        decimal_places=2,
        max_digits=16,
        initial=Decimal("0"),
        required=False,
    )
    taxa = forms.DecimalField(
        label="Taxa de juros (%)",
        min_value=Decimal("0"),
        decimal_places=6,
        max_digits=10,
        initial=Decimal("0"),
    )
    taxa_periodo = forms.ChoiceField(
        label="Periodicidade da taxa",
        choices=TAXA_PERIODO_CHOICES,
        initial="mensal",
    )
    prazo = forms.IntegerField(
        label="Prazo",
        min_value=1,
        initial=12,
    )
    prazo_periodo = forms.ChoiceField(
        label="Periodicidade do prazo",
        choices=PRAZO_PERIODO_CHOICES,
        initial="meses",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_input_class = (
            "w-full rounded-xl border border-slate-300 bg-white px-3 py-2.5 text-slate-900 "
            "shadow-sm outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-200"
        )
        select_class = (
            "w-full rounded-xl border border-slate-300 bg-white px-3 py-2.5 text-slate-900 "
            "shadow-sm outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-200"
        )
        for name in ("principal", "aporte_mensal", "taxa", "prazo"):
            self.fields[name].widget.attrs.update({"class": base_input_class})
        for name in ("taxa_periodo", "prazo_periodo"):
            self.fields[name].widget.attrs.update({"class": select_class})

    def clean(self):
        cleaned_data = super().clean()
        taxa = cleaned_data.get("taxa")
        prazo = cleaned_data.get("prazo")
        aporte_mensal = cleaned_data.get("aporte_mensal")

        if aporte_mensal is None:
            cleaned_data["aporte_mensal"] = Decimal("0")

        if taxa is not None and taxa > Decimal("1000"):
            self.add_error("taxa", "A taxa deve ser ate 1000% para manter um calculo estavel.")

        if prazo is not None and prazo <= 0:
            self.add_error("prazo", "O prazo deve ser maior que zero.")

        return cleaned_data
