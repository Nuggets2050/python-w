import numpy as np
from bokeh.plotting import figure, show
from bokeh.layouts import column
from bokeh.models import Slider
from bokeh.io import curdoc
from scipy.integrate import odeint

def SIR_model(y, t, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I
    dIdt = beta * S * I - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

# Initial parameters
beta = 0.3
gamma = 0.1
N = 1000
I0 = 1
R0 = 0
S0 = N - I0 - R0
t = np.linspace(0, 160, 160)
y0 = S0, I0, R0

# Function to update the data
def update_data(beta, gamma):
    S, I, R = odeint(SIR_model, y0, t, args=(beta, gamma)).T
    return S, I, R

# Initial data
S, I, R = update_data(beta, gamma)

# Create a new plot
p = figure(title="SIR Model", x_axis_label='Czas', y_axis_label='populacja')
susceptible_line = p.line(t, S, legend_label="podejrzani", line_width=2, color="blue")
infected_line = p.line(t, I, legend_label="zarzażeni", line_width=2, color="red")
recovered_line = p.line(t, R, legend_label="zdrowi", line_width=2, color="green")

# Sliders
beta_slider = Slider(start=0.1, end=1.0, value=beta, step=0.1, title="Beta")
gamma_slider = Slider(start=0.05, end=0.5, value=gamma, step=0.05, title="Gamma")

# Update function
def update(attr, old, new):
    beta = beta_slider.value
    gamma = gamma_slider.value
    S, I, R = update_data(beta, gamma)
    susceptible_line.data_source.data['y'] = S
    infected_line.data_source.data['y'] = I
    recovered_line.data_source.data['y'] = R

# Attach the update function to the sliders
beta_slider.on_change('value', update)
gamma_slider.on_change('value', update)

# Layout
layout = column(p, beta_slider, gamma_slider)

# Add the layout to the current document
curdoc().add_root(layout)

# Show the plot
show(layout)
