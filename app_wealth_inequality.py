import dash
from dash import dcc, html, Input, Output, State, callback_context
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from wealth_inequality_sim import WealthInequalitySimulation, AgentStyle

# Initialize Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Wealth Inequality Emergence"

# Global simulation state
sim_instance = None
sim_initialized = False

# App layout
app.layout = html.Div([
    # Store components
    dcc.Store(id='sim-state', data=None),
    dcc.Store(id='running-state', data=False),
    dcc.Interval(id='interval-component', interval=50, disabled=True),  # Faster updates (50ms)
    
    # Header
    html.Div([
        html.H1("Wealth Inequality Emergence", 
                style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '5px', 'fontWeight': '300', 'fontSize': '42px'}),
    ]),
    
    # Parameters panel
    html.Div([
        # Parameters in one row
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
            
            # Column 3: Rich-Get-Richer Bias
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
            ], style={'width': '32.5%', 'display': 'inline-block', 'verticalAlign': 'top', 
                      'padding': '20px', 'marginLeft': '0.75%',
                      'backgroundColor': 'white', 'borderRadius': '4px', 
                      'border': '1px solid #ecf0f1',
                      'boxSizing': 'border-box', 'height': '300px'}),
        ], style={'marginBottom': '20px', 'whiteSpace': 'nowrap'}),
        
        # Redistribution Policies Row
        html.Div([
            html.H3("Redistribution Policies", style={'color': '#2c3e50', 'marginBottom': '15px', 'fontSize': '18px', 'fontWeight': '400'}),
            
            # Policy Column 1: Wealth Tax
            html.Div([
                html.Div([
                    dcc.Checklist(
                        id='wealth-tax-enabled',
                        options=[{'label': ' Wealth Tax', 'value': 'enabled'}],
                        value=[],
                        style={'fontSize': '14px', 'fontWeight': '500'}
                    ),
                ], style={'marginBottom': '10px'}),
                
                html.Label("Tax Top %", style={'fontSize': '12px', 'color': '#7f8c8d', 'display': 'block', 'marginBottom': '5px'}),
                dcc.Slider(id='wealth-tax-threshold', min=0.01, max=0.50, step=0.01, value=0.10,
                          marks={0.01: '1%', 0.10: '10%', 0.25: '25%', 0.50: '50%'},
                          tooltip={"placement": "bottom", "always_visible": True}),
                
                html.Label("Tax Rate", style={'marginTop': '10px', 'fontSize': '12px', 'color': '#7f8c8d', 'display': 'block', 'marginBottom': '5px'}),
                dcc.Slider(id='wealth-tax-rate', min=0.001, max=0.10, step=0.001, value=0.02,
                          marks={0.001: '0.1%', 0.02: '2%', 0.05: '5%', 0.10: '10%'},
                          tooltip={"placement": "bottom", "always_visible": True}),
            ], style={'width': '32%', 'display': 'inline-block', 'verticalAlign': 'top', 
                      'padding': '15px', 'marginRight': '2%',
                      'backgroundColor': 'white', 'borderRadius': '4px', 
                      'border': '1px solid #ecf0f1', 'boxSizing': 'border-box'}),
            
            # Policy Column 2: UBI
            html.Div([
                html.Div([
                    dcc.Checklist(
                        id='ubi-enabled',
                        options=[{'label': ' Universal Basic Income', 'value': 'enabled'}],
                        value=[],
                        style={'fontSize': '14px', 'fontWeight': '500'}
                    ),
                ], style={'marginBottom': '10px'}),
                
                html.Label("UBI Amount (per agent/round)", style={'fontSize': '12px', 'color': '#7f8c8d', 'display': 'block', 'marginBottom': '5px'}),
                dcc.Slider(id='ubi-amount', min=0.1, max=10.0, step=0.1, value=1.0,
                          marks={0.1: '0.1', 2.5: '2.5', 5: '5', 10: '10'},
                          tooltip={"placement": "bottom", "always_visible": True}),
            ], style={'width': '32%', 'display': 'inline-block', 'verticalAlign': 'top', 
                      'padding': '15px', 'marginRight': '2%',
                      'backgroundColor': 'white', 'borderRadius': '4px', 
                      'border': '1px solid #ecf0f1', 'boxSizing': 'border-box'}),
            
            # Policy Column 3: Safety Net
            html.Div([
                html.Div([
                    dcc.Checklist(
                        id='safety-net-enabled',
                        options=[{'label': ' Safety Net', 'value': 'enabled'}],
                        value=[],
                        style={'fontSize': '14px', 'fontWeight': '500'}
                    ),
                ], style={'marginBottom': '10px'}),
                
                html.Label("Minimum Wealth Floor", style={'fontSize': '12px', 'color': '#7f8c8d', 'display': 'block', 'marginBottom': '5px'}),
                dcc.Slider(id='safety-net-floor', min=1, max=50, step=1, value=10,
                          marks={1: '1', 10: '10', 25: '25', 50: '50'},
                          tooltip={"placement": "bottom", "always_visible": True}),
            ], style={'width': '32%', 'display': 'inline-block', 'verticalAlign': 'top', 
                      'padding': '15px',
                      'backgroundColor': 'white', 'borderRadius': '4px', 
                      'border': '1px solid #ecf0f1', 'boxSizing': 'border-box'}),
        ], style={'marginBottom': '20px'}),
        
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
                              'backgroundColor': '#95a5a6', 'color': 'white', 'border': 'none',
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
        
        # Inequality metrics
        dcc.Graph(id='inequality-chart', style={'height': '300px'}, config={'displayModeBar': False}),
        
        # Wealth distribution
        html.Div([
            html.Div([dcc.Graph(id='wealth-hist', config={'displayModeBar': False})], 
                    style={'width': '48%', 'display': 'inline-block'}),
            html.Div([dcc.Graph(id='survival-chart', config={'displayModeBar': False})], 
                    style={'width': '48%', 'display': 'inline-block', 'marginLeft': '4%'}),
        ]),
        
        # Concentration metrics
        dcc.Graph(id='concentration-chart', style={'height': '300px'}, config={'displayModeBar': False}),
        
        # Results table
        html.Div(id='results-table', style={'marginBottom': '15px', 'marginTop': '15px'}),
        
    ], style={'padding': '0 20px'}),
])

