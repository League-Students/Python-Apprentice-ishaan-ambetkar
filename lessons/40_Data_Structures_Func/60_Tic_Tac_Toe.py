import turtle
import math
import random

# Screen setup
wn = turtle.Screen()
wn.title("Python Shooting Game")
wn.bgcolor("lightblue")
wn.setup(width=600, height=600)
wn.tracer(0)

# Player
player = turtle.Turtle()
player.shape("triangle")
player.color("blue")
player.penup()
player.goto(0, -270)
player.setheading(90)

# Target
target = turtle.Turtle()
target.shape("circle")
target.color("red")
target.penup()
target.goto(random.randint(-280, 280), random.randint(100, 250))

# Bullet
bullet = turtle.Turtle()
bullet.shape("circle")
bullet.color("black")
bullet.penup()
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

# Score
score = 0
score_display = turtle.Turtle()
score_display.hideturtle()
score_display.penup()
score_display.goto(-280, 260)
score_display.write(f"Score: {score}", font=("Courier", 16, "normal"))

# Game state
bullet_state = "ready" # "ready" to fire, "fire" in motion

# Functions
def aim(x, y):
    player.setheading(player.towards(x, y))

def fire():
    global bullet_state
    if bullet_state == "ready":
        bullet_state = "fire"
        bullet.showturtle()
        bullet.goto(player.pos())
        bullet.setheading(player.heading())

def is_collision(t1, t2):
    distance = math.sqrt((t1.xcor() - t2.xcor())**2 + (t1.ycor() - t2.ycor())**2)
    return distance < 20

# Keyboard and mouse bindings
wn.listen()
wn.onscreenclick(aim)
wn.onkeypress(fire, "space")

# Main game loop
while True:
    wn.update()
    
    # Move bullet
    if bullet_state == "fire":
        bullet.forward(20)
        
    # Boundary check for bullet
    if bullet.ycor() > 300 or bullet.ycor() < -300 or bullet.xcor() > 300 or bullet.xcor() < -300:
        bullet.hideturtle()
        bullet_state = "ready"
        
    # Check for collision with target
    if is_collision(bullet, target):
        bullet.hideturtle()
        bullet_state = "ready"
        
        # Reset target
        target.goto(random.randint(-280, 280), random.randint(100, 250))
        
        # Update score
        score += 10
        score_display.clear()
        score_display.write(f"Score: {score}", font=("Courier", 16, "normal"))

turtle.done()