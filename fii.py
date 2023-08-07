import yfinance as yf
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd

'''
AJUSTAR CÁLCULOS DE PONTO MÉDIO
'''

def obter_valor_atual(fundo):
    ticker = f"{fundo}.SA"
    fundo_info = yf.Ticker(ticker)

    try:
        valor_atual = fundo_info.history(period="1d")["Close"].iloc[-1]
        return valor_atual
    except:
        return None

def calcular_ponto_medio(compras):
    total_valor = sum(compra['Total'] for compra in compras)
    total_cotas = sum(compra['Quantidade'] for compra in compras)
    return total_valor / total_cotas

def calcular_lucro_prejuizo(valor_compra, valor_venda, quantidade_cotas):
    return (valor_venda - valor_compra) * quantidade_cotas

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG, "style.css"])

csv_file_path = "fundosListados.csv"
fund_options_df = pd.read_csv(csv_file_path, delimiter=";", usecols=["Código"], encoding="ISO-8859-1")
fund_options_df.rename(columns={"Código": "value"}, inplace=True)
fund_options = fund_options_df["value"].tolist()

app.layout = dbc.Container([
    html.H1("Análise de Fundos Imobiliários", className="h1"),
    dbc.Row([
        dbc.Col([
            html.Label("Selecione o Fundo:", className="label"),
            dcc.Dropdown(id="input-fundo", options=[{"label": fundo, "value": fundo} for fundo in fund_options], value="", className="input-field")
        ]),
    ]),
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("Compra 1 - Valor:", className="label_compra"),
                    dcc.Input(id="input-valor-compra", type="number", value="", className="input-field")
                ]),
                dbc.Col([
                    html.Label("Compra 1 - Cotas:", className="label_compra"),
                    dcc.Input(id="input-cotas-compradas", type="number", value="", className="input-field")
                ]),        
            ]),
            dbc.Row([
                dbc.Col([
                    html.Label("Compra 2 - Valor:", className="label_compra"),
                    dcc.Input(id="input-valor-compra-2", type="number", value="", className="input-field")
                ]),
                dbc.Col([
                    html.Label("Compra 2 - Cotas:", className="label_compra"),
                    dcc.Input(id="input-cotas-compradas-2", type="number", value="", className="input-field")
                ]),        
            ]),
            dbc.Row([
                dbc.Col([
                    html.Label("Compra 3 - Valor:", className="label_compra"),
                    dcc.Input(id="input-valor-compra-3", type="number", value="", className="input-field")
                ]),
                dbc.Col([
                    html.Label("Compra 3 - Cotas:", className="label_compra"),
                    dcc.Input(id="input-cotas-compradas-3", type="number", value="", className="input-field")
                ]),        
            ]),
            dbc.Row([
                dbc.Col([
                    html.Label("Compra 4 - Valor:", className="label_compra"),
                    dcc.Input(id="input-valor-compra-4", type="number", value="", className="input-field")
                ]),
                dbc.Col([
                    html.Label("Compra 4 - Cotas:", className="label_compra"),
                    dcc.Input(id="input-cotas-compradas-4", type="number", value="", className="input-field")
                ]),        
            ]),
        ]),
        className="mt-3"
    ),
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("Valor de Venda:", className="label_venda"),
                    dcc.Input(id="input-valor-venda", type="number", value="", className="input-field")
                ]),
                dbc.Col([
                    html.Label("Cotas Venda:", className="label_venda"),
                    dcc.Input(id="input-cotas-venda", type="number", value="", className="input-field")
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Button("Calcular", id="calcular-button", n_clicks=0, color="primary", className="mt-4")
                ])
            ], className="col"),
        ]),
        className="mt-3"
    ),
    html.Div(id="resultado-container", className="resultado-container"),
    dbc.NavbarSimple(
        children=[
            dbc.NavItem("Desenvolvido por Rafael Barbosa | 2023", className="footer")
        ],
        color="dark",
        dark=True,
        className="footer"
    )    
], fluid=True)

