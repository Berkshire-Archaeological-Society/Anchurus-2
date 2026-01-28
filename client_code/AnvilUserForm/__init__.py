from ._anvil_designer import AnvilUserFormTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import Global
from ..Validation import Validator

class AnvilUserForm(AnvilUserFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.validator = Validator()
    # set validation on fields
    self.validator.regex(component=self.user_email_value,
                         events=['lost_focus', 'change'],
                         pattern="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
                         required=True,
                         message="Please enter a correct email address")
    self.validator.regex(component=self.initials,
                         events=['lost_focus', 'change'],
                         pattern="^[A-Z]{2}[a-z0-9]$",
                         required=True,
                         message="Please enter the two letter initials of the user, followed by a lowercase letter or digit")
    #
    self.user_role_value.items = Global.system_user_role_options
    self.user_status_value.items = Global.user_status_options
    print(Global.action,Global.user_items["email"])
    if Global.action == "Edit AnvilUser":
      print(Global.action,Global.user_items["email"])
      self.user_email_value.text = Global.user_items["email"]
      self.user_email_value.enabled = False
      #self.user_email_value.foreground = "#ffffff"
      self.firstname.text = Global.user_items["firstname"]
      self.lastname.text = Global.user_items["lastname"]
      if Global.user_items["systemrole"] is None:
        self.user_role_value.selected_value = "None"
      else:
        self.user_role_value.selected_value = Global.user_items["systemrole"]
      Global.user_role = Global.user_items["systemrole"]
      if Global.user_items["enabled"]:
        Global.user_status = True
        self.user_status_value.selected_value = "True"
      else:
        Global.user_status = False
        self.user_status_value.selected_value = "False"
      self.initials.enabled = True
      self.initials.text = Global.user_items["initials"]
  
    #validate 

  def user_role_value_change(self, **event_args):
    """This method is called when an item is selected"""
    #print("Role selected is ",self.user_role_value.selected_value)
    Global.system_user_role = self.user_role_value.selected_value
    pass

  def user_status_value_change(self, **event_args):
    """This method is called when an item is selected"""
    #print("Status selected is ",self.user_status_value.selected_value)
    if self.user_status_value.selected_value == "True":
      Global.user_status = True
    else:
      Global.user_status = False
    pass

  def initials_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    Global.user_initials = self.initials.text
    pass

  def submit_changes_click(self, **event_args):
    """This method is called when the button is clicked"""
    #print("New values for ",Global.user_items["email"], ": ", Global.user_role,Global.user_status)
    Global.username = self.user_email_value.text
    Global.user_firstname = self.firstname.text
    Global.user_lastname = self.lastname.text
    Global.user_initials = self.initials.text
    if self.user_status_value.selected_value == "True":
      Global.user_status = True
    else:
      Global.user_status = False
    Global.system_user_role = self.user_role_value.selected_value
    #
    if Global.action == "Edit AnvilUser": 
      msg = anvil.server.call('system_user_update',Global.user_items["email"], Global.system_user_role,Global.user_status,Global.user_initials,Global.user_firstname,Global.user_lastname)
    elif Global.action == "Insert AnvilUser":
      msg = anvil.server.call('system_user_insert',Global.user_items["email"], Global.system_user_role,Global.user_status,Global.user_initials,Global.user_firstname,Global.user_lastname)
    else:
      msg = "Unknown action: " + Global.action
    n = Notification(msg)
    n.show()
    pass

  def firstname_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    Global.user_firstname = self.firstname.text
    pass

  def lastname_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    Global.user_lastname = self.lastname.text
    pass
