from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty, DictProperty
from kivy.event import EventDispatcher
import random

# Truth and dare questions
DARE_QUESTIONS = [
    "Do your best impression of someone in the room.",
    "Serenade us with a song for 1 minute.",
    "Draw a funny picture with a marker on your face.",
    "Hold hands with the person next to you for 3 minutes.",
    "Post an embarrassing photo on your status.",
    "Text a random person in your contacts saying 'Ilove you.'",
    "Speak in an accent of your choice until your next turn.",
    "Do your best chicken dance.",
    "Give a peck to the most attractive person in the room.",
]

TRUTH_QUESTIONS = [
    "What's the most embarrassing thing you have ever done?",
    "Name the most attractive person in the room.",
    "Who was your first crush, and what happened?",
    "Have you ever lied to get out of trouble? If yes, what was the lie?",
    "What is the weirdest dream you have ever had?",
    "What is the most childish thing you still do?",
    "What's the weirdest thing that ever happened on a date?",
    "Who was your first love?",
    "Do you believe in love at first sight?",
    "What's your idea of a perfect date?",
    "What is the best advice you have ever received about love?",
    "What's something you have done that you never told your parents?",
]

# Global Theme Manager
class ThemeManager(EventDispatcher):
    theme = StringProperty("light")  # Default theme
    themes = DictProperty({
        "light": {"bg": [1, 1, 1, 1], "text": [0, 0, 0, 1]},
        "dark": {"bg": [0.2, 0.2, 0.2, 1], "text": [1, 1, 1, 1]},
    })

    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"

    def get_colors(self):
        return self.themes[self.theme]

# Initialize the theme manager
theme_manager = ThemeManager()

# Unified Screen
class UnifiedScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=10, spacing=10, size_hint=(1, None))
        self.layout.bind(minimum_height=self.layout.setter('height'))

        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.scroll_view.add_widget(self.layout)

        self.label = Label(text="Enter the number of players:", size_hint=(1, None), height=50)
        self.input = TextInput(hint_text="E.g., 3", multiline=False, input_filter="int", size_hint=(1, None), height=50)
        self.start_button = Button(text="Start Game", on_press=self.start_game, size_hint=(1, None), height=50)
        self.toggle_button = Button(text="Toggle Theme", on_press=self.toggle_theme, size_hint=(1, None), height=50)

        self.layout.add_widget(self.label)
        self.layout.add_widget(self.input)
        self.layout.add_widget(self.start_button)
        self.layout.add_widget(self.toggle_button)
        self.add_widget(self.scroll_view)

        # Background instructions
        with self.canvas.before:
            self.bg_color = Color(*theme_manager.get_colors()["bg"])
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)

        # Bind the size and position changes to update the background
        self.bind(size=self.update_background, pos=self.update_background)

        # Bind to theme changes
        theme_manager.bind(theme=self.on_theme_change)

    def toggle_theme(self, instance):
        theme_manager.toggle_theme()

    def on_theme_change(self, instance, value):
        self.apply_theme()

    def apply_theme(self):
        # Apply background and text colors based on the current theme
        colors = theme_manager.get_colors()
        self.bg_color.rgba = colors["bg"]  # Update the background color
        self.label.color = colors["text"]

    def update_background(self, *args):
        # Update the background rectangle when the screen size or position changes
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def start_game(self, instance):
        try:
            num_players = int(self.input.text)
            if num_players > 0:
                self.manager.num_players = num_players
                self.manager.current = "game_screen"
            else:
                self.label.text = "Please enter a valid number greater than 0."
        except ValueError:
            self.label.text = "Please enter a valid number."

    def on_enter(self):
        self.apply_theme()

# Screen for playing the game
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=10, spacing=10, size_hint=(1, None))
        self.layout.bind(minimum_height=self.layout.setter('height'))

        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.scroll_view.add_widget(self.layout)

        self.label = Label(text="Chose truth or dare?", size_hint=(1, None), height=50)
        self.truth_button = Button(text="Truth", on_press=self.choose_truth, size_hint=(1, None), height=50)
        self.dare_button = Button(text="Dare", on_press=self.choose_dare, size_hint=(1, None), height=50)
        self.next_player_button = Button(text="Next Player", on_press=self.next_player, disabled=True, size_hint=(1, None), height=50)
        self.exit_button = Button(text="Back", on_press=self.exit_game, size_hint=(1, None), height=50)

        self.layout.add_widget(self.label)
        self.layout.add_widget(self.truth_button)
        self.layout.add_widget(self.dare_button)
        self.layout.add_widget(self.next_player_button)
        self.layout.add_widget(self.exit_button)
        self.add_widget(self.scroll_view)

        self.current_player_index = 0

        # Background instructions
        with self.canvas.before:
            self.bg_color = Color(*theme_manager.get_colors()["bg"])
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)

        # Bind the size and position changes to update the background
        self.bind(size=self.update_background, pos=self.update_background)

        # Bind to theme changes
        theme_manager.bind(theme=self.on_theme_change)

    def on_theme_change(self, instance, value):
        self.apply_theme()

    def apply_theme(self):
        # Apply background and text colors based on the current theme
        colors = theme_manager.get_colors()
        self.bg_color.rgba = colors["bg"]  # Update the background color
        self.label.color = colors["text"]

    def update_background(self, *args):
        # Update the background rectangle when the screen size or position changes
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def on_enter(self):
        self.update_player()
        self.apply_theme()

    def update_player(self):
        self.next_player_button.disabled = True
        self.truth_button.disabled = False
        self.dare_button.disabled = False
        self.label.text = f"Player {self.current_player_index + 1}'s turn!."
        self.label.markup = True

    def choose_truth(self, instance):
        self.label.text = f"Truth: {random.choice(TRUTH_QUESTIONS)}"
        self.truth_button.disabled = True
        self.dare_button.disabled = True
        self.next_player_button.disabled = False

    def choose_dare(self, instance):
        self.label.text = f"Dare: {random.choice(DARE_QUESTIONS)}"
        self.truth_button.disabled = True
        self.dare_button.disabled = True
        self.next_player_button.disabled = False

    def next_player(self, instance):
        self.current_player_index = (self.current_player_index + 1) % self.manager.num_players
        self.update_player()

    def exit_game(self, instance):
        self.manager.current = "unified_screen"

# App with Unified Screen
class TruthOrDareApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(UnifiedScreen(name="unified_screen"))
        sm.add_widget(GameScreen(name="game_screen"))
        return sm

if __name__ == "__main__":
    TruthOrDareApp().run()