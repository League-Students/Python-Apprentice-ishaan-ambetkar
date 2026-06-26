import turtle
import time

# Setup Screen
win = turtle.Screen()
win.title("Pong")
win.bgcolor("black")
win.setup(width=800, height=600)
win.tracer(0)

# Scores
score_a, score_b = 0, 0

# Paddles and Ball
def create_paddle(x):
    p = turtle.Turtle()
    p.speed(0)
    p.shape("square")
    p.color("white")
    p.penup()
    p.shapesize(stretch_wid=5, stretch_len=1)
    p.goto(x, 0)
    return p

paddle_a = create_paddle(-350)
paddle_b = create_paddle(350)

ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()
ball.dx, ball.dy = 3, 3 

# Scoreboard
hud = turtle.Turtle()
hud.speed(0)
hud.color("white")
hud.penup()
hud.hideturtle()
hud.goto(0, 260)
hud.write("A: 0  B: 0", align="center", font=("Courier", 24, "normal"))

# Movement Functions (Increased paddle speed to 40)
def paddle_a_up():
    y = paddle_a.ycor()
    if y < 240:
        paddle_a.sety(y + 40)

def paddle_a_down():
    y = paddle_a.ycor()
    if y > -240:
        paddle_a.sety(y - 40)

def paddle_b_up():
    y = paddle_b.ycor()
    if y < 240:
        paddle_b.sety(y + 40)

def paddle_b_down():
    y = paddle_b.ycor()
    if y > -240:
        paddle_b.sety(y - 40)

# Keyboard Binding
win.listen()
win.onkeypress(paddle_a_up, "w")
win.onkeypress(paddle_a_down, "s")
win.onkeypress(paddle_b_up, "Up")
win.onkeypress(paddle_b_down, "Down")

# Main Loop
while True:
    time.sleep(0.016)  # Cap game speed to roughly 60 FPS
    win.update()
    
    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Ceiling and Floor Collisions
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1
    elif ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1

    # Left and Right Boundaries (Scoring)
    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_a += 1
        hud.clear()
        hud.write(f"A: {score_a}  B: {score_b}", align="center", font=("Courier", 24, "normal"))

    elif ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_b += 1
        hud.clear()
        hud.write(f"A: {score_a}  B: {score_b}", align="center", font=("Courier", 24, "normal"))

    # Right Paddle Collision
    if (340 < ball.xcor() < 350) and (paddle_b.ycor() - 50 < ball.ycor() < paddle_b.ycor() + 50):
        ball.setx(340)
        ball.dx *= -1

    # Left Paddle Collision
    if (-350 < ball.xcor() < -340) and (paddle_a.ycor() - 50 < ball.ycor() < paddle_a.ycor() + 50):
        ball.setx(-340)
        ball.dx *= -1