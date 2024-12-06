# this part hopefully allows a user not to call a function like below :
    ## from conn_wizard.src.connection_utility import load_connections
    ## from conn_wizard.src.connection_utility import choose_connection

# but instead like below :
    ## from connection_utility import load_connections
    ## from connection_utility import choose_connection
    ## from connection_manager import main


from .src.connection_utility import (
    load_connections, choose_connection)

from .src.connection_manager import main