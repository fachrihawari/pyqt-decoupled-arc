from edifice import component, Button, HBoxView, VBoxView, Label, TextInput, use_state

@component
def ContactAdd(self, on_save, navigate):
  """Contact add page with form styling.

  on_save: function(new_contact_dict)
  navigate: function(route)
  """
  name, set_name = use_state("")
  phone, set_phone = use_state("")

  # Single root element for this component
  with VBoxView(style={"padding": 20, "max-width": 500}):
    # Page title
    Label(
      text="Add New Contact",
      style={"font-size": "20px", "font-weight": "bold", "color": "#1976d2", "margin-bottom": 20}
    )

    # Form container with white background
    with VBoxView(
      style={
        "background-color": "white",
        "border": "1px solid #e1e4e8",
        "border-radius": "8px",
        "padding": 20,
      }
    ):
      # Name field
      Label(
        text="Name",
        style={"margin-bottom": 6, "font-weight": "bold", "color": "#1a1a1a"}
      )
      TextInput(
        name,
        on_change=set_name,
        style={"margin-bottom": 16, "min-width": 300}
      )

      # Phone field
      Label(
        text="Phone",
        style={"margin-bottom": 6, "font-weight": "bold", "color": "#1a1a1a"}
      )
      TextInput(
        phone,
        on_change=set_phone,
        style={"margin-bottom": 20, "min-width": 300}
      )

      def save(_event=None):
        if name.strip() == "":
          return
        on_save({"name": name, "phone": phone})
        # Clear fields after save
        set_name("")
        set_phone("")
        navigate("list")

      # Action buttons - spacing with margin instead of gap
      with HBoxView():
        Button(
          title="Save",
          on_click=save,
          style={"height": 40, "min-width": 150, "background-color": "#28a745", "margin-right": 10}
        )
        Button(
          title="Cancel",
          on_click=lambda _e: navigate("list"),
          style={"height": 40, "min-width": 150, "background-color": "#6c757d"}
        )

