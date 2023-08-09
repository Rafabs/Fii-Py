import yfinance as yf
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd

cor_titulo = {"font-size": "40px", "text-align": "center", "color": "#007bff"}
cor_selecao_fundo = {"font-size": "20px", "text-align": "center", "color": "#acacac"}
cor_valor_compra = {"font-size": "16px", "color": "#00ff04"}
cor_cota_compra = {"font-size": "16px", "color": "#00ff60"}
cor_valor_venda = {"font-size": "16px", "color": "#001aff"}
cor_cota_venda = {"font-size": "16px", "color": "#001aaa"}
footer = {"width": "100%", "text-align": "center"} 

def obter_valor_atual(fundo):
    ticker = f"{fundo}.SA"
    fundo_info = yf.Ticker(ticker)

    try:
        valor_atual = fundo_info.history(period="1d")["Close"].iloc[-1]
        return valor_atual
    except:
        return None

def calcular_ponto_medio(compras):
    total_valor_quantidade = sum(compra['Total'] * compra['Quantidade'] for compra in compras)
    total_quantidade = sum(compra['Quantidade'] for compra in compras)
    return total_valor_quantidade / total_quantidade

def calcular_lucro_prejuizo(valor_compra, valor_venda, quantidade_cotas):
    return (valor_venda - valor_compra) * quantidade_cotas

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG, "style.css"])

csv_file_path = "fundosListados.csv"
fund_options_df = pd.read_csv(csv_file_path, delimiter=";", usecols=["Código"], encoding="ISO-8859-1")
fund_options_df.rename(columns={"Código": "value"}, inplace=True)
fund_options = fund_options_df["value"].tolist()

app.layout = dbc.Container([
    html.H1("Análise de Fundos Imobiliários", style = cor_titulo),
    dbc.Row([
        dbc.Col([
            html.Label("Selecione o Fundo:", className="label", style = cor_selecao_fundo),
            dcc.Dropdown(id="input-fundo", options=[{"label": fundo, "value": fundo} for fundo in fund_options], value="", className="input-field")
        ]),
    ]),
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("Compra 1 (R$)", style = cor_valor_compra),
                    dcc.Input(id="input-valor-compra", type="number", value="", className="input-field") 
                ]),
                dbc.Col([
                    html.Label("Qtd. Cotas", style = cor_cota_compra),
                    dcc.Input(id="input-cotas-compradas", type="number", value="", className="input-field")
                ]),        
            ]),
            dbc.Row([
                dbc.Col([
                    html.Label("Compra 2 (R$)", style = cor_valor_compra),
                    dcc.Input(id="input-valor-compra-2", type="number", value="", className="input-field")
                ]),
                dbc.Col([
                    html.Label("Qtd. Cotas", style = cor_cota_compra),
                    dcc.Input(id="input-cotas-compradas-2", type="number", value="", className="input-field")
                ]),        
            ]),
            dbc.Row([
                dbc.Col([
                    html.Label("Compra 3 (R$)", style = cor_valor_compra),
                    dcc.Input(id="input-valor-compra-3", type="number", value="", className="input-field")
                ]),
                dbc.Col([
                    html.Label("Qtd. Cotas", style = cor_cota_compra),
                    dcc.Input(id="input-cotas-compradas-3", type="number", value="", className="input-field")
                ]),        
            ]),
            dbc.Row([
                dbc.Col([
                    html.Label("Compra 4 (R$)", style = cor_valor_compra),
                    dcc.Input(id="input-valor-compra-4", type="number", value="", className="input-field")
                ]),
                dbc.Col([
                    html.Label("Qtd. Cotas", style = cor_cota_compra),
                    dcc.Input(id="input-cotas-compradas-4", type="number", value="", className="input-field")
                ]),        
            ]),
            dbc.Row([
                dbc.Col([
                    html.Label("Compra 5 (R$)", style = cor_valor_compra),
                    dcc.Input(id="input-valor-compra-5", type="number", value="", className="input-field")
                ]),
                dbc.Col([
                    html.Label("Qtd. Cotas", style = cor_cota_compra),
                    dcc.Input(id="input-cotas-compradas-5", type="number", value="", className="input-field")
                ]),        
            ]),
            dbc.Row([
                dbc.Col([
                    html.Label("Compra 6 (R$)", style = cor_valor_compra),
                    dcc.Input(id="input-valor-compra-6", type="number", value="", className="input-field")
                ]),
                dbc.Col([
                    html.Label("Qtd. Cotas", style = cor_cota_compra),
                    dcc.Input(id="input-cotas-compradas-6", type="number", value="", className="input-field")
                ]),        
            ]),                        
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Label(f"Ponto Médio - (PM) = (Qtd_Cota1 * Valor_Cota1 + Qtd_Cota2 * Valor_Cota2 + ... / Qtd_Cota1 + Qtd_Cota2 + ...)\n", className="label_compra"),
                    ]),  
                ]),
            ]),          
        ]),
        className="mt-3"
    ),
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("Valor de Venda:", style = cor_valor_venda),
                    dcc.Input(id="input-valor-venda", type="number", value="", className="input-field")
                ]),
                dbc.Col([
                    html.Label("Cotas Venda:", style = cor_cota_venda),
                    dcc.Input(id="input-cotas-venda", type="number", value="", className="input-field")
                ]),
            ]),
            html.Br(),
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
            dbc.NavItem("Desenvolvido por Rafael Barbosa | 2023", style = footer)], 
