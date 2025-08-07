import math
from os import remove
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.widget import Widget        
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Ellipse   
import random

class MyApp(App):
    App.title="Python ile Piton Oyunu"
    Window.size = (440, 700)  
    Window.clearcolor = (1, 1, 1, 1) 
    boyut=20   

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout=FloatLayout()
        self.apple=None
        self.snakeHead=None
        self.width,self.height=Window.size
        self.direction=""
        self.snakeParts=[]
        self.seconds=0.1
        self.point=0
        self.gameOver=False
        self.event=None
        self.playAgain=False
        self.btn1=Button()
        self.btn2=Button()


    def putSnakeHead(self):
        x=random.randint(0,self.width-MyApp.boyut)
        y=random.randint(0,self.height-MyApp.boyut)
        
        if self. apple and self.apple.pos==(x,y):
            self.putSnakeHead()
        else:
            self.snakeHead=SnakeBlock((x,y))
            self.snakeParts.append(self.snakeHead)
            self.layout.add_widget(self.snakeHead)

        

    def putApple(self):
        xa=random.randint(0,self.width-MyApp.boyut)
        ya=random.randint(0,self.height-MyApp.boyut)
        flag=False
        for i in range(len(self.snakeParts)):
            x,y=self.snakeParts[i].pos
            if x==xa and y==ya:
                flag=True
        if flag==True:
            self.putApple()
        else:
            self.apple=Apple((xa,ya))
            self.layout.add_widget(self.apple)
            
    def on_touch_down(self, touch):
        self.touch_start = touch.pos

    def on_touch_up(self, touch):
        x1, y1 = self.touch_start
        x2, y2 = touch.pos

        dx = x2 - x1
        dy = y2 - y1

        if abs(dx) > abs(dy):
            if dx > 0:
                self.direction = "right"
            else:
                self.direction = "left"
        else:
            if dy > 0:
                self.direction = "up"
            else:
                self.direction = "down"

    def determineDirection(self, window, key, scancode, codepoint, modifiers):
    # 'w', 'a', 's', 'd' tuşları için key kodları:
    # w = 119, a = 97, s = 115, d = 100

        if key == 119:  # w tuşu
            self.direction = 'up'
        elif key == 115:  # s tuşu
            self.direction = 'down'
        elif key == 97:  # a tuşu
            self.direction = 'left'
        elif key == 100:  # d tuşu
            self.direction = 'right'
        

    def createSnakePart(self):
        part=SnakeBlock((MyApp.boyut,MyApp.boyut))
        self.snakeParts.append(part)
        self.layout.add_widget(part)

    def updateSnakePartCoordinates(self):
        
        for i in range(len(self.snakeParts)-1,0,-1):
            self.snakeParts[i].pos=self.snakeParts[i-1].pos
            self.snakeParts[i].rect.pos = self.snakeParts[i].pos 
        
    def resetGame(self):
        self.snakeParts.clear()
        self.layout.clear_widgets()
        if(self.playAgain==True):
            self.btn1.text="Tekrar Oyna"
        self.direction=""
        self.layout.add_widget(self.btn1)
        self.layout.add_widget(self.btn2)
        self.btn1.bind(on_press=self.btn1_clicked)
        self.btn2.bind(on_press=self.btn2_clicked)
        
        
    def checkEatItself(self):
        
        for i in range(len(self.snakeParts)-1,2,-1):
            if(self.snakeParts[0].pos==self.snakeParts[i].pos):
                self.gameOver=True
                self.playAgain=True
                self.event.cancel()
                self.point=0
                break
        if(self.gameOver==True):
            self.resetGame()
                
        

    def checkEatApple(self):
        xa,ya=self.apple.pos
        wa,ha=self.apple.size
        mxa=xa+wa/2
        mya=ya+ha/2
        
        for i in range(len(self.snakeParts)):
            x,y=self.snakeParts[i].pos
            w,h=self.snakeParts[i].size
            mx=x+w/2
            my=y+h/2
            if(mx<mxa+MyApp.boyut and mx >mxa-MyApp.boyut 
            and my<mya+MyApp.boyut and my>mya-MyApp.boyut):
                self.layout.remove_widget(self.apple)
                self.putApple()
                self.createSnakePart()
                self.seconds-=0.002
                self.point+=1
                break

    def moveSnakeHead(self):
    
        x, y = self.snakeHead.pos
        step = MyApp.boyut

        if self.direction == 'up':
            y += step
        elif self.direction == 'down':
            y -= step
        elif self.direction == 'left':
            x -= step
        elif self.direction == 'right':
            x += step

        self.snakeHead.pos = (x, y)
        self.snakeHead.rect.pos = (x, y)

    def passWalls(self):
        x,y=self.snakeHead.pos
        if(x<0):                        self.snakeHead.pos=(self.width-MyApp.boyut,y)
        if (x>self.width-MyApp.boyut):  self.snakeHead.pos=(0,y)
        if(y<0):                        self.snakeHead.pos=(x,self.height-MyApp.boyut)
        if (y>self.height-MyApp.boyut):  self.snakeHead.pos=(x,0)

    def update(self,dt):

        self.checkEatApple()
        self.updateSnakePartCoordinates()
        self.moveSnakeHead()
        self.passWalls()
        self.checkEatItself()
        
        

    def build(self):
        if(self.playAgain==True):
            self.btn1.text="Tekrar Oyna"
        else:
            self.btn1.text="Oyuna Başla"
        self.btn1.size_hint=(None,None)
        self.btn1.size=(100,30)
        self.btn1.pos=(110,350)
        self.layout.add_widget(self.btn1)

        self.btn2.text="Çıkış"
        self.btn2.size_hint=(None,None)
        self.btn2.size=(100,30)
        self.btn2.pos=(250,350)
        self.layout.add_widget(self.btn2)

        self.btn1.bind(on_press=self.btn1_clicked)
        self.btn2.bind(on_press=self.btn2_clicked)
        return self.layout
        
        

        

    def btn1_clicked(self,instance):
        self.gameOver=False
        self.layout.remove_widget(self.btn1)
        self.layout.remove_widget(self.btn2)
        self.putApple()
        self.putSnakeHead()
        self.event=Clock.schedule_interval(self.update, 0.1)
        Window.bind(on_key_down=self.determineDirection)
        self.direction=""
        

    def btn2_clicked(self,instance):
        App.get_running_app.stop()


class SnakeBlock(Widget):
    def __init__(self, pos=(0,0)):
        super().__init__()

       
        self.size = (MyApp.boyut, MyApp.boyut)  
        self.pos = pos  

        
        with self.canvas:
            Color(0, 0, 0)  
            self.rect = Rectangle(pos=self.pos, size=self.size)

class Apple(Widget):
    def __init__(self, pos=(0,0)):
        super().__init__()

        
        self.size = (MyApp.boyut, MyApp.boyut)  
        self.pos = pos  

        
        with self.canvas:
            Color(1, 0, 0)  
            self.ellipse = Ellipse(pos=self.pos, size=self.size)    

        

if __name__ == "__main__":
    MyApp().run()





