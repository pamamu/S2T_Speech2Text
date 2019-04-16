import socket


def get_ip():
    """
    TODO DOCUMENTATION
    :return:
    """
    return socket.gethostbyname(socket.gethostname())
