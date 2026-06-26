"""
League of Amazing Programmers
Recipe: Drawing Derpy Cheeks Face with Turtle
"""
import turtle

def draw_derpy_face():
    # Setup screen and turtle pen
    screen = turtle.Screen()
    screen.setup(width=600, height=600)
    screen.bgcolor("white")
    
    t = turtle.Turtle()
    t.speed(3)  # Moderate speed so you can watch it draw
    t.pensize(5)
    
    # --- DRAW HEAD (The ʕ ʔ body outline) ---
    t.penup()
    t.goto(0, -100) # Center bottom of the face
    t.pendown()
    t.color("black", "#f2f2f2") # Light grey face fill
    t.begin_fill()
    t.circle(120)
    t.end_fill()
    
    # --- DRAW BLUSHING CHEEKS (•ᴥ•) ---
    # Left Pink Cheek
    t.penup()
    t.goto(-65, -10)
    t.pendown()
    t.color("#ff9999") # Soft pink color
    t.begin_fill()
    t.circle(20)
    t.end_fill()
    
    # Right Pink Cheek
    t.penup()
    t.goto(65, -10)
    t.pendown()
    t.begin_fill()
    t.circle(20)
    t.end_fill()

    # --- DRAW EYES (•) ---
    t.color("black")
    # Left Eye
    t.penup()
    t.goto(-35, 20)
    t.pendown()
    t.begin_fill()
    t.circle(6)
    t.end_fill()
    
    # Right Eye
    t.penup()
    t.goto(35, 20)
    t.pendown()
    t.begin_fill()
    t.circle(6)
    t.end_fill()

    # --- DRAW NOSE/MOUTH (ᴥ) ---
    t.penup()
    t.goto(-15, 0)
    t.pendown()
    t.setheading(-60)
    t.circle(15, 120) # Center mouth curve
    
    # --- DRAW HANDS (っ っ) ---
    # Left Hugging Hand
    t.penup()
    t.goto(-100, -60)
    t.setheading(160)
    t.pendown()
    t.circle(25, 180)
    
    # Right Hugging Hand
    t.penup()
    t.goto(60, -60)
    t.setheading(200)
    t.pendown()
    t.circle(-25, 180)

    # Hide turtle pen and keep window open
    t.hideturtle()
    screen.mainloop()

if __name__ == '__main__':
    draw_derpy_face()