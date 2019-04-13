import kivy
import serial
import time
import json
kivy.require('1.10.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.properties import ListProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.animation import Animation


class Gerenciador(ScreenManager):
	
    conection = StringProperty('Conectar')

    def conectar(self, *args):
        global arduino
        if(self.conection == 'Conectar'):
            try:
                arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
            except:
                pass
            if(str(arduino.read() == '0x88')):
                self.conection = 'Desconectar'
        else:
            arduino.close()
            self.conection = 'Conectar'

    def setup(self, *args):
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        pInput = BoxLayout(padding=10, spacing=10)
        pop = Popup(title='Preferências', content=box, size_hint=(None, None), size=(100, 30))

        confirm = Botao(text=self.conection, on_press=self.conectar, on_release=pop.dismiss)
        pInput.add_widget(confirm)

        box.add_widget(pInput)
        anim = Animation(size=(300, 150), duration=0.05, t='out_back')
        anim.start(pop)
        pop.open()

class Menu(Screen):

    username = ''
    eUser = ''
    password = ''
    ePass = ''
    path = ''

    def on_pre_enter(self):
        self.path = App.get_running_app().user_data_dir+'/'
        print(self.path)

    def loadData(self, *args):
        try:
            with open(self.path+'username.json', 'r') as username:
                self.username = json.load(username)
            with open(self.path+'password.json', 'r') as password:
                self.password = json.load(password)
        except FileNotFoundError:
            self.saveData()

    def saveData(self, *args):
        with open(self.path+'username.json', 'w') as username:
            json.dump(self.eUser, username)
        with open(self.path+'password.json', 'w') as password:
            json.dump(self.ePass, password)

    def confirmacao(self, *args):
        box = BoxLayout(orientation = 'vertical', padding=10, spacing=10)
        botoes = BoxLayout(padding=10, spacing=10)
        pop = Popup(title='Deseja mesmo sair?', content=box, size_hint=(None, None), size=(150, 150))

        sim = Botao(text = 'Sim', on_release=App.get_running_app().stop)
        nao = Botao(text = 'Não', on_release=pop.dismiss)
        atencao = Image(source='Imagens/warning.png')

        botoes.add_widget(sim)
        botoes.add_widget(nao)

        box.add_widget(atencao)
        box.add_widget(botoes)

        anim = Animation(size=(300,200), duration=0.05, t='out_back')
        anim.start(pop)
        pop.open()
        return True

    def btAuth(self, user='', pw='', **kwargs):
        self.eUser = user
        self.ePass = pw
        print('Usuário: ' + self.eUser + '    Senha: ' + self.ePass)
        #self.loadData()
        #if((self.eUser == self.username) and (self.ePass == self.password)):
        #App.get_running_app.current = 'tarefas'


class Slides(Screen):
    pass

class Abas(Screen):
    pass

class Botao(ButtonBehavior, Label):
    cor = ListProperty([0.1,0.5,0.3,1])
    corpress = ListProperty([0.3,0.3,0.3,1])
    def __init__(self, **kwargs):
        super(Botao, self).__init__(**kwargs)
        self.atualizar()

    def on_pos(self, *args):
        self.atualizar()

    def on_size(self, *args):
        self.atualizar()

    def on_press(self):
        self.cor,self.corpress = self.corpress,self.cor
        self.atualizar()

    def on_release(self):
        self.cor, self.corpress = self.corpress, self.cor
        self.atualizar()

    def atualizar(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=self.cor)
            Ellipse(size=(self.height, self.height), pos=self.pos)
            Ellipse(size=(self.height, self.height), pos=(self.x + self.width - self.height, self.y))
            Rectangle(size=(self.width - self.height, self.height), pos=(self.x + self.height/2., self.y))

class BtClose(ButtonBehavior, Label):
    cor = ListProperty([1, 1, 1, 1])
    corpress = ListProperty([0.3, 0.3, 0.3, 1])
    def __init__(self, **kwargs):
        super(BtClose, self).__init__(**kwargs)
        self.atualizar()

    def on_size(self, *args):
        self.atualizar()

    def on_pos(self, *args):
        self.atualizar()

    def on_press(self):
        self.cor, self.corpress = self.corpress, self.cor
        self.atualizar()

    def on_release(self):
        self.cor, self.corpress = self.corpress, self.cor
        self.atualizar()

    def atualizar(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=self.cor)
            Rectangle(source='Imagens/delete-button.png', size=(self.height,self.height), pos=(self.x, self.y + 15))
            Color(rgba=(0.1,0.1,0.1,1))
            Rectangle(size=(self.width, 1), pos=(self.x, self.y+self.height+30))
            Rectangle(size=(self.width, 1), pos=(self.pos))

class BtSend(ButtonBehavior, Label):
    def __init__(self, **kwargs):
        super(BtSend, self).__init__(**kwargs)
        self.atualizar()

    def on_size(self, *args):
        self.atualizar()

    def on_pos(self, *args):
        self.atualizar()

    def atualizar(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=(1, 1, 1, 1))
            Rectangle(source='Imagens/send.png', size=(self.height*0.75,self.height*0.75), pos=(self.x+5, self.y+14))
            Color(rgba=(0.1,0.1,0.1,1))
            Rectangle(size=(self.width, 1), pos=(self.x, self.y + self.height))
            Rectangle(size=(self.width, 1), pos=(self.pos))

class Tarefas(Screen):
    tarefas = []
    cmds = []
    path = ''

    initLoad = 0

    def on_pre_enter(self):
        i = 0
        self.path = App.get_running_app().user_data_dir+'/'
        print(self.path)
        self.loadData()
        if (self.initLoad == 0):
            for tarefa in self.tarefas:
                self.ids.box.add_widget(Tarefa(text=tarefa, pText=self.cmds[i]))
                i += 1
            self.initLoad = 1
        Window.bind(on_keyboard=self.voltar)

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltar)

    def voltar(self, window, key, *args):
        if key == 27:
            App.get_running_app().root.current = 'menu'
            return True

    def removeWidget(self, tarefa):
        texto = tarefa.ids.label.text
        text_port = tarefa.ids.lb_cmd.text
        self.ids.box.remove_widget(tarefa)
        self.tarefas.remove(texto)
        self.cmds.remove(text_port)
        self.saveData()

    def loadData(self, *args):
        try:
            with open(self.path+'data.json', 'r') as data:
                self.tarefas = json.load(data)
            with open(self.path+'cmds.json', 'r') as cmds:
                self.cmds = json.load(cmds)
        except FileNotFoundError:
            pass

    def saveData(self, *args):
        with open(self.path+'data.json', 'w') as data:
            json.dump(self.tarefas, data)
        with open(self.path+'cmds.json', 'w') as cmds:
            json.dump(self.cmds, cmds)

    def addWidget(self):
        texto = self.ids.texto.text
        text_port = self.ids.text_port.text
        if(texto != ''):
            pass
        else:
            texto = '[color=ff3333]Sem descrição[/color]'
        if(text_port != ''):
            pass
        else:
            text_port = '[color=ff3333]##[/color]'
        self.ids.box.add_widget(Tarefa(text = texto, pText=text_port))
        self.ids.texto.text = ''
        self.ids.text_port.text = ''
        self.tarefas.append(texto)
        self.cmds.append(text_port)
        self.saveData()

    def comSave(self, *args):
        print('OK')


class Tarefa(BoxLayout):
    def __init__(self, text='', pText='', **kwargs):
        super(Tarefa, self).__init__(**kwargs)
        self.ids.label.text = text
        self.ids.lb_cmd.text = pText

    def cmdSend(self, cmd):
        #if(arduino.is_open):
        cmdSent = cmd + '\n'
        print(cmdSent)
            #arduino.write(cmdSent.encode())
        #else:
            #print('Não Conectado!')


class main(App):
    def build(self):
        self.icon = 'Imagens/icon.png'
        return Gerenciador()

if __name__ == '__main__':
    arduino = serial.Serial()
    main().run()
