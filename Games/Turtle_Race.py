import time
import turtle
from turtle import *
from random import randint


setup(800,500)
title("Turtle Race")
bgcolor("forestgreen")
speed(0)

penup()
goto(-100,205)
color("white")
write("TURTLE RACE", font= ("Arial", 20, "bold"))

#DIRT
goto(-350, 200)
pendown()
color("chocolate")
begin_fill()
for i in range(2):
    forward(700)
    right(90)
    forward(400)
    right(90)
end_fill()

# FINISH LINE
gap_size = 20
shape("square")
penup()

color("white")
for i in range(10):
    goto(250, (170-(i * gap_size *2)))
    stamp()

for i in range(10):
    goto(250 + gap_size, ((210- gap_size) - (i * gap_size *2)))
    stamp()


# BLACK squares
color("black")
for i in range(10):
    goto(250, (190-(i * gap_size *2)))
    stamp()

for i in range(10):
    goto(251 + gap_size, ((190- gap_size) - (i * gap_size *2)))
    stamp()


# TURTLE 1 - BLUE
blue_turtle = Turtle()
blue_turtle.color("cyan")
blue_turtle.shape("turtle")
blue_turtle.shapesize(1.5)
blue_turtle.penup()
blue_turtle.goto(-300,150)
blue_turtle.pendown()


# TURTLE 2 - PINK
pink_turtle = Turtle()
pink_turtle.color("magenta")
pink_turtle.shape("turtle")
pink_turtle.shapesize(1.5)
pink_turtle.penup()
pink_turtle.goto(-300,50)
pink_turtle.pendown()


# TURTLE 3 - YELLOW
yellow_turtle = Turtle()
yellow_turtle.color("yellow")
yellow_turtle.shape("turtle")
yellow_turtle.shapesize(1.5)
yellow_turtle.penup()
yellow_turtle.goto(-300,-50)
yellow_turtle.pendown()


# TURTLE 4 - GREEN
green_turtle = Turtle()
green_turtle.color("lime")
green_turtle.shape("turtle")
green_turtle.shapesize(1.5)
green_turtle.penup()
green_turtle.goto(-300,-150)
green_turtle.pendown()


time.sleep(1)

while blue_turtle.xcor() <= 230 and blue_turtle.xcor() <= 230 and yellow_turtle.xcor() <= 230 and green_turtle.xcor() <= 230 :
    blue_turtle.forward(randint(1,10))
    pink_turtle.forward(randint(1,10))
    yellow_turtle.forward(randint(1,10))
    green_turtle.forward(randint(1,10))


if blue_turtle.xcor() > pink_turtle.xcor() and blue_turtle.xcor() > yellow_turtle.xcor() and blue_turtle.xcor() > green_turtle.xcor():
    print("Blue turtle wins!")
    for i in range(72):
        blue_turtle.right(5)
        blue_turtle.shapesize(2.5)
elif pink_turtle.xcor() > blue_turtle.xcor() and pink_turtle.xcor() > yellow_turtle.xcor() and pink_turtle.xcor() > green_turtle.xcor():
    print("Pink turtle wins!")    
    for i in range(72):
        pink_turtle.right(5)
        pink_turtle.shapesize(2.5)
elif yellow_turtle.xcor() > blue_turtle.xcor() and yellow_turtle.xcor() > pink_turtle.xcor() and yellow_turtle.xcor() > green_turtle.xcor():
    print("Yellow turtle wins!")
    for i in range(72):
        yellow_turtle.right(5)
        yellow_turtle.shapesize(2.5)
else:
    print("Green turtle wins!")
    for i in range(72):
        green_turtle.right(5)
        green_turtle.shapesize(2.5)

turtle.done()