# Callbacks
@app.callback(
    Output('contrarian-display', 'children'),
    [Input('greedy-ratio', 'value'),
     Input('neutral-ratio', 'value')]
)
def update_contrarian(greedy, neutral):
    contrarian = 1.0 - greedy - neutral
    return f"Contrarian Ratio: {contrarian:.2f}"

@app.callback(
    [Output('sim-state', 'data'),
     Output('running-state', 'data'),
     Output('interval-component', 'disabled'),
     Output('validation-message', 'children'),
     Output('start-btn', 'disabled'),
     Output('stop-btn', 'disabled'),
     Output('start-btn', 'style'),
     Output('stop-btn', 'style')],
    [Input('start-btn', 'n_clicks'),
     Input('stop-btn', 'n_clicks'),
     Input('reset-btn', 'n_clicks')],
    [State('n-agents', 'value'),
     State('initial-wealth', 'value'),
     State('greedy-ratio', 'value'),
     State('neutral-ratio', 'value'),
     State('rich-bias', 'value'),
     State('speed-multiplier', 'value'),
     State('wealth-tax-enabled', 'value'),
     State('wealth-tax-threshold', 'value'),
     State('wealth-tax-rate', 'value'),
     State('ubi-enabled', 'value'),
     State('ubi-amount', 'value'),
     State('safety-net-enabled', 'value'),
     State('safety-net-floor', 'value'),
     State('sim-state', 'data'),
     State('running-state', 'data')]
)
def control_simulation(start_clicks, stop_clicks, reset_clicks,
                       n_agents, initial_wealth, greedy_ratio, neutral_ratio,
                       rich_bias, speed_multiplier,
                       wealth_tax_enabled, wealth_tax_threshold, wealth_tax_rate,
                       ubi_enabled, ubi_amount,
                       safety_net_enabled, safety_net_floor,
                       sim_data, is_running):
    global sim_instance, sim_initialized
    
    # Define button styles
    start_enabled_style = {
        'width': '120px', 'padding': '10px 20px', 'fontSize': '14px', 'fontWeight': '500',
        'backgroundColor': '#27ae60', 'color': 'white', 'border': 'none',
        'borderRadius': '4px', 'cursor': 'pointer', 'marginRight': '10px'
    }
    start_disabled_style = {
        'width': '120px', 'padding': '10px 20px', 'fontSize': '14px', 'fontWeight': '500',
        'backgroundColor': '#1e7e34', 'color': '#cccccc', 'border': 'none',
        'borderRadius': '4px', 'cursor': 'not-allowed', 'marginRight': '10px', 'opacity': '0.7'
    }
    stop_enabled_style = {
        'width': '120px', 'padding': '10px 20px', 'fontSize': '14px', 'fontWeight': '500',
        'backgroundColor': '#e74c3c', 'color': 'white', 'border': 'none',
        'borderRadius': '4px', 'cursor': 'pointer', 'marginRight': '10px'
    }
    stop_disabled_style = {
        'width': '120px', 'padding': '10px 20px', 'fontSize': '14px', 'fontWeight': '500',
        'backgroundColor': '#95a5a6', 'color': '#cccccc', 'border': 'none',
        'borderRadius': '4px', 'cursor': 'not-allowed', 'marginRight': '10px', 'opacity': '0.6'
    }
    
    ctx = callback_context
    if not ctx.triggered:
        if greedy_ratio + neutral_ratio > 1.0:
            return (None, False, True, "Error: Greedy + Neutral ratios cannot exceed 1.0!", 
                    False, True, start_enabled_style, stop_disabled_style)
        
        sim_data = {
            'params': {
                'n_agents': n_agents, 'initial_wealth': initial_wealth,
                'greedy_ratio': greedy_ratio, 'neutral_ratio': neutral_ratio,
                'rich_bias': rich_bias,
                'wealth_tax_enabled': 'enabled' in (wealth_tax_enabled or []),
                'wealth_tax_threshold': wealth_tax_threshold,
                'wealth_tax_rate': wealth_tax_rate,
                'ubi_enabled': 'enabled' in (ubi_enabled or []),
                'ubi_amount': ubi_amount,
                'safety_net_enabled': 'enabled' in (safety_net_enabled or []),
                'safety_net_floor': safety_net_floor,
            },
            'initialized': True
        }
        sim_initialized = False
        return (sim_data, False, True, "", False, True, start_enabled_style, stop_disabled_style)
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'start-btn':
        if greedy_ratio + neutral_ratio > 1.0:
            return (sim_data, False, True, "Error: Greedy + Neutral ratios cannot exceed 1.0!", 
                    False, True, start_enabled_style, stop_disabled_style)
        
        if sim_data is None:
            sim_data = {
                'params': {
                    'n_agents': n_agents, 'initial_wealth': initial_wealth,
                    'greedy_ratio': greedy_ratio, 'neutral_ratio': neutral_ratio,
                    'rich_bias': rich_bias,
                    'wealth_tax_enabled': 'enabled' in (wealth_tax_enabled or []),
                    'wealth_tax_threshold': wealth_tax_threshold,
                    'wealth_tax_rate': wealth_tax_rate,
                    'ubi_enabled': 'enabled' in (ubi_enabled or []),
                    'ubi_amount': ubi_amount,
                    'safety_net_enabled': 'enabled' in (safety_net_enabled or []),
                    'safety_net_floor': safety_net_floor,
                },
                'initialized': True
            }
            sim_initialized = False
        
        # Start simulation: disable Start (dark green), enable Stop (red)
        return (sim_data, True, False, "", True, False, start_disabled_style, stop_enabled_style)
    
    elif button_id == 'stop-btn':
        # Stop simulation: enable Start (green), disable Stop (gray)
        return (sim_data, False, True, "", False, True, start_enabled_style, stop_disabled_style)
    
    elif button_id == 'reset-btn':
        sim_data = {
            'params': {
                'n_agents': n_agents, 'initial_wealth': initial_wealth,
                'greedy_ratio': greedy_ratio, 'neutral_ratio': neutral_ratio,
                'rich_bias': rich_bias,
                'wealth_tax_enabled': 'enabled' in (wealth_tax_enabled or []),
                'wealth_tax_threshold': wealth_tax_threshold,
                'wealth_tax_rate': wealth_tax_rate,
                'ubi_enabled': 'enabled' in (ubi_enabled or []),
                'ubi_amount': ubi_amount,
                'safety_net_enabled': 'enabled' in (safety_net_enabled or []),
                'safety_net_floor': safety_net_floor,
            },
            'initialized': True
        }
        sim_instance = None
        sim_initialized = False
        # Reset: enable Start (green), disable Stop (gray)
        return (sim_data, False, True, "", False, True, start_enabled_style, stop_disabled_style)
    
    # Default: based on current running state
    if is_running:
        return (sim_data, True, False, "", True, False, start_disabled_style, stop_enabled_style)
    else:
        return (sim_data, False, True, "", False, True, start_enabled_style, stop_disabled_style)

