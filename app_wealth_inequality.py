import dash
from dash import dcc, html, Input, Output, State, callback_context
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from wealth_inequality_sim import WealthInequalitySimulation, AgentStyle

# Initialize Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Wealth Inequality Emergence"

# Global simulation state (works fine for local use)
sim = None
running = False

# App layout
app.layout = html.Div([
    dcc.Interval(id='interval-component', interval=100, n_intervals=0),
    
    # Header
    html.Div([
        html.H1("Wealth Inequality Emergence", 
                style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '5px', 'fontWeight': '300', 'fontSize': '42px'}),
    ]),
    
    # Parameters panel
    html.Div([
        html.Div([
            # Column 1: Basic Setup
            html.Div([
                html.H4("Basic Setup", style={'color': '#2c3e50', 'borderBottom': '1px solid #ecf0f1', 
                                               'paddingBottom': '8px', 'marginBottom': '20px', 'fontWeight': '400'}),
                html.Label("Number of Agents", style={'fontSize': '13px', 'color': '#7f8c8d', 'display': 'block', 'marginBottom': '5px'}),
                dcc.Slider(id='n-agents', min=50, max=500, step=10, value=100,
                          marks={50: '50', 250: '250', 500: '500'},
                          tooltip={"placement": "bottom", "always_visible": True}),
                
                html.Label("Initial Wealth (Everyone Equal)", style={'marginTop': '20px', 'fontSize': '13px', 'color': '#7f8c8d', 'display': 'block', 'marginBottom': '5px'}),
                dcc.Input(id='initial-wealth', type='number', value=100, min=10, max=1000, step=10,
                         style={'width': '100%', 'padding': '8px', 'fontSize': '13px', 'border': '1px solid #dfe6e9',
                                'borderRadius': '4px', 'boxSizing': 'border-box'}),
                
                html.Label("Simulation Speed (rounds/update)", style={'marginTop': '20px', 'fontSize': '13px', 'color': '#7f8c8d', 'display': 'block', 'marginBottom': '5px'}),
                dcc.Slider(id='speed-multiplier', min=1, max=1000, step=1, value=10,
                          marks={1: '1', 250: '250', 500: '500', 1000: '1000'},
                          tooltip={"placement": "bottom", "always_visible": True}),
            ], style={'width': '32.5%', 'display': 'inline-block', 'verticalAlign': 'top', 
                      'padding': '20px', 'marginRight': '0.75%',
                      'backgroundColor': 'white', 'borderRadius': '4px', 
                      'border': '1px solid #ecf0f1',
                      'boxSizing': 'border-box', 'height': '300px'}),
            
            # Column 2: Agent Styles
            html.Div([
                html.H4("Agent Styles", style={'color': '#2c3e50', 'borderBottom': '1px solid #ecf0f1', 
                                                'paddingBottom': '8px', 'marginBottom': '20px', 'fontWeight': '400'}),
                
                html.Label("Greedy (Stakes 30%)", style={'fontSize': '13px', 'color': '#7f8c8d', 'display': 'block', 'marginBottom': '5px'}),
                dcc.Slider(id='greedy-ratio', min=0.0, max=0.7, step=0.05, value=0.33,
                          marks={0.0: '0%', 0.35: '35%', 0.7: '70%'},
                          tooltip={"placement": "bottom", "always_visible": True}),
                
                html.Label("Neutral (Stakes 20%)", style={'marginTop': '20px', 'fontSize': '13px', 'color': '#7f8c8d', 'display': 'block', 'marginBottom': '5px'}),
                dcc.Slider(id='neutral-ratio', min=0.0, max=0.7, step=0.05, value=0.33,
                          marks={0.0: '0%', 0.35: '35%', 0.7: '70%'},
                          tooltip={"placement": "bottom", "always_visible": True}),
                
                html.Label("Contrarian (Stakes 10%)", style={'marginTop': '20px', 'fontSize': '13px', 'color': '#7f8c8d', 'display': 'block', 'marginBottom': '5px'}),
                html.Div(id='contrarian-display', 
                        style={'marginTop': '8px', 'fontSize': '13px', 'color': '#2c3e50', 'fontWeight': '500'}),
            ], style={'width': '32.5%', 'display': 'inline-block', 'verticalAlign': 'top', 
                      'padding': '20px', 'marginLeft': '0.75%', 'marginRight': '0.75%',
                      'backgroundColor': 'white', 'borderRadius': '4px', 
                      'border': '1px solid #ecf0f1',
                      'boxSizing': 'border-box', 'height': '300px'}),
            
            # Column 3: Rich-Get-Richer + Redistribution
            html.Div([
                html.H4("Rich-Get-Richer Bias", style={'color': '#2c3e50', 'borderBottom': '1px solid #ecf0f1', 
                                                        'paddingBottom': '8px', 'marginBottom': '20px', 'fontWeight': '400'}),
                
                html.Label("Rich Bias (advantage)", style={'fontSize': '13px', 'color': '#7f8c8d', 'display': 'block', 'marginBottom': '5px'}),
                dcc.Slider(id='rich-bias', min=0.0, max=0.15, step=0.01, value=0.05,
                          marks={0.0: '0%', 0.05: '5%', 0.10: '10%', 0.15: '15%'},
                          tooltip={"placement": "bottom", "always_visible": True}),
                
                html.Div([
                    html.Div("Richer: 50% + bias", style={'fontSize': '12px', 'marginBottom': '4px', 'color': '#7f8c8d'}),
                    html.Div("Poorer: 50% - bias", style={'fontSize': '12px', 'color': '#7f8c8d'}),
                ], style={'marginTop': '20px', 'padding': '12px', 'backgroundColor': '#f8f9fa', 
                         'borderRadius': '4px', 'border': '1px solid #ecf0f1'}),
                
                # Redistribution options
                html.Div([
                    dcc.Checklist(id='wealth-tax-enabled', options=[{'label': ' Wealth Tax', 'value': 'enabled'}], value=[], 
                                 style={'fontSize': '12px', 'marginTop': '15px'}),
                    dcc.Checklist(id='ubi-enabled', options=[{'label': ' UBI', 'value': 'enabled'}], value=[],
                                 style={'fontSize': '12px'}),
                    dcc.Checklist(id='safety-net-enabled', options=[{'label': ' Safety Net', 'value': 'enabled'}], value=[],
                                 style={'fontSize': '12px'}),
                ]),
            ], style={'width': '32.5%', 'display': 'inline-block', 'verticalAlign': 'top', 
                      'padding': '20px', 'marginLeft': '0.75%',
                      'backgroundColor': 'white', 'borderRadius': '4px', 
                      'border': '1px solid #ecf0f1',
                      'boxSizing': 'border-box', 'height': '300px'}),
        ]),
        
        # Hidden inputs for redistribution params (simplified)
        dcc.Store(id='wealth-tax-threshold', data=0.10),
        dcc.Store(id='wealth-tax-rate', data=0.02),
        dcc.Store(id='ubi-amount', data=1.0),
        dcc.Store(id='safety-net-floor', data=10.0),
        
        # Control buttons
        html.Div([
            html.Button('Start', id='start-btn', n_clicks=0,
                       style={'width': '120px', 'padding': '10px 20px', 'fontSize': '14px', 'fontWeight': '500',
                              'backgroundColor': '#27ae60', 'color': 'white', 'border': 'none',
                              'borderRadius': '4px', 'cursor': 'pointer', 'marginRight': '10px'}),
            html.Button('Stop', id='stop-btn', n_clicks=0,
                       style={'width': '120px', 'padding': '10px 20px', 'fontSize': '14px', 'fontWeight': '500',
                              'backgroundColor': '#e74c3c', 'color': 'white', 'border': 'none',
                              'borderRadius': '4px', 'cursor': 'pointer', 'marginRight': '10px'}),
            html.Button('Reset', id='reset-btn', n_clicks=0,
                       style={'width': '120px', 'padding': '10px 20px', 'fontSize': '14px', 'fontWeight': '500',
                              'backgroundColor': '#3498db', 'color': 'white', 'border': 'none',
                              'borderRadius': '4px', 'cursor': 'pointer'}),
        ], style={'textAlign': 'center', 'marginTop': '15px'}),
        
        html.Div(id='validation-message', 
                style={'marginTop': '8px', 'color': '#e74c3c', 'textAlign': 'center', 'fontSize': '13px'}),
        
    ], style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '4px', 
              'marginBottom': '20px', 'border': '1px solid #ecf0f1'}),
    
    # Main content
    html.Div([
        # Status bar
        html.Div(id='status-bar', style={'padding': '10px', 'backgroundColor': '#3498db',
                                         'color': 'white', 'borderRadius': '4px',
                                         'marginBottom': '15px', 'fontSize': '13px',
                                         'textAlign': 'center'}),
        
        # Key metrics
        html.Div(id='key-metrics', style={'marginBottom': '15px'}),
        
        # Charts
        dcc.Graph(id='inequality-chart', style={'height': '300px'}, config={'displayModeBar': False}),
        
        html.Div([
            html.Div([dcc.Graph(id='wealth-hist', config={'displayModeBar': False})], 
                    style={'width': '48%', 'display': 'inline-block'}),
            html.Div([dcc.Graph(id='survival-chart', config={'displayModeBar': False})], 
                    style={'width': '48%', 'display': 'inline-block', 'marginLeft': '4%'}),
        ]),
        
        dcc.Graph(id='concentration-chart', style={'height': '300px'}, config={'displayModeBar': False}),
        
        # Results table
        html.Div(id='results-table', style={'marginBottom': '15px', 'marginTop': '15px'}),
        
    ], style={'padding': '0 20px'}),
])

