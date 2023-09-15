import turtle
import time

t = turtle.Turtle()
t2 = turtle.Turtle()
text = turtle.Turtle()
text2 = turtle.Turtle()


def practice(pos):
    for i in range(len(pos)):
        t2.pendown()
        text.write(f'{i+1} Generation', font=(10))
        text2.write(f'Score : {round(pos[i][4], 1)}', font=(10))
        for j in pos[i][3]:
            t2.setheading(j)
            t2.forward(50)
        t2.penup()
        t2.goto(0, 0)
        t2.clear()
        text.clear()
        text2.clear()

        time.sleep(0.1)


t.ht()
text.ht()
text2.ht()
t.pendown()
text2.penup()
t.shape("turtle")
t2.shape("turtle")
t2.shapesize(3)
text.color('red')
text2.setposition(0, -50)
t2.speed(7)
t.color('red')
t.speed(10)
t.forward(500)
t.left(90)
t.forward(500)
t.left(90)
t.forward(500)
t.left(90)
t.forward(500)
t.left(90)
t.penup()
