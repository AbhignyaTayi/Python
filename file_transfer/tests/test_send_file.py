from unittest.mock import Mock, patch  # Import Mock and patch from unittest.mock module
from file_transfer.send_file import (
    send_file,
)  # Import send_file function from your module


# Use the patch decorator to mock the socket and open built-ins
@patch("socket.socket")
@patch("builtins.open")
def test_send_file_running_as_expected(file, sock):
    """
    Test to ensure the send_file function behaves as expected.

    Parameters:
    - file (Mock): Mock object representing the file being sent
    - sock (Mock): Mock object representing the socket connection

    """

    # ===== Initialization =====
    # Create a mock connection
    conn = Mock()
    # Mock the behavior of the socket's accept method
    sock.return_value.accept.return_value = conn, Mock()
    # Mock the behavior of the file read method
    f = iter([1, None])
    file.return_value.__enter__.return_value.read.side_effect = lambda _: next(f)

    # ===== Invoke the Function Under Test =====
    # Call send_file with a mock filename and testing flag
    send_file(filename="mytext.txt", testing=True)

    # ===== Ensurance: Verify the Expected Behavior =====
    # Ensure socket is initialized once
    sock.assert_called_once()
    # Ensure bind, listen, and accept methods are called once on the socket
    sock.return_value.bind.assert_called_once()
    sock.return_value.listen.assert_called_once()
    sock.return_value.accept.assert_called_once()
    # Ensure recv is called once on the connection
    conn.recv.assert_called_once()

    # Ensure the file is opened and read
    file.return_value.__enter__.assert_called_once()
    file.return_value.__enter__.return_value.read.assert_called()

    # Ensure send and close are called once on the connection
    conn.send.assert_called_once()
    conn.close.assert_called_once()

    # Ensure shutdown and close are called once on the socket
    sock.return_value.shutdown.assert_called_once()
    sock.return_value.close.assert_called_once()