# Callbacks
@app.callback(
    Output('contrarian-display', 'children'),
    [Input('greedy-ratio', 'value'), Input('neutral-ratio', 'value')]
)
def update_contrarian(greedy, neutral):
    return f"Contrarian Ratio: {1.0 - greedy - neutral:.2f}"

@app.callback(
    Output('validation-message', 'children'),
    [Input('start-btn', 'n_clicks'), Input('stop-btn', 'n_clicks'), Input('reset-btn', 'n_clicks')],
    [State('n-agents', 'value'), State('initial-wealth', 'value'),
     State('greedy-ratio', 'value'), State('neutral-ratio', 'value'), State('rich-bias', 'value'),
     State('wealth-tax-enabled', 'value'), State('ubi-enabled', 'value'), State('safety-net-enabled', 'value')]
)
def control_simulation(start_clicks, stop_clicks, reset_clicks,
                       n_agents, initial_wealth, greedy_ratio, neutral_ratio, rich_bias,
                       wealth_tax_enabled, ubi_enabled, safety_net_enabled):
    global sim, running
    
    ctx = callback_context
    if not ctx.triggered:
        # Initialize on first load
        sim = WealthInequalitySimulation(
            n_agents=n_agents, initial_wealth=initial_wealth,
            greedy_ratio=greedy_ratio, neutral_ratio=neutral_ratio, rich_bias=rich_bias,
            wealth_tax_enabled='enabled' in (wealth_tax_enabled or []),
            ubi_enabled='enabled' in (ubi_enabled or []),
            safety_net_enabled='enabled' in (safety_net_enabled or []),
        )
        sim.reset()
        running = False
        return ""
    
    if greedy_ratio + neutral_ratio > 1.0:
        return "Error: Greedy + Neutral ratios cannot exceed 1.0!"
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'start-btn':
        if sim is None:
            sim = WealthInequalitySimulation(
                n_agents=n_agents, initial_wealth=initial_wealth,
                greedy_ratio=greedy_ratio, neutral_ratio=neutral_ratio, rich_bias=rich_bias,
                wealth_tax_enabled='enabled' in (wealth_tax_enabled or []),
                ubi_enabled='enabled' in (ubi_enabled or []),
                safety_net_enabled='enabled' in (safety_net_enabled or []),
            )
            sim.reset()
        running = True
    elif button_id == 'stop-btn':
        running = False
    elif button_id == 'reset-btn':
        sim = WealthInequalitySimulation(
            n_agents=n_agents, initial_wealth=initial_wealth,
            greedy_ratio=greedy_ratio, neutral_ratio=neutral_ratio, rich_bias=rich_bias,
            wealth_tax_enabled='enabled' in (wealth_tax_enabled or []),
            ubi_enabled='enabled' in (ubi_enabled or []),
            safety_net_enabled='enabled' in (safety_net_enabled or []),
        )
        sim.reset()
        running = False
    
    return ""

