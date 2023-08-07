import yfinance as yf
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

def obter_valor_atual(fundo):
    ticker = f"{fundo}.SA"
    fundo_info = yf.Ticker(ticker)

    try:
        valor_atual = fundo_info.history(period="1d")["Close"].iloc[-1]
        return valor_atual
    except:
        return None

def calcular_ponto_medio(valor_compra, valor_venda):
    return (valor_compra + valor_venda) / 2

def calcular_lucro_prejuizo(valor_compra, valor_venda, quantidade_cotas):
    return (valor_venda - valor_compra) * quantidade_cotas

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

app.layout = dbc.Container([
    html.H1("Análise de Fundos Imobiliários", className="h1"),
    dbc.Row([
        dbc.Col([
            html.Label("Código do Fundo:", className="label"),
            dcc.Input(id="input-fundo", type="text", value="", className="input-field")
        ]),
        dbc.Col([
            html.Label("Valor de Compra:", className="label"),
            dcc.Input(id="input-valor-compra", type="number", value="", className="input-field")
        ]),
        dbc.Col([
            html.Label("Valor de Venda:", className="label"),
            dcc.Input(id="input-valor-venda", type="number", value="", className="input-field")
        ]),
        dbc.Col([
            html.Label("Quantidade de Cotas:", className="label"),
            dcc.Input(id="input-quantidade-cotas", type="number", value="", className="input-field")
        ]),
        dbc.Col([
            dbc.Button("Calcular", id="calcular-button", n_clicks=0, color="primary", className="mt-4")
        ])
    ], className="col"),
    html.Div(id="resultado-container", className="resultado-container"),

    # Footer
    dbc.NavbarSimple(
        children=[
            dbc.NavItem("Desenvolvido por Rafael Barbosa | 2023", className="navbar")
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
        dash.dependencies.State("input-valor-venda", "value"),
        dash.dependencies.State("input-quantidade-cotas", "value"),
    ],
)
def calcular_e_mostrar_resultado(n_clicks, fundo, valor_compra, valor_venda, quantidade_cotas):
    if n_clicks > 0:
        valor_atual = obter_valor_atual(fundo)
        if valor_atual is not None:
            ponto_medio = calcular_ponto_medio(valor_compra, valor_venda)
            lucro_prejuizo = calcular_lucro_prejuizo(valor_compra, valor_venda, quantidade_cotas)

            resultado_text = f"Valor atual do fundo {fundo}: R${valor_atual:.2f}\n"
            resultado_text += f"Ponto médio da operação: R${ponto_medio:.2f}\n"

            if lucro_prejuizo > 0:
                resultado_text += f"Lucro da operação: R${lucro_prejuizo:.2f}\n"
            elif lucro_prejuizo < 0:
                resultado_text += f"Prejuízo da operação: R${abs(lucro_prejuizo):.2f}\n"
            else:
                resultado_text += f"A operação ficou no ponto de equilíbrio. Não houve lucro nem prejuízo."

            return html.Div([dcc.Markdown(resultado_text)], style={"margin-top": "20px"})

        else:
            return html.Div([html.H4(f"Fundo '{fundo}' não encontrado ou não disponível no Yahoo Finance.")])

if __name__ == "__main__":
    app.run_server(debug=True)
