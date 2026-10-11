# Procurement Cost Comparator · Demo

**Estágio: experimental / em teste. Demonstração parcial sanitizada, não pronta para produção.**

Comparador offline de duas cotações, com benefício hipotético por embalagem e margem bruta estimada. Uma demonstração desktop em Python para tornar explícitas as premissas de uma comparação de custos.

## O que demonstra

- Comparação de custos unitários de duas opções equivalentes.
- Distribuição de um benefício em pontos pelas unidades de uma embalagem.
- Cálculo com `Decimal`, validação de entradas e identificação de empate.
- Interface desktop e histórico local opcional, gravado somente ao clicar em **Salvar**.
- Exemplo fictício executável no terminal, sem dependências externas.

## Comece pelo exemplo

Requer Python 3.10 ou superior. Na pasta deste projeto:

```sh
python core.py
python -m unittest discover -s tests -v
```

Resultado do exemplo: custo estimado A = 9,60; B = 9,80; diferença = 0,20 por unidade. Todos os números foram inventados para esta demonstração.

## Interface desktop opcional

Crie um ambiente isolado e instale a dependência de interface:

```sh
python -m venv .venv
# Linux/macOS:
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python app.py
# Windows (PowerShell):
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe app.py
```

A distribuição do Python precisa incluir Tk e um ambiente gráfico. A interface foi preparada para desktop, não navegador/celular. A biblioteca externa é instalada separadamente; seu código não está incluído neste repositório.

Informe os dois custos unitários; pontos, unidades por embalagem e preço de venda são opcionais. Exemplo: A = 10, B = 9,80, pontos = 500, unidades = 10, venda = 15. Use nomes fictícios se for compartilhar uma captura.

O histórico fica em `.procurement-demo-history.json` na pasta pessoal do usuário; não é enviado à internet. O botão de limpeza pede confirmação. Não inclua esse arquivo em commits ou publicações.

## Regras transparentes

`benefício por unidade = pontos / taxa de conversão / unidades`

`custo estimado A = máximo(0, custo A - benefício por unidade)`

`margem bruta estimada = (venda - custo estimado) / venda × 100`

A interface usa a hipótese ilustrativa de 125 pontos para uma unidade monetária. A função `compare` aceita outra taxa. Isso não representa programa comercial real, valor de resgate garantido nem desconto imediato na nota. Frete, tributos, vencimento de pontos, prazo de pagamento, qualidade e disponibilidade não são modelados. Compare produtos de mesma unidade e condições equivalentes. A indicação de menor custo não executa compra nem substitui avaliação financeira/fiscal.

## Estrutura

- `app.py`: interface desktop adaptada e histórico local.
- `core.py`: cálculo independente da interface e exemplo fictício.
- `tests/test_core.py`: testes de precisão, validação e casos-limite.

## Estágio e limites

Demonstração sanitizada de um recorte de projeto, não cópia integral do sistema original. Não contém conexão com ERP, importação de notas, banco operacional, credenciais ou dados de fornecedores. Os testes do núcleo passaram em ambiente sem interface gráfica. A abertura e a renderização da janela desktop ainda precisam de validação manual no sistema de destino. Nenhuma economia real de tempo ou dinheiro foi medida.

## Licença

Nenhuma licença de redistribuição foi escolhida nesta preparação. A publicação e uma eventual licença dependem da revisão de titularidade e dos direitos aplicáveis. Não se presume uma licença permissiva por o código estar visível.