@app.callback(
    [Output('status-bar', 'children'),
     Output('key-metrics', 'children'),
     Output('inequality-chart', 'figure'),
     Output('wealth-hist', 'figure'),
     Output('survival-chart', 'figure'),
     Output('concentration-chart', 'figure'),
     Output('results-table', 'children'),
     Output('interval-component', 'interval')],
    [Input('interval-component', 'n_intervals'),
     Input('sim-state', 'data'),
     Input('running-state', 'data')],
    [State('speed-multiplier', 'value')]
)
def update_charts(n_intervals, sim_data, is_running, speed_multiplier):
    global sim_instance, sim_initialized
    
    try:
        # Initialize simulation if needed
        if sim_data is not None and (sim_instance is None or not sim_initialized):
            params = sim_data['params']
            sim_instance = WealthInequalitySimulation(
                n_agents=params['n_agents'],
                initial_wealth=params['initial_wealth'],
                greedy_ratio=params['greedy_ratio'],
                neutral_ratio=params['neutral_ratio'],
                rich_bias=params['rich_bias'],
                wealth_tax_enabled=params.get('wealth_tax_enabled', False),
                wealth_tax_threshold=params.get('wealth_tax_threshold', 0.10),
                wealth_tax_rate=params.get('wealth_tax_rate', 0.02),
                ubi_enabled=params.get('ubi_enabled', False),
                ubi_amount=params.get('ubi_amount', 1.0),
                safety_net_enabled=params.get('safety_net_enabled', False),
                safety_net_floor=params.get('safety_net_floor', 10.0),
            )
            sim_instance.reset()
            sim_initialized = True
        
        if sim_instance is None:
            return create_empty_outputs()
        
        # Run simulation step if running
        if is_running and n_intervals is not None and n_intervals > 0:
            # Run multiple steps based on speed multiplier
            if speed_multiplier is None:
                speed_multiplier = 1
            
            # Cap speed multiplier to prevent UI freezing - keep UI responsive
            # Max 100 steps per callback for smooth updates
            max_steps = min(int(speed_multiplier), 100)
            
            for _ in range(max_steps):
                can_continue = sim_instance.step()
                if not can_continue:
                    break
                
                # Safety check: if only a few agents left, slow down
                active_count = len([a for a in sim_instance.agents if a.active])
                if active_count < 2:
                    break
        
        # Get current results
        results = sim_instance.get_current_results()
        
        # Create all outputs
        return create_all_outputs(sim_instance, results, is_running)
    
    except Exception as e:
        # Log error and reset simulation to recover
        print(f"Error in update_charts: {e}")
        import traceback
        traceback.print_exc()
        sim_instance = None
        sim_initialized = False
        return create_empty_outputs()

