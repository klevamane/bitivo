""" mock flask_sse before using it"""
from flask_sse import sse
from api.utilities.helpers.env_resource_adapter import adapt_resource_to_env

def publish(message, event):
    """
       method to mock sse.publish when environment is testing and 
       run the actuall sse.publish when in development and production.
       args:
           message: data to send to a stream
           event: what to listen for on the client side 
    """
    sse_publish = adapt_resource_to_env(sse.publish)
    sse_publish(message, event)