@app.callback(
    [Output('status-bar', 'children'),
     Output('key-metrics', 'children'),
     Output('inequality-chart', 'figure'),
     Output('wealth-hist', 'figure'),
     Output('survival-chart', 'figure'),
     Output('concentration-chart', 'figure'),
     Output('results-table', 'children')],
    [Input('interval-component', 'n_intervals')],
    [State('speed-multiplier', 'value')]
)
def update_display(n_intervals, speed_multiplier):
    global sim, running
    
    if sim is None:
        return create_empty_outputs()
    
    # Run simulation steps if running
    if running:
        steps = max(1, int(speed_multiplier or 10))
        for _ in range(steps):
            if not sim.step():
                running = False
                break
            if len([a for a in sim.agents if a.active]) < 2:
                running = False
                break
    
    results = sim.get_current_results()
    return create_outputs(sim, results, running)

def create_empty_outputs():
    empty_fig = go.Figure()
    empty_fig.update_layout(title="Ready to start", font=dict(color='#7f8c8d'))
    return (
        "Not running | Click Start",
        html.Div("No data", style={'textAlign': 'center', 'color': '#7f8c8d'}),
        empty_fig, empty_fig, empty_fig, empty_fig,
        html.Div("No data", style={'textAlign': 'center', 'color': '#7f8c8d'})
    )

