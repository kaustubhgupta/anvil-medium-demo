from ._anvil_designer import homeTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

class home(homeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.

  def username_submit_click(self, **event_args):
    """This method is called when the button is clicked"""
    username = self.username_input.text
    Notification(username).show()
    
    

