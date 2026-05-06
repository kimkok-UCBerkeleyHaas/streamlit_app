# linear regression app in streamlit
import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Sample x and y values
x = np.linspace(0, 10, 100)
true_slope = 2
true_intercept = 1
y = [1.33834027, 0.466297, 0.65657658, 2.81295272, 1.91558707, 1.94654332, 1.70041666, 2.00043377,
 1.47658775, 3.02842091, 2.5455045, 4.40579211, 3.00547067, 2.30514459, 5.51214582, 3.76696161,
 5.72006752, 4.64999898, 8.47257988, 6.06168009, 5.07555886, 5.54756556, 4.70414018, 5.19428963,
 5.06218166, 5.55128344, 5.44043216, 5.2349653, 5.95758662, 7.45846738, 7.53273748, 7.49013263,
 8.71045918, 6.52562765, 7.47811641, 7.61698675, 8.9879674, 8.7720833, 7.30291837, 9.61149918,
 9.44026857, 10.96099466, 10.46039585, 10.35499903, 9.65048691, 9.40352371, 10.57604901,
 10.85021488, 9.18578763, 11.96991231, 12.11471772, 11.20966054, 11.09294182, 12.57767102,
 10.904476, 10.68065032, 12.21740325, 13.33584236, 14.04100026, 12.67103981, 12.45006044,
 13.29672482, 13.55070585, 12.28027721, 12.63208897, 13.37240742, 13.0879925, 14.16029844,
 15.80615295, 14.0770665, 15.99523426, 15.34006979, 14.20243096, 16.45749069, 16.87052957,
 16.03642403, 17.60328494, 14.51637791, 16.95978813, 17.51309463, 16.59271327, 16.39797672,
 15.67970033, 16.86023381, 17.42297663, 18.59399204, 19.93657387, 18.44827168, 18.99734926,
 17.78251538, 20.5421966, 19.25568482, 17.62994326, 20.4547526, 21.15984321, 21.16034499,
 20.85578454, 19.91514047, 19.78394871, 20.78790285]
#true_slope * x + true_intercept + np.random.normal(0, 1, size=x.shape)  # Adding some noise to y values
#print(y)

# calculate MSE
def compute_mse(slope, intercept, x, y):
    predicted_y = slope * x + intercept
    mse = np.mean((y - predicted_y) ** 2)
    return mse

# Streamlit app
st.title("Savio's Interactive Regression App")

# Slope and intercept input fields
st.sidebar.subheader("Adjust the Slope and Intercept")
slope_input = st.sidebar.slider("Slope", min_value=-10.0, max_value=10.0, value=1.0, step=0.1)
intercept_input = st.sidebar.slider("Intercept", min_value=-10.0, max_value=10.0, value=0.0, step=0.1)

# Compute MSE with the user's input values
mse = compute_mse(slope_input, intercept_input, x, y)

# Updated plot with the user's line
fig = go.Figure()

# Scatter plot for data points
fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name='Data points', marker=dict(color='blue')))

# User's line plot
fig.add_trace(go.Scatter(x=x, y=slope_input * x + intercept_input, mode='lines', name="User's line", line=dict(color='green')))

fig.update_layout(
    title=f"Scatter Plot of Data with Line (Slope: {slope_input}, Intercept: {intercept_input})",
    xaxis_title='X',
    yaxis_title='Y',
    showlegend=True
)

# Display the updated Plotly figure
st.plotly_chart(fig)

# Display the MSE
st.sidebar.subheader(f"Mean Squared Error (MSE) for the model: {mse:.4f}")

fig = go.Figure()

# Scatter plot for data points
fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name='Data points', marker=dict(color='blue')))

# True line plot (based on actual slope and intercept)
fig.add_trace(go.Scatter(x=x, y=true_slope * x + true_intercept, mode='lines', name='True line', line=dict(dash='dash', color='red')))

fig.update_layout(
    title="Scatter Plot of Sample Data with True Line",
    xaxis_title='X',
    yaxis_title='Y',
    showlegend=True
)

# Display the Plotly figure
st.plotly_chart(fig)
