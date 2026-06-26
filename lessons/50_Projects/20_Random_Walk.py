"""
League of Amazing Programmers
Recipe: Turtle Derpy Face (Rounded Paws Up)
"""
import turtle

def draw_derpy_face():
    # Setup canvas
    screen = turtle.Screen()
    screen.setup(width=600, height=600)
    screen.bgcolor("white")
    
    t = turtle.Turtle()
    t.speed(4)
    t.pensize(5)
    
    # --- DRAW HEAD OUTLINE ---
    t.penup()
    t.goto(0, -100) 
    t.pendown()
    t.color("black", "#f2f2f2") # Light grey face fill
    t.begin_fill()
    t.circle(120)
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
    t.circle(15, 120) 

   
    t.color("black", "#f2f2f2") 
   
    t.penup()
    t.goto(-110, -20) 
    t.setheading(120) 
    t.pendown()
    t.begin_fill()
    t.circle(20, 180) 
    t.goto(-115, -45) 
    t.end_fill()
    
    t.penup()
    t.goto(110, -20) 
    t.setheading(60)  
    t.pendown()
    t.begin_fill()
    t.circle(-20, 180) 
    t.goto(115, -45)  
    t.end_fill()

    t.hideturtle()
    screen.mainloop()

if __name__ == '__main__':
    draw_derpy_face()