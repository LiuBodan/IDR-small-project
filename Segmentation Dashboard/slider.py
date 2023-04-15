import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input
import plotly.graph_objs as go
import cv2
import os

# read images
image_folder = '../img'
image_files = sorted([f for f in os.listdir(image_folder) if f.endswith('.png')])

# initiation
app = dash.Dash(__name__)

# frontend
app.layout = html.Div([
    html.H4('Displaying Multiple Images with a Slider'),
    dcc.Graph(id="graph"),
    html.Div([
        html.Label('Image Index:'),
        dcc.Slider(id='image-slider', min=0, max=len(image_files) - 1, value=0, step=1, marks={i: str(i) for i in range(len(image_files))})
    ], style={'width': '50%', 'padding': '20px'})
])

# an update in numpy 1.2 causes some problem for imshow
def custom_imshow(img, **kwargs):
    return go.Figure(data=go.Image(z=img, **kwargs))

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

if __name__ == '__main__':
    app.run_server(debug=True)
