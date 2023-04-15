import dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import cv2
import os
import numpy as np

# read images
image_folder = '../img'
image_files = sorted([f for f in os.listdir(image_folder) if f.endswith('.png')])

# no background for plots
layout = go.Layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)'
    )

def create_random_scatter_plot():
    N = 100
    random_x = np.random.randn(N)
    random_y = np.random.randn(N)

    trace = go.Scatter(x=random_x, y=random_y, mode='markers', marker=dict(color='black',
                                                                           size=10))
    layout = go.Layout(title='Random Scatter Plot', plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)')
    return go.Figure(data=[trace], layout=layout)

random_scatter_plot = create_random_scatter_plot()

# initiation
app = dash.Dash(__name__)
server = app.server
# frontend
app.layout = html.Div([

    html.H4('IDR small project dashboard', style={'font-family': 'Arial, sans-serif',
                                              'margin-left':'200px', 'font-size': '35px', }),


    # segmentation image
    html.Div(className='parent',
    children=[

    # left hand side segmentation
    html.Div([
    # headins and body
    html.H4('Segmented Planes Slider', style={'font-family': 'Arial, sans-serif',
                                              'margin-left':'200px', 'font-size': '25px', }),
    html.P('Slide the slider to see different segmentation planes or click play',
           style={'font-family': 'Arial, sans-serif', 'margin-left':'200px',
                  'font-size': '20px'}),
    dcc.Graph(id="graph", style={'width': '700px', 'height': '700px',
                                  'margin-left':'200px'}),
        ]),


    # right hand side plots
    html.Div([
    # headins and body
    html.H4('on developing', style={'font-family': 'Arial, sans-serif',
                                              'margin-left':'200px', 'font-size': '25px', }),
    html.P('on developing',
           style={'font-family': 'Arial, sans-serif', 'margin-left':'200px',
                  'font-size': '20px'}),
    dcc.Graph(id="right-plot", figure=random_scatter_plot, style={'margin-left':'200px',
                                                 'width': '700px', 'height': '700px'}),])
    ]),





    # slider for left hand side
    html.Div([
    html.Label('Image Index:'),
    dcc.Slider(id='image-slider', min=0, max=len(image_files) - 1,
                           value=0, step=1, marks={i: str(i) for i in range(len(image_files))}),
    # play
    html.Button('Play', id='play-button', n_clicks=0),
    dcc.Interval(id='interval', interval=500, max_intervals=-1, disabled=True),
    ], style={'width':'35%', 'margin-left':'200px'}),



    html.P('Images from omero guide on IDR', style={'font-family': 'Arial, sans-serif', 'font-size': '13px'}),
    html.P('Dash Board by Bodan Liu', style={'font-family': 'Arial, sans-serif', 'font-size': '13px'})
])



# update in numpy 1.2 causes problem in imshow
def custom_imshow(img, **kwargs):
    return go.Figure(data=go.Image(z=img, **kwargs), layout=layout)


# backend
@app.callback(
    Output("graph", "figure"),
    [Input('image-slider', 'value')])
def update_image(slider_value):
    image_file = image_files[slider_value]
    image_path = os.path.join(image_folder, image_file)
    img = cv2.imread(image_path)  # Read image as BGR
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    fig = custom_imshow(img)
    return fig

@app.callback(
    Output("interval", "disabled"),
    [Input("play-button", "n_clicks")])
def toggle_interval(n_clicks):
    return not n_clicks % 2

@app.callback(
    Output("image-slider", "value"),
    [Input("interval", "n_intervals")],
    [dash.dependencies.State("image-slider", "value")])
def update_slider_value(n_intervals, current_value):
    if current_value < len(image_files) - 1:
        return current_value + 1
    else:
        return 0



if __name__ == '__main__':
    app.run_server(debug=1)
