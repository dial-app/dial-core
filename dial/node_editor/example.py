from dial.node_editor import InputPort, Node, OutputPort


class ValueNode(Node):
    def __init__(self, value=0):
        super().__init__("Value Node")

        # Port configuration
        self.add_output_port("value", OutputPort(port_type=int))
        self.outputs["value"].output_generator = self.return_value

        # Attributes
        self.value = value

    def return_value(self):
        return self.value


class AddNode(Node):
    def __init__(self):
        super().__init__("Addition Node")

        self.add_input_port("op1", InputPort(port_type=int))
        self.add_input_port("op2", InputPort(port_type=int))

        self.add_output_port("result", OutputPort(port_type=int))
        self.outputs["result"].output_generator = self.add_ops

    def add_ops(self):
        op1 = self.inputs["op1"].receive()
        op2 = self.inputs["op2"].receive()

        return op1 + op2


class PrintNode(Node):
    def __init__(self):
        super().__init__("Print Node")

        self.add_input_port("string", InputPort(port_type=int))

    def process(self):
        super().process()

        string_to_print = self.inputs["string"].receive()
        print(string_to_print)


def run_example():
    node_op1 = ValueNode(4)
    node_op2 = ValueNode(3)
    add_node = AddNode()
    print_node = PrintNode()
    print_node_2 = PrintNode()

    node_op1.outputs["value"].connect_to(add_node.inputs["op1"])
    node_op2.outputs["value"].connect_to(add_node.inputs["op2"])

    add_node.outputs["result"].connect_to(print_node.inputs["string"])
    add_node.outputs["result"].connect_to(print_node_2.inputs["string"])

    node_op2.process()
