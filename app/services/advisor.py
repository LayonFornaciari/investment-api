from groq import Groq
from typing import List, Dict

# 🔑 SUA CHAVE GROQ (Hardcoded para facilitar para a banca)
API_KEY = "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"

# Inicializa o cliente Groq
# O Groq vai usar essa chave automaticamente
client = Groq(api_key=API_KEY)


def get_ai_insight(assets: List[Dict], total_value: float) -> str:
    """
    Gera insight usando o modelo Llama-3 na Groq (Extremamente rápido).
    """
    try:
        # 1. Monta o Prompt
        prompt = f"""
        Atue como um consultor financeiro experiente, ácido e sarcástico (estilo 'The Big Short').
        Analise esta carteira de investimentos:

        Valor Total: $ {total_value:.2f}
        Ativos: {assets}

        Regras de Resposta:
        1. Identifique o maior risco de concentração ou uma oportunidade perdida.
        2. Dê um conselho curto e direto (máximo 2 frases).
        3. Use emojis financeiros.
        4. Responda em Português do Brasil.
        5. NÃO use formatação markdown (negrito/itálico), apenas texto puro.
        """

        # 2. Chama a API da Groq
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            # Llama 3 70B é um modelo muito inteligente e rápido
            model="llama-3.3-70b-versatile",
        )

        # 3. Retorna o texto
        return chat_completion.choices[0].message.content.strip()

    except Exception as e:
        print(f"❌ Erro na Groq: {e}")
        return None


def get_rule_based_insight(assets: List[Dict], total_value: float) -> str:
    """
    FALLBACK: Lógica baseada em regras (Offline).
    """
    if not assets or total_value == 0:
        return "Carteira vazia. Adicione ativos para análise."

    biggest_asset = max(assets, key=lambda x: x['total_value'])
    pct = (biggest_asset['total_value'] / total_value) * 100
    ticker = biggest_asset['ticker']

    if pct > 60:
        return f"🚨 RISCO CRÍTICO (Offline): {pct:.1f}% do capital em {ticker}. Diversifique!"
    elif pct > 30:
        return f"⚠️ Atenção: Concentração alta em {ticker} ({pct:.1f}%)."
    else:
        return f"🛡️ Carteira bem diversificada (Maior: {ticker} com {pct:.1f}%)."


def analyze_portfolio(assets: List[Dict], total_value: float) -> str:
    # Tenta IA (Groq) Primeiro
    ai_insight = get_ai_insight(assets, total_value)

    if ai_insight:
        return ai_insight
    else:
        return get_rule_based_insight(assets, total_value)