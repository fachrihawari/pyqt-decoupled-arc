from edifice import component, VBoxView, Label, Button

@component
def ContactList(self, contacts, navigate):
  """Simple contact list page with improved styling.

  contacts: list of dicts with keys 'name' and 'phone'
  navigate: function(route) to change page
  """
  # Single root element for this component
  with VBoxView(style={"padding": 20}):
    # Page title with larger font and bold styling
    Label(
      text="Contact List",
      style={"font-size": "24px", "font-weight": "bold", "color": "#1976d2", "margin-bottom": 20}
    )

    # Container for contact cards
    if len(contacts) == 0:
      Label(
        text="No contacts yet. Add your first contact!",
        style={"color": "#666", "font-style": "italic"}
      )
    else:
      # Show each contact as a styled card
      for idx, c in enumerate(contacts):
        with VBoxView(
          style={
            "background-color": "white",
            "border": "1px solid #e1e4e8",
            "border-radius": "8px",
            "padding": 12,
            "margin-bottom": 10,
          }
        ):
          # Contact name - larger and bold
          Label(
            text=f"{c.get('name', 'Unnamed')}",
            style={"font-size": "15px", "font-weight": "bold", "color": "#1a1a1a"}
          )
          
          # Contact phone - smaller and gray
          if c.get('phone'):
            Label(
              text=f"📞 {c.get('phone')}",
              style={"margin-top": 4, "color": "#586069", "font-size": "13px"}
            )
    
    # Add contact button at the bottom
    Button(
      title="➕ Add New Contact",
      on_click=lambda _e: navigate("add"),
      style={
        "margin-top": 20,
        "padding": "12px 24px",
        "font-size": "14px",
        "background-color": "#28a745",
      }
    )