@app.callback(
    Output("resultado-container", "children"),
    [Input("calcular-button", "n_clicks")],
    [
        dash.dependencies.State("input-fundo", "value"),
        dash.dependencies.State("input-valor-compra", "value"),
        dash.dependencies.State("input-cotas-compradas", "value"),        
        dash.dependencies.State("input-valor-compra-2", "value"),
        dash.dependencies.State("input-cotas-compradas-2", "value"),
        dash.dependencies.State("input-valor-compra-3", "value"),
        dash.dependencies.State("input-cotas-compradas-3", "value"),
        dash.dependencies.State("input-valor-compra-4", "value"),
        dash.dependencies.State("input-cotas-compradas-4", "value"),
        dash.dependencies.State("input-valor-venda", "value"),
        dash.dependencies.State("input-cotas-venda", "value"),
    ],
)
def calcular_e_mostrar_resultado(n_clicks, fundo, valor_compra, cotas_compradas, valor_compra_2, cotas_compradas_2, valor_compra_3, cotas_compradas_3, valor_compra_4, cotas_compradas_4, valor_venda, cotas_venda):
    if n_clicks > 0:
        valor_compra = float(valor_compra) if valor_compra else 0
        cotas_compradas = float(cotas_compradas) if cotas_compradas else 0
        valor_compra_2 = float(valor_compra_2) if valor_compra_2 else 0
        cotas_compradas_2 = float(cotas_compradas_2) if cotas_compradas_2 else 0
        valor_compra_3 = float(valor_compra_3) if valor_compra_3 else 0
        cotas_compradas_3 = float(cotas_compradas_3) if cotas_compradas_3 else 0
        valor_compra_4 = float(valor_compra_4) if valor_compra_4 else 0
        cotas_compradas_4 = float(cotas_compradas_4) if cotas_compradas_4 else 0
        valor_venda = float(valor_venda) if valor_venda else 0
        cotas_venda = float(cotas_venda) if cotas_venda else 0
        
        valor_atual = obter_valor_atual(fundo)
        if valor_atual is not None:
            compras = [
                {'Quantidade': cotas_compradas, 'Total': valor_compra},
                {'Quantidade': cotas_compradas_2, 'Total': valor_compra_2},
                {'Quantidade': cotas_compradas_3, 'Total': valor_compra_3},
                {'Quantidade': cotas_compradas_4, 'Total': valor_compra_4},
            ]
            ponto_medio = calcular_ponto_medio(compras)
            lucro_prejuizo_compradas = calcular_lucro_prejuizo(valor_compra, valor_atual, cotas_compradas)
            lucro_prejuizo_venda = calcular_lucro_prejuizo(valor_venda, valor_atual, cotas_venda)

            resultado_text = f"Valor atual do fundo {fundo}: R${valor_atual:.2f}\n"
            resultado_text += f"Ponto médio da operação: R${ponto_medio:.2f}\n"

            if lucro_prejuizo_compradas > 0:
                resultado_text += f"Lucro das cotas compradas: R${lucro_prejuizo_compradas:.2f}\n"
            elif lucro_prejuizo_compradas < 0:
                resultado_text += f"Prejuízo das cotas compradas: R${abs(lucro_prejuizo_compradas):.2f}\n"
            else:
                resultado_text += f"As cotas compradas ficaram no ponto de equilíbrio. Não houve lucro nem prejuízo.\n"

            if lucro_prejuizo_venda > 0:
                resultado_text += f"Lucro das cotas para venda: R${lucro_prejuizo_venda:.2f}\n"
            elif lucro_prejuizo_venda < 0:
                resultado_text += f"Prejuízo das cotas para venda: R${abs(lucro_prejuizo_venda):.2f}\n"
            else:
                resultado_text += f"As cotas para venda ficaram no ponto de equilíbrio. Não houve lucro nem prejuízo.\n"

            return html.Div([dcc.Markdown(resultado_text)], style={"margin-top": "20px"})

        else:
            return html.Div([html.H4(f"Fundo '{fundo}' não encontrado ou não disponível no Yahoo Finance.")])

if __name__ == "__main__":
    app.run_server(debug=True)
