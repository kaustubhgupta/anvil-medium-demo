from ._anvil_designer import homeTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import datetime

class home(homeTemplate):

  NA = "Not Available"
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.

  def username_submit_click(self, **event_args):
    """This method is called when the button is clicked"""
    username = str(self.username_input.text)
    general_data, language_data = anvil.server.call('fetchStats', username)
    if general_data['photoURL']:
      self.avatarImage.source = general_data['photoURL']
    else:
      self.avatarImage.source = ''
    if general_data['name']:
      self.name.text = general_data['name']
    else:
      self.name.text = home.NA
    if general_data['profileBio']:
      self.bio.text = general_data['profileBio']
    else:
      self.bio.text = home.NA
    self.location.icon = "fa:map-pin"
    if general_data['location']:
      self.location.text = general_data['location']
    else:
      self.location.text = home.NA
    self.twitter.icon = "fa:twitter"
    if general_data['twitterUsername']:
      self.twitter.text = '@' + general_data['twitterUsername']
    else:
      self.twitter.text = home.NA
    self.languagePlot.data = go.Pie(labels=list(language_data.keys()),
                             values=list(language_data.values()),
                             textinfo='label+percent',
                             title='Language Used'
                             )
    

