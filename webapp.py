from GTC import ureal
from dash import Dash, dcc, html, Input, Output, callback
from flask import request, Response

data = {
    'voltage': (1, 0),  # value, uncertainty
    'current1': (1, 0),
    'current2': (1, 0),
}

header_style = {
    'font-size': '6vw',
    'padding': '72px',
}
iv_style = {
    'font-size': '4vw',
    'text-align': 'center',
}
power_style = {
    'font-size': '4vw',
    'text-align': 'center',
    'padding-top': '72px',
}
power_value_style = {
    'font-size': '7vw',
    'text-align': 'center',
    'color': '#D2691E',
    'padding-top': '72px',
}

app = Dash(__name__, title='World Metrology Day 2024')
app.layout = html.Div(
    html.Div([
        html.Img(src='assets/wmd-2024-banner.png', alt='WMD-2024', width='100%'),
        html.Div(id='live-update-text'),
        dcc.Interval(
            id='interval-component',
            interval=1000,  # milliseconds
            n_intervals=0
        )
    ])
)


@callback(Output('live-update-text', 'children'), Input('interval-component', 'n_intervals'))
def update_voltage_1(n):
    voltage = ureal(*data['voltage'])
    current1 = ureal(*data['current1'])
    current2 = ureal(*data['current2'])
    power1 = voltage * current1  # true for DC, for AC we ignore phase (good enough for a booth demo)
    power2 = voltage * current2
    return html.Table([
            html.Tr([
                html.Th(''),
                html.Th('LED', style=header_style),
                html.Th('Halogen', style=header_style),
            ]),
            html.Tr([
                html.Td('Voltage', style=iv_style),
                html.Td(f'{voltage:.3g} V', style=iv_style),
                html.Td(f'{voltage:.3g} V', style=iv_style),
            ]),
            html.Tr([
                html.Td('Current', style=iv_style),
                html.Td(f'{current1:.3g} A', style=iv_style),
                html.Td(f'{current2:.3g} A', style=iv_style),
            ]),
            html.Tr([
                html.Td('Power', style=power_style),
                html.Td(f'{power1:.3g} W', style=power_value_style),
                html.Td(f'{power2:.3g} W', style=power_value_style),
            ]),
        ], 
        style={'width': '100%'},
    )


@app.server.route('/update', methods=["PUT"])
def update():
    data.update(request.json)
    return Response('ok', status=200)
    

if __name__ == '__main__':
    import webbrowser
    webbrowser.open('http://127.0.0.1:8050')
    app.run(debug=False)
