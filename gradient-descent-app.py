# streamlit app
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# Define the quadratic function and its gradient
def quadratic_function(x):
    return x**2

def gradient(x):
    return 2*x

st.title("Interactive Gradient Descent Demo")

# Input parameters
learning_rate = st.slider("Learning Rate", min_value=0.01, max_value=0.1, value=0.05, step=0.01)
iterations = st.slider("Number of Iterations", min_value=10, max_value=100, value=50, step=1)
initial_point = st.slider("Initial Point", min_value=-10, max_value=10, value=5, step=1)

# Gradient descent algorithm
def gradient_descent(starting_point, learning_rate, iterations):
    path = [starting_point]
    current_point = starting_point
    for _ in range(iterations):
        gradient_value = gradient(current_point)
        current_point = current_point - learning_rate * gradient_value
        path.append(current_point)
    return path

# Function to plot the steps interactively
def plot_gradient_descent_step_by_step(path):
    x_values = np.linspace(-10, 10, 400)
    y_values = quadratic_function(x_values)

    # Create a placeholder for the plot that will be updated
    plot_placeholder = st.empty()

    fig, ax = plt.subplots()
    ax.plot(x_values, y_values, label="Quadratic Function $f(x) = x^2$")
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.set_title('Gradient Descent Visualization')

    # Display the initial plot
    plot_placeholder.pyplot(fig)

    # Plot points step-by-step
    for i in range(len(path)):
        ax.scatter(path[i], quadratic_function(np.array([path[i]])), color="red", zorder=5)

        # Update the plot in-place
        plot_placeholder.pyplot(fig)

        # Pause for a moment to allow users to see the update
        time.sleep(0.1)

# Run gradient descent
path = gradient_descent(initial_point, learning_rate, iterations)

# Visualize step-by-step with the gradient descent path
plot_gradient_descent_step_by_step(path)

# Show the final path of the descent
st.write("Final Path of Gradient Descent:")
st.write(path)
