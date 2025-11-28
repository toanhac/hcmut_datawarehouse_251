"""
Interactive Dashboard for Bank Customer Churn Analysis
Uses Plotly Dash for web-based interactive visualizations
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Dash and Plotly imports
try:
    import dash
    from dash import dcc, html, Input, Output
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
except ImportError:
    print("Error: Dash and Plotly are required for the dashboard.")
    print("Install with: pip install dash plotly")
    sys.exit(1)

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.config import (
    CLEAN_CHURN_FILE,
    FACT_CUSTOMER_STATUS_FILE,
    DIM_CUSTOMER_FILE,
    DIM_GEO_FILE,
    DIM_SEGMENT_FILE
)


class ChurnDashboard:
    """Interactive dashboard for churn analysis"""
    
    def __init__(self):
        """Initialize the dashboard"""
        self.app = dash.Dash(__name__, suppress_callback_exceptions=True)
        self.load_data()
        self.setup_layout()
        self.setup_callbacks()
    
    def load_data(self):
        """Load all required data"""
        print("Loading data for dashboard...")
        
        # Load cleaned data
        if CLEAN_CHURN_FILE.exists():
            self.df = pd.read_csv(CLEAN_CHURN_FILE)
            print(f"✓ Loaded cleaned data: {len(self.df)} records")
        else:
            print(f"Warning: {CLEAN_CHURN_FILE} not found. Run preprocessing first.")
            self.df = None
        
        # Load DWH tables if available
        if FACT_CUSTOMER_STATUS_FILE.exists():
            self.fact = pd.read_csv(FACT_CUSTOMER_STATUS_FILE)
            self.dim_customer = pd.read_csv(DIM_CUSTOMER_FILE)
            self.dim_geo = pd.read_csv(DIM_GEO_FILE)
            self.dim_segment = pd.read_csv(DIM_SEGMENT_FILE)
            
            # Join for analysis
            self.dwh_data = self.fact.merge(self.dim_geo, on='geo_key') \
                                       .merge(self.dim_segment, on='segment_key') \
                                       .merge(self.dim_customer, on='customer_key')
            print(f"✓ Loaded DWH data: {len(self.fact)} records")
        else:
            self.dwh_data = None
    
    def setup_layout(self):
        """Setup dashboard layout"""
        
        self.app.layout = html.Div([
            # Header
            html.Div([
                html.H1("🏦 Bank Customer Churn Analytics Dashboard",
                       style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 10}),
                html.P("Data Warehouse & Decision Support System",
                      style={'textAlign': 'center', 'color': '#7f8c8d', 'fontSize': 18})
            ], style={'backgroundColor': '#ecf0f1', 'padding': '20px', 'marginBottom': '20px'}),
            
            # KPI Cards
            html.Div([
                html.Div([
                    html.Div([
                        html.H3("Total Customers", style={'color': '#3498db'}),
                        html.H2(id='kpi-total-customers', style={'color': '#2c3e50'})
                    ], className='kpi-card', style=self.card_style('#3498db'))
                ], style={'width': '24%', 'display': 'inline-block', 'margin': '0.5%'}),
                
                html.Div([
                    html.Div([
                        html.H3("Churned", style={'color': '#e74c3c'}),
                        html.H2(id='kpi-churned', style={'color': '#2c3e50'})
                    ], className='kpi-card', style=self.card_style('#e74c3c'))
                ], style={'width': '24%', 'display': 'inline-block', 'margin': '0.5%'}),
                
                html.Div([
                    html.Div([
                        html.H3("Churn Rate", style={'color': '#f39c12'}),
                        html.H2(id='kpi-churn-rate', style={'color': '#2c3e50'})
                    ], className='kpi-card', style=self.card_style('#f39c12'))
                ], style={'width': '24%', 'display': 'inline-block', 'margin': '0.5%'}),
                
                html.Div([
                    html.Div([
                        html.H3("Avg Balance", style={'color': '#2ecc71'}),
                        html.H2(id='kpi-avg-balance', style={'color': '#2c3e50'})
                    ], className='kpi-card', style=self.card_style('#2ecc71'))
                ], style={'width': '24%', 'display': 'inline-block', 'margin': '0.5%'}),
            ], style={'marginBottom': '20px'}),
            
            # Filters
            html.Div([
                html.Div([
                    html.Label("Select Country:", style={'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='filter-country',
                        options=[{'label': 'All', 'value': 'All'}],
                        value='All',
                        style={'width': '100%'}
                    )
                ], style={'width': '32%', 'display': 'inline-block', 'margin': '0.5%'}),
                
                html.Div([
                    html.Label("Select Age Group:", style={'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='filter-age-group',
                        options=[{'label': 'All', 'value': 'All'}],
                        value='All',
                        style={'width': '100%'}
                    )
                ], style={'width': '32%', 'display': 'inline-block', 'margin': '0.5%'}),
                
                html.Div([
                    html.Label("Select Gender:", style={'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='filter-gender',
                        options=[
                            {'label': 'All', 'value': 'All'},
                            {'label': 'Male', 'value': 'Male'},
                            {'label': 'Female', 'value': 'Female'}
                        ],
                        value='All',
                        style={'width': '100%'}
                    )
                ], style={'width': '32%', 'display': 'inline-block', 'margin': '0.5%'}),
            ], style={'marginBottom': '20px', 'padding': '10px', 'backgroundColor': '#f8f9fa'}),
            
            # Charts Row 1
            html.Div([
                html.Div([
                    dcc.Graph(id='chart-churn-by-country')
                ], style={'width': '49%', 'display': 'inline-block', 'margin': '0.5%'}),
                
                html.Div([
                    dcc.Graph(id='chart-churn-by-age')
                ], style={'width': '49%', 'display': 'inline-block', 'margin': '0.5%'}),
            ]),
            
            # Charts Row 2
            html.Div([
                html.Div([
                    dcc.Graph(id='chart-balance-distribution')
                ], style={'width': '49%', 'display': 'inline-block', 'margin': '0.5%'}),
                
                html.Div([
                    dcc.Graph(id='chart-products-churn')
                ], style={'width': '49%', 'display': 'inline-block', 'margin': '0.5%'}),
            ]),
            
            # Charts Row 3
            html.Div([
                html.Div([
                    dcc.Graph(id='chart-age-distribution')
                ], style={'width': '49%', 'display': 'inline-block', 'margin': '0.5%'}),
                
                html.Div([
                    dcc.Graph(id='chart-tenure-churn')
                ], style={'width': '49%', 'display': 'inline-block', 'margin': '0.5%'}),
            ]),
            
            # Footer
            html.Div([
                html.P("Bank Customer Churn DWH & DSS | University Project",
                      style={'textAlign': 'center', 'color': '#95a5a6', 'marginTop': '20px'})
            ])
        ], style={'fontFamily': 'Arial, sans-serif', 'padding': '20px', 'backgroundColor': '#ffffff'})
    
    def card_style(self, border_color):
        """Return style for KPI cards"""
        return {
            'padding': '20px',
            'backgroundColor': '#ffffff',
            'borderRadius': '10px',
            'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
            'borderLeft': f'5px solid {border_color}',
            'textAlign': 'center'
        }
    
    def setup_callbacks(self):
        """Setup interactive callbacks"""
        
        # Update filter options
        @self.app.callback(
            [Output('filter-country', 'options'),
             Output('filter-age-group', 'options')],
            [Input('filter-country', 'id')]
        )
        def update_filter_options(_):
            if self.df is None:
                return [{'label': 'All', 'value': 'All'}], [{'label': 'All', 'value': 'All'}]
            
            countries = [{'label': 'All', 'value': 'All'}] + \
                       [{'label': c, 'value': c} for c in sorted(self.df['Geography'].unique())]
            
            age_groups = [{'label': 'All', 'value': 'All'}] + \
                        [{'label': str(ag), 'value': str(ag)} for ag in sorted(self.df['AgeGroup'].unique())]
            
            return countries, age_groups
        
        # Update KPIs and charts
        @self.app.callback(
            [Output('kpi-total-customers', 'children'),
             Output('kpi-churned', 'children'),
             Output('kpi-churn-rate', 'children'),
             Output('kpi-avg-balance', 'children'),
             Output('chart-churn-by-country', 'figure'),
             Output('chart-churn-by-age', 'figure'),
             Output('chart-balance-distribution', 'figure'),
             Output('chart-products-churn', 'figure'),
             Output('chart-age-distribution', 'figure'),
             Output('chart-tenure-churn', 'figure')],
            [Input('filter-country', 'value'),
             Input('filter-age-group', 'value'),
             Input('filter-gender', 'value')]
        )
        def update_dashboard(country, age_group, gender):
            if self.df is None:
                empty_fig = go.Figure()
                return "N/A", "N/A", "N/A", "N/A", empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig
            
            # Filter data
            df_filtered = self.df.copy()
            if country != 'All':
                df_filtered = df_filtered[df_filtered['Geography'] == country]
            if age_group != 'All':
                df_filtered = df_filtered[df_filtered['AgeGroup'].astype(str) == age_group]
            if gender != 'All':
                df_filtered = df_filtered[df_filtered['Gender'] == gender]
            
            # Calculate KPIs
            total = len(df_filtered)
            churned = df_filtered['Exited'].sum()
            churn_rate = (churned / total * 100) if total > 0 else 0
            avg_balance = df_filtered['Balance'].mean()
            
            # Create charts
            fig1 = self.create_churn_by_country(df_filtered)
            fig2 = self.create_churn_by_age(df_filtered)
            fig3 = self.create_balance_distribution(df_filtered)
            fig4 = self.create_products_churn(df_filtered)
            fig5 = self.create_age_distribution(df_filtered)
            fig6 = self.create_tenure_churn(df_filtered)
            
            return (
                f"{total:,}",
                f"{int(churned):,}",
                f"{churn_rate:.1f}%",
                f"${avg_balance:,.0f}",
                fig1, fig2, fig3, fig4, fig5, fig6
            )
    
    def create_churn_by_country(self, df):
        """Create churn rate by country chart"""
        churn_by_country = df.groupby('Geography')['Exited'].agg(['sum', 'count', 'mean']).reset_index()
        churn_by_country['churn_rate'] = churn_by_country['mean'] * 100
        
        fig = px.bar(churn_by_country, x='Geography', y='churn_rate',
                     title='Churn Rate by Country',
                     labels={'churn_rate': 'Churn Rate (%)', 'Geography': 'Country'},
                     color='churn_rate',
                     color_continuous_scale='Reds')
        fig.update_layout(showlegend=False, height=400)
        return fig
    
    def create_churn_by_age(self, df):
        """Create churn rate by age group chart"""
        age_order = ['<=25', '26-35', '36-45', '46-55', '>=56']
        churn_by_age = df.groupby('AgeGroup')['Exited'].agg(['sum', 'count', 'mean']).reset_index()
        churn_by_age['churn_rate'] = churn_by_age['mean'] * 100
        churn_by_age['AgeGroup'] = pd.Categorical(churn_by_age['AgeGroup'], categories=age_order, ordered=True)
        churn_by_age = churn_by_age.sort_values('AgeGroup')
        
        fig = px.bar(churn_by_age, x='AgeGroup', y='churn_rate',
                     title='Churn Rate by Age Group',
                     labels={'churn_rate': 'Churn Rate (%)', 'AgeGroup': 'Age Group'},
                     color='churn_rate',
                     color_continuous_scale='Blues')
        fig.update_layout(showlegend=False, height=400)
        return fig
    
    def create_balance_distribution(self, df):
        """Create balance distribution by churn status"""
        fig = px.box(df, x='Exited', y='Balance',
                     title='Account Balance Distribution by Churn Status',
                     labels={'Exited': 'Churn Status', 'Balance': 'Account Balance ($)'},
                     color='Exited',
                     color_discrete_map={0: '#2ecc71', 1: '#e74c3c'})
        fig.update_xaxes(ticktext=['Retained', 'Churned'], tickvals=[0, 1])
        fig.update_layout(showlegend=False, height=400)
        return fig
    
    def create_products_churn(self, df):
        """Create churn rate by number of products"""
        products_churn = df.groupby('NumOfProducts')['Exited'].agg(['sum', 'count', 'mean']).reset_index()
        products_churn['churn_rate'] = products_churn['mean'] * 100
        
        fig = px.bar(products_churn, x='NumOfProducts', y='churn_rate',
                     title='Churn Rate by Number of Products',
                     labels={'churn_rate': 'Churn Rate (%)', 'NumOfProducts': 'Number of Products'},
                     color='churn_rate',
                     color_continuous_scale='Oranges')
        fig.update_layout(showlegend=False, height=400)
        return fig
    
    def create_age_distribution(self, df):
        """Create age distribution histogram"""
        fig = px.histogram(df, x='Age', nbins=30,
                          title='Customer Age Distribution',
                          labels={'Age': 'Age', 'count': 'Frequency'},
                          color_discrete_sequence=['#3498db'])
        fig.update_layout(showlegend=False, height=400)
        return fig
    
    def create_tenure_churn(self, df):
        """Create churn rate by tenure"""
        tenure_churn = df.groupby('Tenure')['Exited'].agg(['sum', 'count', 'mean']).reset_index()
        tenure_churn['churn_rate'] = tenure_churn['mean'] * 100
        
        fig = px.line(tenure_churn, x='Tenure', y='churn_rate',
                     title='Churn Rate by Customer Tenure',
                     labels={'churn_rate': 'Churn Rate (%)', 'Tenure': 'Tenure (Years)'},
                     markers=True)
        fig.update_traces(line_color='#9b59b6', marker=dict(size=8))
        fig.update_layout(showlegend=False, height=400)
        return fig
    
    def run(self, debug=True, port=3000):
        """Run the dashboard server"""
        print(f"\n{'='*60}")
        print("STARTING CHURN ANALYTICS DASHBOARD")
        print(f"{'='*60}\n")
        print(f"Dashboard will be available at: http://localhost:{port}")
        print("Press Ctrl+C to stop the server\n")
        
        self.app.run(debug=debug, port=port)


def main():
    """Main function to run the dashboard"""
    dashboard = ChurnDashboard()
    dashboard.run(debug=True, port=3000)


if __name__ == "__main__":
    main()