def create_empty_outputs():
    empty_fig = go.Figure()
    empty_fig.update_layout(
        title="Ready to start simulation",
        font=dict(size=14, color='#7f8c8d')
    )
    
    return (
        "Not running | Configure parameters and click Start",
        html.Div("No data yet", style={'textAlign': 'center', 'color': '#7f8c8d'}),
        empty_fig, empty_fig, empty_fig, empty_fig,
        html.Div("No data yet", style={'textAlign': 'center', 'color': '#7f8c8d'}),
        50
    )

def create_all_outputs(sim, results, is_running):
    # Downsample history data for performance if too many data points
    max_points = 500  # Maximum points to display in charts
    
    def downsample_data(data_list):
        """Downsample data to max_points for chart performance"""
        if len(data_list) <= max_points:
            return data_list
        # Take every nth point to reduce to max_points
        step = len(data_list) // max_points
        return data_list[::step]
    
    # Status bar
    active_count = len([a for a in sim.agents if a.active])
    
    # Build status message with redistribution info
    status_parts = [f"{'Running' if is_running else 'Paused'} | Round: {sim.current_round} | Active: {active_count} agents | Bankrupt: {results['bankrupt_count']} (< ${sim.min_wealth})"]
    
    policies_active = []
    if sim.wealth_tax_enabled:
        policies_active.append("Wealth Tax")
    if sim.ubi_enabled:
        policies_active.append("UBI")
    if sim.safety_net_enabled:
        policies_active.append("Safety Net")
    
    if policies_active:
        status_parts.append(f"Policies: {', '.join(policies_active)}")
    
    status = " | ".join(status_parts)
    
    # Key metrics
    final_gini = results['gini_history'][-1] if results['gini_history'] else 0
    top_10 = results['top_10_percent_history'][-1] if results['top_10_percent_history'] else 0
    top_1 = results['top_1_percent_history'][-1] if results['top_1_percent_history'] else 0
    
    # Build metrics with redistribution stats
    metric_boxes = [
        html.Div([
            html.Div("Gini", style={'fontSize': '11px', 'color': '#95a5a6', 'marginBottom': '4px'}),
            html.Div(f"{final_gini:.3f}", style={'fontSize': '24px', 'fontWeight': '500', 'color': '#2c3e50'}),
        ], style={'width': '23%', 'display': 'inline-block', 'padding': '12px',
                 'backgroundColor': 'white', 'borderRadius': '4px', 'textAlign': 'center',
                 'border': '1px solid #ecf0f1', 'boxSizing': 'border-box', 'verticalAlign': 'top'}),
        
        html.Div([
            html.Div("Top 10%", style={'fontSize': '11px', 'color': '#95a5a6', 'marginBottom': '4px'}),
            html.Div(f"{top_10:.1f}%", style={'fontSize': '24px', 'fontWeight': '500', 'color': '#2c3e50'}),
        ], style={'width': '23%', 'display': 'inline-block', 'padding': '12px',
                 'backgroundColor': 'white', 'borderRadius': '4px', 'textAlign': 'center',
                 'marginLeft': '2%', 'border': '1px solid #ecf0f1', 'boxSizing': 'border-box', 'verticalAlign': 'top'}),
        
        html.Div([
            html.Div("Top 1%", style={'fontSize': '11px', 'color': '#95a5a6', 'marginBottom': '4px'}),
            html.Div(f"{top_1:.1f}%", style={'fontSize': '24px', 'fontWeight': '500', 'color': '#e74c3c'}),
        ], style={'width': '23%', 'display': 'inline-block', 'padding': '12px',
                 'backgroundColor': 'white', 'borderRadius': '4px', 'textAlign': 'center',
                 'marginLeft': '2%', 'border': '1px solid #ecf0f1', 'boxSizing': 'border-box', 'verticalAlign': 'top'}),
    ]
    
    # Add redistribution metric if any policy is active
    if sim.wealth_tax_enabled or sim.ubi_enabled or sim.safety_net_enabled:
        redist_text = []
        if sim.wealth_tax_enabled:
            redist_text.append(f"Tax: ${results['total_taxes_collected']:.1f}")
        if sim.ubi_enabled:
            redist_text.append(f"UBI: ${results['total_ubi_distributed']:.1f}")
        if sim.safety_net_enabled:
            redist_text.append(f"Safety: {results['safety_net_interventions']}")
        
        metric_boxes.append(
            html.Div([
                html.Div("Redistribution", style={'fontSize': '11px', 'color': '#95a5a6', 'marginBottom': '4px'}),
                html.Div([
                    html.Div(line, style={'fontSize': '10px', 'color': '#2c3e50'}) for line in redist_text
                ]),
            ], style={'width': '23%', 'display': 'inline-block', 'padding': '12px',
                     'backgroundColor': '#e8f5e9', 'borderRadius': '4px', 'textAlign': 'center',
                     'marginLeft': '2%', 'border': '1px solid #27ae60', 'boxSizing': 'border-box', 'verticalAlign': 'top'})
        )
    
    metrics = html.Div(metric_boxes)
    
    # Inequality evolution chart (single plot) - DOWNSAMPLED
    inequality_fig = go.Figure()
    gini_data = downsample_data(results['gini_history'])
    inequality_fig.add_trace(
        go.Scatter(y=gini_data, mode='lines',
                  line=dict(color='#e74c3c', width=2), name='Gini Coefficient')
    )
    inequality_fig.update_layout(
        title={'text': "Inequality Over Time", 'font': {'size': 14}},
        xaxis_title="Round",
        yaxis_title="Gini",
        height=300,
        showlegend=False,
        margin=dict(l=50, r=20, t=40, b=40),
        uirevision='constant'  # Prevent unnecessary replotting
    )
    
    # Wealth histogram
    wealth_fig = go.Figure()
    if len(results['current_wealths']) > 0:
        wealth_fig.add_trace(go.Histogram(
            x=results['current_wealths'], nbinsx=40,
            marker=dict(color='#27ae60')
        ))
    wealth_fig.update_layout(
        title={'text': "Wealth Distribution", 'font': {'size': 14}},
        xaxis_title="Wealth", yaxis_title="Agents",
        height=300,
        margin=dict(l=50, r=20, t=40, b=40),
        uirevision='constant'
    )
    
    # Survival chart - DOWNSAMPLED
    survival_fig = go.Figure()
    survival_data = downsample_data(results['active_count_history'])
    survival_fig.add_trace(go.Scatter(
        y=survival_data, mode='lines',
        fill='tozeroy', line=dict(color='#9467bd', width=2)
    ))
    survival_fig.update_layout(
        title={'text': "Agent Survival", 'font': {'size': 14}},
        xaxis_title="Round", yaxis_title="Active",
        height=300,
        margin=dict(l=50, r=20, t=40, b=40),
        uirevision='constant'
    )
    
    # Wealth concentration chart - DOWNSAMPLED
    concentration_fig = go.Figure()
    top_10_data = downsample_data(results['top_10_percent_history'])
    top_1_data = downsample_data(results['top_1_percent_history'])
    
    concentration_fig.add_trace(go.Scatter(
        y=top_10_data, mode='lines',
        name='Top 10%', line=dict(color='#f39c12', width=2)
    ))
    concentration_fig.add_trace(go.Scatter(
        y=top_1_data, mode='lines',
        name='Top 1%', line=dict(color='#e74c3c', width=2)
    ))
    concentration_fig.update_layout(
        title={'text': "Wealth Concentration", 'font': {'size': 14}},
        xaxis_title="Round", yaxis_title="% Wealth",
        height=300, showlegend=True,
        margin=dict(l=50, r=20, t=40, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        uirevision='constant'
    )
    
    # Results table
    type_data = []
    for style, data in results['results_by_style'].items():
        type_data.append({
            'Style': style.capitalize(),
            'Initial Count': data['total'],
            'Active': data['active'],
            'Bankruptcies': data['total'] - data['active'],
            'Survival Rate': f"{data['survival_rate']*100:.1f}%",
            'Avg Wealth': f"${data['avg_wealth']:.2f}"
        })
    
    df = pd.DataFrame(type_data)
    table = html.Table([
        html.Thead(
            html.Tr([html.Th(col, style={'backgroundColor': '#3498db', 'color': 'white', 
                                         'padding': '8px', 'fontSize': '12px', 'fontWeight': '500'}) 
                    for col in df.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col], style={'padding': '8px', 'fontSize': '12px', 'border': '1px solid #ecf0f1'}) 
                for col in df.columns
            ], style={'backgroundColor': '#f8f9fa' if i % 2 == 0 else 'white'}) 
            for i in range(len(df))
        ])
    ], style={'width': '100%', 'borderCollapse': 'collapse', 'border': '1px solid #ecf0f1',
              'textAlign': 'center', 'borderRadius': '4px'})
    
    return (status, metrics, inequality_fig, wealth_fig, survival_fig, 
            concentration_fig, table, 50)  # Return 50ms for responsive updates

if __name__ == '__main__':
    import os
    # Use PORT environment variable for deployment (Render, Railway, Heroku)
    port = int(os.environ.get('PORT', 8050))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    # Run with proper callback support
    app.run(debug=debug, host='0.0.0.0', port=port, use_reloader=False, threaded=True)

# Expose server for production WSGI servers
server = app.server

