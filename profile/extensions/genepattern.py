__author__ = 'tabor'
__copyright__ = 'Copyright 2015, Broad Institute'
__version__ = '0.3'
__status__ = 'Beta'


##############################################
# GenePattern Notebook extension for Jupyter #
# Tested with Jupyter 3.x and Python 2.7.x   #
##############################################


from IPython.core.magic import Magics, magics_class, line_magic
from IPython.core.display import display, Javascript
from IPython.html import widgets
from IPython.utils.traitlets import Unicode, Integer
from gp import GPResource
import IPython
import os
import gp
import json
import urllib
import urllib2


@magics_class
class GenePatternMagic(Magics):
    """
    GenePattern Notebook magic commands
    """

    @line_magic
    def get_job(self, line):
        args = line.split(" ")          # GPServer, job number
        if len(args) != 4:
            return 'Incorrect number of args. Need 4: Server URL, username, password, job number'

        server = gp.GPServer(args[0], args[1], args[2])
        job = gp.GPJob(server, int(args[3]))
        return job

    @line_magic
    def get_task(self, line):
        args = line.split(" ")          # GPServer, task name or lsid
        if len(args) != 4:
            return 'Incorrect number of args. Need 4: Server URL, username, password, task name or LSID'

        server = gp.GPServer(args[0], args[1], args[2])
        task = gp.GPTask(server, args[3])
        return task


class GPAuthWidget(GPResource, widgets.DOMWidget):
    """
    A running or completed job on a GenePattern server.

    Contains methods to get the info of the job, and to wait on a running job by
    polling the server until the job is completed.
    """
    _view_name = Unicode('AuthWidgetView', sync=True)  # Define the widget's view

    def __init__(self, uri, **kwargs):
        super(GPAuthWidget, self).__init__(uri)
        widgets.DOMWidget.__init__(self, **kwargs)
        self.info = None

        self.errors = widgets.CallbackDispatcher(accepted_nargs=[0, 1])
        self.on_msg(self._handle_custom_msg)

    def _handle_custom_msg(self, content):
        """
        Handle a msg from the front-end.

        Parameters
        ----------
        content: dict
        Content of the msg.
        """
        if 'event' in content and content['event'] == 'error':
            self.errors()
            self.errors(self)


class GPJobWidget(GPResource, widgets.DOMWidget):
    """
    A running or completed job on a Gene Pattern server.

    Contains methods to get the info of the job, and to wait on a running job by
    polling the server until the job is completed.
    """
    _view_name = Unicode('JobWidgetView', sync=True)  # Define the widget's view
    job_number = Integer(0, sync=True)

    def __init__(self, job, **kwargs):
        super(GPJobWidget, self).__init__(job.uri)
        widgets.DOMWidget.__init__(self, **kwargs)
        self.job_number = job.job_number

        self.errors = widgets.CallbackDispatcher(accepted_nargs=[0, 1])
        self.on_msg(self._handle_custom_msg)

    def _handle_custom_msg(self, content):
        """
        Handle a msg from the front-end.

        Parameters
        ----------
        content: dict
        Content of the msg.
        """
        if 'event' in content and content['event'] == 'error':
            self.errors()
            self.errors(self)


class GPTaskWidget(GPResource, widgets.DOMWidget):
    """
    A running or completed job on a Gene Pattern server.

    Contains methods to get the info of the job, and to wait on a running job by
    polling the server until the job is completed.
    """
    _view_name = Unicode('TaskWidgetView', sync=True)  # Define the widget's view
    lsid = Unicode("", sync=True)
    name = Unicode("", sync=True)

    def __init__(self, task, **kwargs):
        super(GPTaskWidget, self).__init__(task.uri)
        widgets.DOMWidget.__init__(self, **kwargs)

        if self.is_uri_lsid(task.uri):
            self.lsid = task.uri
        else:
            self.name = task.uri

        self.errors = widgets.CallbackDispatcher(accepted_nargs=[0, 1])
        self.on_msg(self._handle_custom_msg)

    def _handle_custom_msg(self, content):
        """
        Handle a msg from the front-end.

        Parameters
        ----------
        content: dict
        Content of the msg.
        """
        if 'event' in content and content['event'] == 'error':
            self.errors()
            self.errors(self)

    def is_uri_lsid(self, uri):
        if uri.startswith("urn"):
            return True
        else:
            return False


def download_client_files():
    """
    Checks for the presence of all necessary client-side files for the
    extension, and downloads copies from a CDN if necessary.
    """

    # Get the directory and lazily create
    client_dir = IPython.utils.path.locate_profile() + '/static/genepattern'
    if not os.path.exists(client_dir):
        os.makedirs(client_dir)

    # Get the necessary file list in JSON
    list_url = 'https://api.github.com/repos/genepattern/genepattern-notebook/contents/profile/profile_default/static/genepattern'
    try:
        response = urllib2.urlopen(list_url)
    except:
        # This is likely a forbidden error from overuse of the GitHub API, ignore error
        return
    list_data = json.load(response)

    # Loop over list, downloading if necessary
    for file_data in list_data:
        file_name = file_data['name']
        file_url = file_data['download_url']
        file_path = client_dir + '/' + file_name
        # Check and download
        if not os.path.exists(file_path):
            urllib.urlretrieve(file_url, file_path)


def load_client_files():
    client_dir = IPython.utils.path.locate_profile() + '/static/genepattern'

    with open(client_dir + '/loader.js', 'r') as loader:
        loader_text = loader.read()
    display(Javascript(loader_text))


# The `ipython` argument is the currently active `InteractiveShell`
# instance, which can be used in any way. This allows you to register
# new magics or aliases, for example.
def load_ipython_extension(ipython):
    # Register magics
    ipython.register_magics(GenePatternMagic)

    # Check for presence of required client-side files, download if necessary
    download_client_files()

    # Load all required files on the client-side
    load_client_files()