"""Personal dashboard: UCI Wine Quality. Run locally with python app.py or host on Render."""
from pathlib import Path
import pandas as pd
from dash import Dash, Input, Output, dcc, html
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def build_dashboard(data):
    data = data.copy()
    type_order = ['red', 'white']
    type_colors = {'red': '#b2182b', 'white': '#2166ac'}
    corr_features = ['quality', 'alcohol', 'volatile acidity', 'fixed acidity', 'density']
    short_labels = ['Quality', 'Alcohol', 'Volatile acidity', 'Fixed acidity', 'Density']

    app = Dash(__name__)
    app.layout = html.Div([
        html.H1('Wine chemistry and expert quality scores'),
        html.P('Vinho Verde samples from UCI Wine Quality. Explore how alcohol and volatile acidity relate '
               'to expert scores in red and white wines. These are recorded samples, not a prediction of '
               'how a wine will taste to you.'),
        html.Label('Wine type - updates all four figures and the sample summary', htmlFor='wine-type'),
        dcc.Dropdown(
            id='wine-type',
            options=[{'label': 'All wines', 'value': 'all'},
                     {'label': 'Red wines', 'value': 'red'},
                     {'label': 'White wines', 'value': 'white'}],
            value='all', clearable=False, style={'maxWidth': '360px'}
        ),
        html.P(id='sample-summary'),
        html.Div([
            html.Div([dcc.Graph(id='quality-share')], style={'width': '50%', 'padding': '6px'}),
            html.Div([dcc.Graph(id='alcohol-box')], style={'width': '50%', 'padding': '6px'}),
        ], style={'display': 'flex', 'flexWrap': 'wrap'}),
        html.Div([
            html.Div([dcc.Graph(id='scatter')], style={'width': '50%', 'padding': '6px'}),
            html.Div([dcc.Graph(id='corr-heatmap')], style={'width': '50%', 'padding': '6px'}),
        ], style={'display': 'flex', 'flexWrap': 'wrap'}),
        html.P(id='conclusion-note'),
        html.P('Source: Cortez et al. (2009), UCI Wine Quality, winequality-red.csv and '
               'winequality-white.csv, combined with a wine_type label. Quality is the median of at least '
               'three expert ratings on a 0-10 scale. Limitations: expert score is not consumer preference; '
               'no price, brand, grape, or region is available; the groups are unbalanced (1,599 red, '
               '4,898 white) and score 9 has only 5 white samples; 1,177 exact duplicate rows were kept. '
               'The patterns are associations, not causes.'),
    ], style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f6f7f9',
              'color': '#202b35', 'padding': '24px', 'maxWidth': '1200px', 'margin': 'auto'})

    @app.callback(
        Output('quality-share', 'figure'),
        Output('alcohol-box', 'figure'),
        Output('scatter', 'figure'),
        Output('corr-heatmap', 'figure'),
        Output('sample-summary', 'children'),
        Output('conclusion-note', 'children'),
        Input('wine-type', 'value')
    )
    def update_dashboard(selection):
        visible = type_order if selection == 'all' else [selection]
        selected = data.loc[data['wine_type'].isin(visible)]

        # Figure 1: percent of samples at each score within each selected type.
        counts = pd.crosstab(selected['quality'], selected['wine_type']).reindex(
            index=sorted(data['quality'].unique()), columns=visible, fill_value=0)
        percent = counts.copy().astype(float)
        for wine_type in visible:
            total = counts[wine_type].sum()
            percent[wine_type] = 100 * counts[wine_type] / total if total else 0.0
        long_percent = percent.reset_index().melt(id_vars='quality', var_name='wine_type', value_name='percent')
        fig1 = px.bar(long_percent, x='quality', y='percent', color='wine_type', barmode='group',
                      color_discrete_map=type_colors, category_orders={'wine_type': visible},
                      labels={'quality': 'Expert quality score (0-10)',
                              'percent': 'Percent within wine type', 'wine_type': 'Wine type'},
                      title='Quality scores within each wine type')

        # Figure 2: alcohol by score, with the same type colors.
        fig2 = px.box(selected, x='quality', y='alcohol', color='wine_type', points=False,
                      category_orders={'wine_type': visible}, color_discrete_map=type_colors,
                      labels={'quality': 'Expert quality score (0-10)',
                              'alcohol': 'Alcohol (% by volume)', 'wine_type': 'Wine type'},
                      title='Alcohol by quality score')

        # Figure 3: one point per sample, score on a common color scale.
        fig3 = px.scatter(selected, x='alcohol', y='volatile acidity', color='quality',
                          facet_col='wine_type', color_continuous_scale='Viridis',
                          range_color=[3, 9], opacity=0.65,
                          labels={'alcohol': 'Alcohol (% by volume)',
                                  'volatile acidity': 'Volatile acidity (g/L)',
                                  'quality': 'Quality score', 'wine_type': 'Wine type'},
                          title='Alcohol, volatile acidity, and quality')
        fig3.for_each_annotation(lambda a: a.update(text=a.text.split('=')[-1].capitalize() + ' wines'))

        # Figure 4: Pearson correlations, one heatmap per selected type.
        fig4 = make_subplots(rows=1, cols=len(visible), subplot_titles=[t.capitalize() + ' wines' for t in visible])
        for index, wine_type in enumerate(visible, start=1):
            group = selected.loc[selected['wine_type'].eq(wine_type)]
            corr = group[corr_features].corr() if not group.empty else pd.DataFrame(
                0.0, index=corr_features, columns=corr_features)
            fig4.add_trace(go.Heatmap(
                z=corr.values, x=short_labels, y=short_labels, zmin=-1, zmax=1,
                colorscale='RdBu_r', text=corr.round(2).values,
                texttemplate='%{text:.2f}', textfont={'size': 10},
                showscale=(index == len(visible)), colorbar={'title': 'Pearson r'}
            ), row=1, col=index)
        fig4.update_layout(title='Correlations among selected measurements', height=460)

        parts = [f'{len(selected):,} of {len(data):,} samples shown']
        for wine_type in visible:
            parts.append(f'{wine_type}: {int(selected["wine_type"].eq(wine_type).sum()):,}')
        summary = ' | '.join(parts) + '. Percentages use the selected wine type(s) as the denominator.'
        note = ('All-data conclusion (based on all ' + f'{len(data):,}' +
                ' samples, not the current selection): higher alcohol and lower volatile acidity are '
                'associated with higher quality scores, and the volatile-acidity pattern is stronger in '
                'red wines. These are associations, not causes.')
        if selection != 'all':
            note = 'Filtered view: ' + selection + ' wines. ' + note

        if selected.empty:
            for fig in [fig1, fig2, fig3, fig4]:
                fig.update_layout(annotations=[{'text': 'No samples in this selection.',
                                                'x': 0.5, 'y': 0.5, 'xref': 'paper', 'yref': 'paper',
                                                'showarrow': False, 'font': {'size': 18}}])
            summary = 'No samples in this selection. Percentages are not defined.'
        for fig in [fig1, fig2, fig3, fig4]:
            fig.update_layout(template='plotly_white', height=460)
        return fig1, fig2, fig3, fig4, summary, note

    return app

data = pd.read_csv(
    Path(__file__).resolve().parent / 'data' / 'wine_quality_red_white.csv',
    dtype={'wine_type': 'object'},
)
app = build_dashboard(data)
server = app.server

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8055, debug=False)
