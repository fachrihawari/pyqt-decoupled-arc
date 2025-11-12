from edifice import App, Label, TextInput, HBoxView, Window, Button, component, use_state

@component
def MyApp(self):
    open, set_open = use_state(False)

    with Window(): # Top of every App must be a Window
        with HBoxView():
            Label("Measurement in meters:")
            if open:
              TextInput("")
            Label("Measurement in feet:")

            Button(
              title="Add One",
              on_click = lambda _event: set_open(not open)
            )

if __name__ == "__main__":
    App(MyApp()).start()