
import random
from kivy.config import Config
from kivy.app import App
from kivy.metrics import dp
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty,NumericProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.widget import Widget
from kivy.graphics.context_instructions import Color
from kivy.graphics import Line,Quad,Triangle
from kivy.properties import Clock
from kivy.core.window import Window
from kivy import platform
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.audio import SoundLoader


Builder.load_file("menu.kv")

class MainWidget(RelativeLayout):
    from transforms import transform,transform_2D,transform_perspective
    from user_actions import keyboard_closed,on_keyboard_down,on_keyboard_up,on_touch_down,on_touch_up
    perspectiver_pont_x=NumericProperty(0)
    perspectiver_pont_y=NumericProperty(0)
    menuwidget=ObjectProperty()
    menu_title=StringProperty("G   A   L   A   X   Y")
    menu_button_title=StringProperty("START")
    score_txt=StringProperty()

    curent_ofsset_y=0
    curent_y_loop=0
    SPEED=.8         

    SPEED_X=.8
    curent_speed_x=0
    curent_ofsset_x=0
    

    
    V_NB_LINES=8
    V_LINES_SPACING=.4 # pourcentage de la largeur de l'ecran
    vertical_lines=[]

    H_NB_LINES=8
    H_LINES_SPACING=.15 # pourcentage de la largeur de l'ecran
    horizontal_lines=[]
    
    NB_TILES=16
    tiles=[]
    tiles_coordinates=[]
     
    SHIP_WIDTH=.1
    SHIP_HEIGHT=0.035
    SHIP_BASE_Y=0.04
    ship=None
    ship_coordinate=[(0,0),(0,0),(0,0)]

    stat_game_over=False
    state_game_has_started=False

    sound_bigin=None
    sound_galaxy=None
    sound_gameover_impact=None
    sound_gameover_voice=None
    sound_music1=None
    sound_restart=None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #print("INIT W:"+str(self.width)+" H:"+str(self.height))
        self.init_audio()
        self.init_vertical_lines()
        self.init_horizontal_lines()
        self.init_tile()
        self.init_ship()
        self.rest_game()
        
        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)
        Clock.schedule_interval(self.update, 1.0/60.0)

        self.sound_galaxy.play()

    def init_audio(self):
        self.sound_bigin=SoundLoader.load("audio/begin.wav")
        self.sound_galaxy=SoundLoader.load("audio/galaxy.wav")
        self.sound_gameover_impact=SoundLoader.load("audio/gameover_impact.wav")
        self.sound_gameover_voice=SoundLoader.load("audio/gameover_voice.wav")
        self.sound_music1=SoundLoader.load("audio/music1.wav")
        self.sound_restart=SoundLoader.load("audio/restart.wav")

        self.sound_music1.volume=1
        self.sound_bigin.volume=.25
        self.sound_galaxy.volume=.25
        self.sound_restart.volume=.25
        self.sound_gameover_impact.volume=.6



    def rest_game(self):
        self.curent_ofsset_y=0
        self.curent_y_loop=0
        self.curent_speed_x=0
        self.curent_ofsset_x=0
        self.tiles_coordinates=[]
        self.score_txt="SCORE: "+str(self.curent_y_loop)
        self.pre_file_tiles_coordinates()
        self.generate_tiles_coordinates()
        self.stat_game_over=False
    def is_desktop(self):
        if platform in ('linux','windows','macosx'):
            return True
    

    def init_ship(self):
        with self.canvas:
            Color(0,0,0)
            self.ship=Triangle()

    def update_ship(self):
        center_x=self.width/2
        base_y=self.SHIP_BASE_Y*self.height
        half_width=self.SHIP_WIDTH*self.width/2
        ship_height=self.SHIP_HEIGHT*self.height
        #    2
        # 1      3
        self.ship_coordinate[0]=(center_x-half_width,base_y)
        self.ship_coordinate[1]=(center_x,base_y+ship_height)
        self.ship_coordinate[2]=(center_x+half_width,base_y)
        x1,y1=self.transform(*self.ship_coordinate[0])
        x2,y2=self.transform(*self.ship_coordinate[1])
        x3,y3=self.transform(*self.ship_coordinate[2])
        self.ship.points=[x1,y1,x2,y2,x3,y3]
    
    def check_ship_collision(self):
        for i in range(0,len(self.tiles_coordinates)):
            ti_x,ti_y=self.tiles_coordinates[i]
            if ti_y>self.curent_y_loop+1:
                return False
            if self.check_ship_collision_with_tile(ti_x,ti_y):
                return True
        return False

    def check_ship_collision_with_tile(self,ti_x,ti_y):
        xmin,ymin=self.get_tile_coordinates(ti_x,ti_y)
        xmax,ymax=self.get_tile_coordinates(ti_x+1,ti_y+1)
        for i in range(0,3):
            px,py=self.ship_coordinate[i]
            if xmin<=px<=xmax and ymin<=py<=ymax:
                return True
        return False
        
    def init_tile(self):
        with self.canvas:
            Color(1,1,1)
            for i in range(0,self.NB_TILES):
                self.tiles.append(Quad())
    def pre_file_tiles_coordinates(self):
        for i in range(0,10):
            self.tiles_coordinates.append((0,i))

    
    def generate_tiles_coordinates(self):
        last_x=0
        last_y=0
        if len(self.tiles_coordinates)>0:
            last_coordinate=self.tiles_coordinates[-1]
            last_x=last_coordinate[0]
            last_y=last_coordinate[1]+1
        
        for i in range(len(self.tiles_coordinates)-1,-1,-1):
            if self.tiles_coordinates[i][1]<self.curent_y_loop:
                del self.tiles_coordinates[i]

        

        for i in range(len(self.tiles_coordinates),self.NB_TILES):
            r=random.randint(0,2)
            start_index=-int(self.V_NB_LINES/2)+1
            end_index=start_index+self.V_NB_LINES-1

            if last_x<=start_index:
                r=1
            if last_x>=end_index:
                r=2
            self.tiles_coordinates.append((last_x,last_y))
            
            if r==1:
                last_x+=1
                self.tiles_coordinates.append((last_x,last_y))
                last_y+=1
                self.tiles_coordinates.append((last_x,last_y))
            elif r==2:
                last_x-=1
                self.tiles_coordinates.append((last_x,last_y))
                last_y+=1
                self.tiles_coordinates.append((last_x,last_y))
            last_y+=1

    def init_vertical_lines(self):
        with self.canvas:
            Color(1,1,1)
            #self.line=Line(points=[100,0,100,100])
            for i in range(0,self.V_NB_LINES):
                self.vertical_lines.append(Line())
    def get_line_x_from_index(self,index):
        central_line_x=self.perspectiver_pont_x
        spacing=self.V_LINES_SPACING*self.width
        ofsset=index-0.5 
        line_x=central_line_x+ofsset*spacing + self.curent_ofsset_x 
        return line_x   

    def get_line_y_from_index(self,index):
        spacing_y=self.H_LINES_SPACING * self.height
        line_y=index*spacing_y-self.curent_ofsset_y
        return line_y

    def get_tile_coordinates(self,ti_x,ti_y):
        ti_y=ti_y-self.curent_y_loop
        x=self.get_line_x_from_index(ti_x)
        y=self.get_line_y_from_index(ti_y)
        return x,y
    

    def upadate_tiles(self):
        for i in range(0,self.NB_TILES):
            tile=self.tiles[i]
            tile_coodinates=self.tiles_coordinates[i]
            xmin,ymin=self.get_tile_coordinates(tile_coodinates[0],tile_coodinates[1])
            xmax,ymax=self.get_tile_coordinates(tile_coodinates[0]+1,tile_coodinates[1]+1)

            x1,y1=self.transform(xmin,ymin)
            x2,y2=self.transform(xmin,ymax)
            x3,y3=self.transform(xmax,ymax)
            x4,y4=self.transform(xmax,ymin)

            tile.points=[x1,y1,x2,y2,x3,y3,x4,y4]
        
    def update_vertical_line(self):
        start_index=-int(self.V_NB_LINES/2)+1
        for i in range(start_index,start_index+self.V_NB_LINES):
            line_x=self.get_line_x_from_index(i)
            x1,y1=self.transform(line_x,0)
            x2,y2=self.transform(line_x,self.height)
            self.vertical_lines[i].points=[x1,y1,x2,y2]
            
    def init_horizontal_lines(self):
        with self.canvas:
            Color(1,1,1)
            #self.line=Line(points=[100,0,100,100])
            for i in range(0,self.H_NB_LINES):
                self.horizontal_lines.append(Line())
    
    def update_horizontal_line(self):
        start_index=-int(self.V_NB_LINES/2)+1
        end_index=start_index+self.V_NB_LINES-1

        xmin=self.get_line_x_from_index(start_index)
        xmax=self.get_line_x_from_index(end_index)
        for i in range(0,self.H_NB_LINES):
            line_y=self.get_line_y_from_index(i)
            x1,y1=self.transform(xmin,line_y)
            x2,y2=self.transform(xmax,line_y)
            self.horizontal_lines[i].points=[x1,y1,x2,y2]


    
    def update(self,dt):
        time_factor=dt*60
        self.update_vertical_line()
        self.update_horizontal_line()
        self.upadate_tiles()
        self.update_ship()
        if not self.stat_game_over and self.state_game_has_started:
            speed_y=self.SPEED*self.height/100
            self.curent_ofsset_y+=speed_y*time_factor

            spacing_y=self.H_LINES_SPACING * self.height
            while self.curent_ofsset_y>spacing_y:
                self.curent_ofsset_y-=spacing_y
                self.curent_y_loop+=1
                self.score_txt="SCORE: "+str(self.curent_y_loop)
                self.generate_tiles_coordinates()
            speed_x=self.curent_speed_x*self.width/100
            self.curent_ofsset_x+=speed_x*time_factor

        

        if not self.check_ship_collision():
            self.stat_game_over=True
            self.menu_title="G  A  M  E     O  V  E  R"
            self.menu_button_title="RESTART"
            self.menuwidget.opacity=1
            self.sound_music1.stop()
            self.sound_gameover_impact.play()
            Clock.schedule_interval(self.play_voice_game_over, 3)
            #print("Game Over")

    def play_voice_game_over(self,dt):
        if self.stat_game_over:
            self.sound_gameover_voice.play()
        
    
    def on_menu_button_pressed(self):
       # print("BUTTON")
       if self.stat_game_over:
           self.sound_restart.play()
       else:
            self.sound_bigin.play()
       self.sound_music1.play()
       self.rest_game()
       self.state_game_has_started=True
       self.menuwidget.opacity=0


   



class GalaxyApp(App):
    pass


GalaxyApp().run()