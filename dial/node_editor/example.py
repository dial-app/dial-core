from dial.node_editor import InputPort, Node, OutputPort


class ValueNode(Node):
    def __init__(self, value=0):
        super().__init__("Value Node")

        # Port configuration
        self.add_output("value", OutputPort(port_type=int))
        self.outputs["value"].processing_function = self.return_value

        # Attributes
        self.value = value

    def return_value(self):
        return self.value


class AddNode(Node):
    def __init__(self):
        super().__init__("Addition Node")

        self.add_input("op1", InputPort(port_type=int))
        self.add_input("op2", InputPort(port_type=int))

        self.add_output("result", OutputPort(port_type=int))
        self.outputs["result"].processing_function = self.add_inputs

    def add_inputs(self):
        op1 = self.inputs["op1"].receive()
        op2 = self.inputs["op2"].receive()

        return op1 + op2


class PrintNode(Node):
    def __init__(self):
        super().__init__("Print Node")

        self.add_input("string", InputPort(port_type=int))

    def process(self):
        string_to_print = self.inputs["string"].receive()

        print(string_to_print)


def run_example():
    node_op1 = ValueNode(2)
    node_op2 = ValueNode(3)
    add_node = AddNode()
    print_node = PrintNode()

    node_op1.outputs["value"].connect_to(add_node.inputs["op1"])
    node_op2.outputs["value"].connect_to(add_node.inputs["op2"])

    add_node.outputs["result"].connect_to(print_node.inputs["string"])

    print_node.process()

    print("Example")
