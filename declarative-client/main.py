import sys
from edifice import App, Window, component, use_state
from PyQt6.QtWidgets import QApplication
from pages.contact_list import ContactList
from pages.contact_add import ContactAdd

@component
def MyApp(self):
  """
  Main app component - handles routing only.
  Business logic is now encapsulated in each page component.
  """
  # route: 'list' or 'add'
  route, set_route = use_state("list")

  def navigate(r):
    set_route(r)

  with Window(title="Contact Manager"):
    # Render the selected page - components are now self-contained
    if route == "list":
      ContactList(navigate=navigate)
    elif route == "add":
      ContactAdd(navigate=navigate)


if __name__ == "__main__":
  app = QApplication(sys.argv)

  App(
    root_element=MyApp(),
    create_application=False,
    qapplication=app,
  ).start()