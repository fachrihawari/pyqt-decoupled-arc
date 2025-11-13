import sys
from edifice import App, Window, component, use_state
from PyQt6.QtWidgets import QApplication
from pages.contact_list import ContactList
from pages.contact_add import ContactAdd



@component
def MyApp(self):
  # route: 'list' or 'add'
  route, set_route = use_state("list")
  contacts, set_contacts = use_state([])

  def navigate(r):
    set_route(r)

  def add_contact(c):
    set_contacts(list(contacts) + [c])

  with Window(title="Contact Manager"):

    # Render the selected page
    if route == "list":
      ContactList(contacts=contacts, navigate=navigate)
    elif route == "add":
      ContactAdd(on_save=add_contact, navigate=navigate)


if __name__ == "__main__":
  app = QApplication(sys.argv)

  App(
    root_element=MyApp(),
    create_application=False,
    qapplication=app,
  ).start()