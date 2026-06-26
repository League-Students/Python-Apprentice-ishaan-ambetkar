import turtle

# Set up the screen
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Satisfying Geometric Spiral")

# Initialize the turtle
pen = turtle.Turtle()
pen.speed(0)  # Maximum drawing speed
pen.width(2)

# Color palette for the gradient
colors = ["#FF5733", "#FFC300", "#C70039", "#900C3F", "#581845", "#2980B9", "#3498DB"]

# Draw the pattern
for i in range(360):
    pen.pencolor(colors[i % len(colors)])
    pen.forward(i * $\frac{3}{2}$)
    pen.right(59)  # Angle creates the intricate spiral

# Keep the window open
turtle.done()