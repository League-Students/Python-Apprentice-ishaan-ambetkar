import turtle

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
    p.speed(0); p.shape("square"); p.color("white"); p.penup()
    p.shapesize(stretch_wid=5, stretch_len=1)
    p.goto(x, 0)
    return p

paddle_a = create_paddle(-350)
paddle_b = create_paddle(350)

ball = turtle.Turtle()
ball.speed(0); ball.shape("square"); ball.color("white"); ball.penup()
ball.dx, ball.dy = 0.3, 0.3

# Scoreboard
hud = turtle.Turtle()
hud.speed(0); hud.color("white"); hud.penup(); hud.hideturtle()
hud.goto(0, 260)
hud.write("A: 0  B: 0", align="center", font=("Courier", 24, "normal"))

# Movement Functions
def paddle_a_up():
    y = paddle_a.ycor(); paddle_a.sety(y + 20) if y < 250 else None
def paddle_a_down():
    y = paddle_a.ycor(); paddle_a.sety(y - 20) if y > -250 else None
def paddle_b_up():
    y = paddle_b.ycor(); paddle_b.sety(y + 20) if y < 250 else None
def paddle_b_down():
    y = paddle_b.ycor(); paddle_b.sety(y - 20) if y > -250 else None

# Keyboard Binding
win.listen()
win.onkeypress(paddle_a_up, "w")
win.onkeypress(paddle_a_down, "s")
win.onkeypress(paddle_b_up, "Up")
win.onkeypress(paddle_b_down, "Down")

# Main Loop
while True:
    win.update()
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Collision & Scoring
    if ball.ycor() > 290 or ball.ycor() < -290: ball.dy *= -1
    if ball.xcor() > 390 or ball.xcor() < -390:
        ball.goto(0, 0); ball.dx *= -1
        score_a += 1 if ball.xcor() < 0 else 0
        score_b += 1 if ball.xcor() > 0 else 0
        hud.clear(); hud.write(f"A: {score_a}  B: {score_b}", align="center", font=("Courier", 24, "normal"))

    if (340 < ball.xcor() < 350 and abs(ball.ycor() - paddle_b.ycor()) < 50) or \
       (-350 < ball.xcor() < -340 and abs(ball.ycor() - paddle_a.ycor()) < 50):
        ball.dx *= -1