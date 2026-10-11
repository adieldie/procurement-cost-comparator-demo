"""Offline illustrative comparison. No supplier connection or purchase execution."""
from decimal import Decimal, InvalidOperation


def number(value, label, *, positive=False):
    try:
        result = Decimal(str(value).strip().replace(',', '.'))
    except (InvalidOperation, ValueError):
        raise ValueError(f'{label}: informe um número válido.') from None
    if not result.is_finite() or result < 0 or (positive and result == 0):
        raise ValueError(f'{label}: valor inválido.')
    return result


def compare(cost_a, cost_b, points=0, units=1, points_per_currency=125, sale=0):
    """Two comparable unit quotes; optional hypothetical points on A's pack.

    Keeps exact Decimal arithmetic until display. A zero cost is a valid quote.
    Points are illustrative future benefits, not a cash discount on an invoice.
    """
    a = number(cost_a, 'Custo A')
    b = number(cost_b, 'Custo B')
    p = number(points, 'Pontos')
    q = number(units, 'Unidades', positive=True)
    rate = number(points_per_currency, 'Taxa de pontos', positive=True)
    selling = number(sale, 'Venda')
    benefit = p / rate / q
    effective = max(Decimal('0'), a - benefit)
    winner = 'A' if effective < b else 'B' if b < effective else 'Empate'
    return {'cost_a': a, 'cost_b': b, 'benefit_a': benefit,
            'effective_a': effective, 'difference': abs(effective - b),
            'winner': winner,
            'margin_a': ((selling-effective)/selling*100) if selling else None,
            'margin_b': ((selling-b)/selling*100) if selling else None}


if __name__ == '__main__':
    # Entirely fictional, directly reproducible example; no file/network access.
    r = compare('10.00', '9.80', 500, 10, 125, 15)
    print('DEMONSTRAÇÃO — dados fictícios')
    print(f"A após benefício hipotético: {r['effective_a']:.2f}")
    print(f"B: {r['cost_b']:.2f}; menor custo ilustrativo: {r['winner']}")
    print(f"Diferença por unidade: {r['difference']:.2f}")
