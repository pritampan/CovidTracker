import sys
from kivymd.uix.button import MDFloatingActionButtonSpeedDial

sys.path.append("/".join(x for x in __file__.split("/")[:-1]))
from kivy.uix.screenmanager import Screen, NoTransition, CardTransition
from kivy.lang import Builder
import traceback
from kivymd.app import MDApp
from string import Template
import requests

url = "https://api.rootnet.in/covid19-in/stats/latest"
KV = Template('''
Screen:
    MDCard:
        orientation: "vertical"
        padding: "8dp"
        pos_hint: {"center_x": .5, "center_y": .5}
        MDLabel:
            text: "$location"
            theme_text_color: "Secondary"
            size_hint_y: None
            height: self.texture_size[1]
            halign: "center"
            
        Image:
            source: "$image" 

        MDSeparator:
            height: "1dp"
        MDChip:
            pos_hint: {'center_y': 0.5, 'center_x': 0.5}
            label: "confirmedCasesIndian: $confirmedCasesIndian"
            color: .56078431302, .482352906, .435294883, 1
            icon: 'emoticon-sad'
            align: "center"
        MDChip:
            pos_hint: {'center_y': 0.5, 'center_x': 0.5}
            label: "confirmedCasesForeign: $confirmedCasesForeign"
            color: .56078431302, .482352906, .435294883, 1
            icon: 'emoticon-sad'
            align: "center"
        MDChip:
            pos_hint: {'center_y': 0.5, 'center_x': 0.5}
            label: "discharged: $discharged"
            color: .21176470535294, .098039627451, 1, 1
            icon: 'emoticon-happy'
            align: "center"
        MDChip:
            pos_hint: {'center_y': 0.5, 'center_x': 0.5}
            label: 'deaths: $deaths'
            color: 1,0,0,1
            icon: 'skull-crossbones'
            align: "center"
''')





class HomeScreen(Screen):
    pass


class MainApp(MDApp):
    data = {
        'language-python': 'Python',
        'language-php': 'PHP',
        'language-cpp': 'C++',
    }

    def build(self):
        self.title = 'Corona Realtime Update'
        screen = Screen()
        speed_dial = MDFloatingActionButtonSpeedDial()
        speed_dial.data = self.data
        speed_dial.rotation_root_button = True
        screen.add_widget(speed_dial)
        return Builder.load_file("main.kv")

    def on_start(self):
        try:
            carousel = self.root.ids['home_screen'].ids['carousel_id']
            for state in self.get_statewise_count():
                location = state.get("loc")
                confirmedCasesIndian = state.get('confirmedCasesIndian', 0)
                confirmedCasesForeign = state.get('confirmedCasesForeign', 0)
                discharged = state.get('discharged', 0)
                deaths = state.get('deaths', 0)
                l = Builder.load_string(KV.substitute({"location":location,
                                                       "image" : "images/{0}.png".format(location),
                                                       "confirmedCasesIndian": confirmedCasesIndian,
                                                       "confirmedCasesForeign": confirmedCasesForeign,
                                                       "discharged": discharged,
                                                       "deaths": deaths}))
                carousel.add_widget(l)
            self.change_screen("home_screen", "None")

        except Exception as e:
            traceback.print_exc()
            pass

    def change_screen(self, screen_name, direction='forward', mode=""):
        # Get the screen manager from the kv file
        screen_manager = self.root.ids['screen_manager']
        print(direction, mode)
        # If going backward, change the transition. Else make it the default
        # Forward/backward between pages made more sense to me than left/right
        if direction == 'forward':
            mode = "push"
            direction = 'left'
        elif direction == 'backwards':
            direction = 'right'
            mode = 'pop'
        elif direction == "None":
            screen_manager.transition = NoTransition()
            screen_manager.current = screen_name
            return

        screen_manager.transition = CardTransition(direction=direction, mode=mode)
        screen_manager.current = screen_name

    def get_statewise_count(self):
        response = requests.get(url)
        if response.ok:
            data = response.json().get("data",{}).get("regional")
            return data



if __name__ == '__main__':
    MainApp().run()