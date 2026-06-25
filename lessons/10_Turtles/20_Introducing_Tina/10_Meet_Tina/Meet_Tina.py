import turtle
import time
import random

# Game configuration constants
DELAY = 0.1
SCORE = 0
HIGH_SCORE = 0

# Set up the game screen canvas
screen = turtle.Screen()
screen.title("Google Snake Game (Python)")
screen.bgcolor("#578a34")  # Classic Google Snake green
screen.setup(width=600, height=600)
screen.tracer(0)  # Turns off automatic screen updates for smoother rendering

# Create the Snake's head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("#4a752c")  # Darker green for the head
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Create the Food (Apple)
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("#e74c3c")  # Apple red
food.penup()
food.goto(0, 100)

# List to hold the segments of the snake's body
segments = []

# Scoreboard display setup
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center", font=("Arial", 24, "bold"))

# Movement validation functions (prevents reversing directly into yourself)
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

# Update position vectors based on current direction
def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

# Keyboard input bindings
screen.listen()
screen.onkeypress(go_up, "Up")
screen.onkeypress(go_down, "Down")
screen.onkeypress(go_left, "Left")
screen.onkeypress(go_right, "Right")

# Main Game Loop
while True:
    screen.update()

    # Check for wall collisions (Out of bounds)
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        time.sleep(1)
        head.goto(0, 0)
        head.direction = "stop"

        # Hide the body segments when resetting
        for segment in segments:
            segment.goto(1000, 1000)
        segments.clear()

        # Reset game session score metrics
        SCORE = 0
        pen.clear()
        pen.write(f"Score: {SCORE}  High Score: {HIGH_SCORE}", align="center", font=("Arial", 24, "bold"))

    # Check for food collision (Snake eats the apple)
    if head.distance(food) < 20:
        # Reposition the food to a random grid location
        x = random.randint(-14, 14) * 20
        y = random.randint(-14, 14) * 20
        food.goto(x, y)

        # Grow the snake by appending a new body segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("#b1c999")  # Lighter green body segment
        new_segment.penup()
        segments.append(new_segment)

        # Update scoring values
        SCORE += 10
        if SCORE > HIGH_SCORE:
            HIGH_SCORE = SCORE
        
        pen.clear()
        pen.write(f"Score: {SCORE}  High Score: {HIGH_SCORE}", align="center", font=("Arial", 24, "bold"))

    # Move the end segments first in reverse order to follow the path
    for index in range(len(segments) - 1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)

    # Move segment 0 to the position where the head was
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    move()

    # Check for self-collision (Snake runs into its own tail)
    for segment in segments:
        if segment.distance(head) < 20:
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "stop"
            
            for seg in segments:
                seg.goto(1000, 1000)
            segments.clear()
            
            SCORE = 0
            pen.clear()
            pen.write(f"Score: {SCORE}  High Score: {HIGH_SCORE}", align="center", font=("Arial", 24, "bold"))

    time.sleep(DELAY)

screen.mainloop()