#Requirements

Design and implement an encrypted overlay network that consists of a single network end-point and multiple
clients that can connect to this network. Each client can communicate with other clients as long as these
clients are on the same network.

#Network Design

A high-level design of the network is shown in the figure below. The traffic flows as follows -
• Flow 1 -> This flow occurs every time a new client is started. Each client has a name (e.g.,
client1.c6610.uml.edu, client2.c6610.uml.edu) that it registers with the network.
• Flow 2 -> This flow occurs every 10 seconds on each running client. Each client connects with the
network to retrieve the names of all other clients connected to the network.
• Flow 3 -> This flow occurs every 15 seconds on each running client. Each client establishes a connection
with other clients and sends the message PING to them. Each client responds back with a PONG
