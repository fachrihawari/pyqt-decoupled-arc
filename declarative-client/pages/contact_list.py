from edifice import component, VBoxView, Label, Button
import sys
sys.path.insert(0, '../')
from contexts.contact_manager import use_contact_manager

@component
def ContactList(self, navigate):
  """Simple contact list page with improved styling.
  
  This component is self-contained and manages its own data and actions.
  
  navigate: function(route) to change page
  """
  # Get global manager and contacts
  manager, contacts = use_contact_manager()
  
  def delete_contact(contact_id):
    """Delete contact through core business logic"""
    try:
      manager.delete_contact(contact_id)
    except Exception as e:
      print(f"Error deleting contact: {e}")
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
          # Contact info section
          with VBoxView():
            # Contact name - larger and bold
            Label(
              text=f"{c.get('name', 'Unnamed')}",
              style={"font-size": "15px", "font-weight": "bold", "color": "#1a1a1a"}
            )
            
            # Contact email
            if c.get('email'):
              Label(
                text=f"✉️ {c.get('email')}",
                style={"margin-top": 4, "color": "#586069", "font-size": "13px"}
              )
            
            # Contact phone - smaller and gray
            if c.get('phone'):
              Label(
                text=f"📞 {c.get('phone')}",
                style={"margin-top": 2, "color": "#586069", "font-size": "13px"}
              )
          
          # Delete button
          if c.get('id'):
            Button(
              title="🗑️ Delete",
              on_click=lambda _e, contact_id=c['id']: delete_contact(contact_id),
              style={
                "margin-top": 8,
                "padding": "6px 12px",
                "font-size": "12px",
                "background-color": "#dc3545",
              }
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