def create_outputs(sim, results, is_running):
    active = len([a for a in sim.agents if a.active])
    status = f"{'Running' if is_running else 'Paused'} | Round: {sim.current_round} | Active: {active} | Bankrupt: {results['bankrupt_count']}"
    
    gini = results['gini_history'][-1] if results['gini_history'] else 0
    top10 = results['top_10_percent_history'][-1] if results['top_10_percent_history'] else 0
    top1 = results['top_1_percent_history'][-1] if results['top_1_percent_history'] else 0
    
    metrics = html.Div([
        html.Div([html.Div("Gini", style={'fontSize': '11px', 'color': '#95a5a6'}),
                  html.Div(f"{gini:.3f}", style={'fontSize': '24px', 'fontWeight': '500', 'color': '#2c3e50'})],
                 style={'width': '30%', 'display': 'inline-block', 'padding': '12px', 'backgroundColor': 'white',
                        'borderRadius': '4px', 'textAlign': 'center', 'border': '1px solid #ecf0f1'}),
        html.Div([html.Div("Top 10%", style={'fontSize': '11px', 'color': '#95a5a6'}),
                  html.Div(f"{top10:.1f}%", style={'fontSize': '24px', 'fontWeight': '500', 'color': '#2c3e50'})],
                 style={'width': '30%', 'display': 'inline-block', 'padding': '12px', 'backgroundColor': 'white',
                        'borderRadius': '4px', 'textAlign': 'center', 'marginLeft': '3%', 'border': '1px solid #ecf0f1'}),
        html.Div([html.Div("Top 1%", style={'fontSize': '11px', 'color': '#95a5a6'}),
                  html.Div(f"{top1:.1f}%", style={'fontSize': '24px', 'fontWeight': '500', 'color': '#e74c3c'})],
                 style={'width': '30%', 'display': 'inline-block', 'padding': '12px', 'backgroundColor': 'white',
                        'borderRadius': '4px', 'textAlign': 'center', 'marginLeft': '3%', 'border': '1px solid #ecf0f1'}),
    ])
    
    # Gini chart
    gini_fig = go.Figure()
    gini_fig.add_trace(go.Scatter(y=results['gini_history'], mode='lines', line=dict(color='#e74c3c', width=2)))
    gini_fig.update_layout(title="Inequality Over Time", xaxis_title="Round", yaxis_title="Gini",
                          height=300, margin=dict(l=50, r=20, t=40, b=40))
    
    # Wealth histogram
    wealth_fig = go.Figure()
    if results['current_wealths']:
        wealth_fig.add_trace(go.Histogram(x=results['current_wealths'], nbinsx=40, marker=dict(color='#27ae60')))
    wealth_fig.update_layout(title="Wealth Distribution", xaxis_title="Wealth", yaxis_title="Agents",
                            height=300, margin=dict(l=50, r=20, t=40, b=40))
    
    # Survival chart
    survival_fig = go.Figure()
    survival_fig.add_trace(go.Scatter(y=results['active_count_history'], mode='lines', 
                                      fill='tozeroy', line=dict(color='#9467bd', width=2)))
    survival_fig.update_layout(title="Agent Survival", xaxis_title="Round", yaxis_title="Active",
                              height=300, margin=dict(l=50, r=20, t=40, b=40))
    
    # Concentration chart
    conc_fig = go.Figure()
    conc_fig.add_trace(go.Scatter(y=results['top_10_percent_history'], mode='lines', 
                                  name='Top 10%', line=dict(color='#f39c12', width=2)))
    conc_fig.add_trace(go.Scatter(y=results['top_1_percent_history'], mode='lines',
                                  name='Top 1%', line=dict(color='#e74c3c', width=2)))
    conc_fig.update_layout(title="Wealth Concentration", xaxis_title="Round", yaxis_title="% Wealth",
                          height=300, margin=dict(l=50, r=20, t=40, b=40), showlegend=True)
    
    # Results table
    rows = []
    for style, data in results['results_by_style'].items():
        rows.append(html.Tr([
            html.Td(style.capitalize()), html.Td(data['total']), html.Td(data['active']),
            html.Td(f"{data['survival_rate']*100:.1f}%"), html.Td(f"${data['avg_wealth']:.2f}")
        ]))
    
    table = html.Table([
        html.Thead(html.Tr([html.Th(c, style={'backgroundColor': '#3498db', 'color': 'white', 'padding': '8px'}) 
                           for c in ['Style', 'Total', 'Active', 'Survival', 'Avg Wealth']])),
        html.Tbody(rows)
    ], style={'width': '100%', 'borderCollapse': 'collapse', 'textAlign': 'center'})
    
    return status, metrics, gini_fig, wealth_fig, survival_fig, conc_fig, table

if __name__ == '__main__':
    print("Starting Wealth Inequality Simulation...")
    print("Open http://localhost:8050 in your browser")
    app.run(debug=True, host='127.0.0.1', port=8050)
