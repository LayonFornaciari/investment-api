from typing import List, Dict


def analyze_portfolio(assets: List[Dict], total_value: float) -> str:
    if not assets or total_value == 0:
        return "Carteira vazia. Inicie operações para receber análises."

    # 1. Achar a maior posição
    biggest_asset = None
    highest_value = -1

    for asset in assets:
        # Garante que estamos pegando o valor calculado
        val = asset.get('total_value', 0)
        if val > highest_value:
            highest_value = val
            biggest_asset = asset

    if not biggest_asset:
        return "Aguardando dados de mercado..."

    # 2. Calcular porcentagem
    concentration_pct = (highest_value / total_value) * 100
    ticker = biggest_asset['ticker']

    # 3. Regras de "Humano"
    if concentration_pct > 60:
        return f"🚨 RISCO CRÍTICO: {concentration_pct:.1f}% do seu capital está apenas em {ticker}. Diversifique urgente!"

    elif concentration_pct > 35:
        return f"⚠️ Atenção: Você está muito exposto em {ticker} ({concentration_pct:.1f}%). Considere rebalancear."

    elif concentration_pct > 20:
        return f"📊 Carteira Moderada. Maior posição: {ticker} com {concentration_pct:.1f}%."

    else:
        return f"🏆 Excelente Diversificação! Seu maior ativo ({ticker}) representa apenas {concentration_pct:.1f}% do total."