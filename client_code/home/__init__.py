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
    username = str(self.username_input.text)
    general_data, language_data = anvil.server.call('fetchStats', username)
    self.avatarImage.source = general_data['photoURL']
    self.name.text = general_data['name']
    self.bio.text = general_data['profileBio']
    self.location.icon = "fa:map-pin"
    self.location.text = general_data['location']
    self.twitter.icon = "fa:twitter"
    self.twitter.text = '@' + general_data['twitterUsername']
    self.languagePlot.data = go.Pie(labels=list(language_data.keys()),
                             values=list(language_data.values()),
                             textinfo='label+percent',
                             title='Language Used'
                             )