fluid=True)
])

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
        dash.dependencies.State("input-valor-compra-5", "value"),
        dash.dependencies.State("input-cotas-compradas-5", "value"),
        dash.dependencies.State("input-valor-compra-6", "value"),
        dash.dependencies.State("input-cotas-compradas-6", "value"),                
        dash.dependencies.State("input-valor-venda", "value"),
        dash.dependencies.State("input-cotas-venda", "value"),
    ],
)
def calcular_e_mostrar_resultado(n_clicks, fundo, valor_compra, cotas_compradas, valor_compra_2, cotas_compradas_2, valor_compra_3, cotas_compradas_3, valor_compra_4, cotas_compradas_4, valor_compra_5, cotas_compradas_5, valor_compra_6, cotas_compradas_6, valor_venda, cotas_venda):
    if n_clicks > 0:
        valor_compra = float(valor_compra) if valor_compra else 0
        cotas_compradas = float(cotas_compradas) if cotas_compradas else 0
        valor_compra_2 = float(valor_compra_2) if valor_compra_2 else 0
        cotas_compradas_2 = float(cotas_compradas_2) if cotas_compradas_2 else 0
        valor_compra_3 = float(valor_compra_3) if valor_compra_3 else 0
        cotas_compradas_3 = float(cotas_compradas_3) if cotas_compradas_3 else 0
        valor_compra_4 = float(valor_compra_4) if valor_compra_4 else 0
        cotas_compradas_4 = float(cotas_compradas_4) if cotas_compradas_4 else 0
        valor_compra_5 = float(valor_compra_5) if valor_compra_5 else 0
        cotas_compradas_5 = float(cotas_compradas_5) if cotas_compradas_5 else 0
        valor_compra_6 = float(valor_compra_6) if valor_compra_6 else 0
        cotas_compradas_6 = float(cotas_compradas_6) if cotas_compradas_6 else 0                
        valor_venda = float(valor_venda) if valor_venda else 0
        cotas_venda = float(cotas_venda) if cotas_venda else 0
        
        valor_atual = obter_valor_atual(fundo)
        if valor_atual is not None:
            compras = [
                {'Quantidade': cotas_compradas, 'Total': valor_compra},
                {'Quantidade': cotas_compradas_2, 'Total': valor_compra_2},
                {'Quantidade': cotas_compradas_3, 'Total': valor_compra_3},
                {'Quantidade': cotas_compradas_4, 'Total': valor_compra_4},
                {'Quantidade': cotas_compradas_5, 'Total': valor_compra_5},
                {'Quantidade': cotas_compradas_6, 'Total': valor_compra_6},
            ]
            ponto_medio = calcular_ponto_medio(compras)
            lucro_prejuizo_compradas = calcular_lucro_prejuizo(valor_compra, valor_atual, cotas_compradas)
            lucro_prejuizo_venda = calcular_lucro_prejuizo(valor_venda, valor_atual, cotas_venda)

            resultado_text = f"Valor atual do fundo {fundo}: R${valor_atual:.2f}  \n" 
            resultado_text += f"Ponto médio da operação: R${ponto_medio:.2f}  \n"

            if lucro_prejuizo_compradas > 0:
                resultado_text += f"Lucro das cotas compradas: R${lucro_prejuizo_compradas:.2f}  \n"
            elif lucro_prejuizo_compradas < 0:
                resultado_text += f"Prejuízo das cotas compradas: R${abs(lucro_prejuizo_compradas):.2f}  \n"
            else:
                resultado_text += f"As cotas compradas ficaram no ponto de equilíbrio. Não houve lucro nem prejuízo.  \n"

            if lucro_prejuizo_venda > 0:
                resultado_text += f"Lucro das cotas para venda: R${lucro_prejuizo_venda:.2f}  \n"
            elif lucro_prejuizo_venda < 0:
                resultado_text += f"Prejuízo das cotas para venda: R${abs(lucro_prejuizo_venda):.2f}  \n"
            else:
                resultado_text += f"As cotas para venda ficaram no ponto de equilíbrio. Não houve lucro nem prejuízo.  \n"

            return html.Div([dcc.Markdown(resultado_text)], style={"margin-top": "20px"})

        else:
            return html.Div([html.H4(f"Fundo '{fundo}' não encontrado ou não disponível no Yahoo Finance.")])

def run_server(self,
               port=8050,
               debug=True,
               threaded=True,
               **flask_run_options):
    self.server.run(port=port, debug=debug, **flask_run_options)

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)