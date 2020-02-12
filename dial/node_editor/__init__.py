# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from .input_port import InputPort
from .node import Node
from .output_port import OutputPort
from .port import Port

__all__ = ["Node", "Port", "InputPort", "OutputPort"]

"""
scene = NodeEditorScene()
view = NodeEditorView()
view.setScene(scene)

node_a = Node(title="a")
node_b = Node(title="b")

dataset_node.outputs["train"].connect_to(training_node.input["dataset"])

dataset_node.outputs["train"].disconnect_from(training_node.input["dataset"])

# How can we check if two ports can be connected?

* When the port is defined, it already knows its type
(Doesn't has sense to change port types on the fly I guess)

foo_a = Port(type=int)
foo_b = Port(type=str)

foo_a.connect_to(foo_b) # CAN'T, because types aren't compatible

* What happens with user defined types?

bar_a = Port(type=ClassA)
bar_b = Port(type=ClassB)

bar_a.connect_to(bar_b) # CAN'T, because types aren't compatible even if the classes do
the same thing.

Solution 1: Prevent using user defined classes, and stick to primitive ones.
Solution 2: Make types explicitly convertible.
ClassA => convertible to ["ClassB", "ClassC"]...
(Requires the mantainer to constantly check if the classes are still compatible)

Solution 3 (DISCARDED): Make types compatible if they share their interface.

ClassA:
    def foo():

ClassB:
    def foo()

bar_a.connect_to(bar_b) # CAN, because ClassA and ClassB have same interface
(is it really a good solution? Can introduce a lot of unintended errors. What if a class
also have more methods?)

NOTE: Methods on an input port aren't used (Only on an output port)

Final: For now,  go to the Solution 1 and explicit types shared by libraries instead of
between plugins (For example, send a Sequential() Keras dataset instead of a custom
Dataset class).



Let's say a node with 1 inputs and 2 outputs has a method process:
  def process():
    data_1 = self.input["a"].receive()

    self.outputs["foo"].send(data_1)
    self.outputs["bar"].send(data_1 * 2)

scene.addNode(dataset_node)
scene.addNode(training_node)


### Flowing data from nodes

Example: We're creating a Calculator using Nodes

AddNode = Node(inputs={"op1": Port(port_type=int), "op2": Port(port_type=int)},
                outputs={"result": Port(port_type=int)})

NumberNode = Node(outputs={"value": Port(port_type=int)})

# How is this node going to process its data?

* Graph is started from any node (Change later?)
* All input ports can't allow multiple connections.

* What is clear: process should be an abstract class of Node, and let other objects
  subclass it


AHA! Having InputPort and OutputPort reduces confusion on the API

(Inside Port class)
def receive(self):
    return port.connect_to.process_func()

(Inside NumberNode class)
def __init__(self):
    self.value = 5

    self.add_output("value", Port(port_type=int))

    # TODO: Prob check if fun return type is compatible?
    self.outputs["value"].process_func = self.get_value

def get_value(self):
    return self.value

# def process (self):
    pass # No need to define

(Inside AddNode class)
def process(self):
   op1 = self.inputs["op1"].receive() # Probably nonblocking functions?
   op2 = self.inputs["op2"].receive()

   # (Check when op1 and op2 are ready)

   result = op1 + op2

(Something like that?)

^^^^ Process from current node backwards

(Inside InputPort class)
def receive(self):
    output_value = self.port_connected_to.get_value()

    return output_value

(Inside OutputPort class)
def send(self):
    return self.processing_function()

(Inside Node class)
def __init__(self):
    self.add_output("value", port_type=int)
    self.outputs["value"].processing_function = self.get_value


"""
