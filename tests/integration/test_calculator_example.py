# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from dial.node_editor import InputPort, Node, OutputPort


class ValueNode(Node):
    def __init__(self, value=0):
        super().__init__("Value Node")

        # Port configuration
        self.add_output_port(OutputPort("value", port_type=int))
        self.outputs["value"].output_generator = self.return_value

        # Attributes
        self.value = value

    def return_value(self):
        return self.value


class AddNode(Node):
    def __init__(self):
        super().__init__("Addition Node")

        self.add_input_port(InputPort("op1", port_type=int))
        self.add_input_port(InputPort("op2", port_type=int))

        self.add_output_port(OutputPort("result", port_type=int))
        self.outputs["result"].output_generator = self.add_ops

    def add_ops(self):
        op1 = self.inputs["op1"].receive()
        op2 = self.inputs["op2"].receive()

        return op1 + op2


class TypeConversionNode(Node):
    def __init__(self, input_type, output_type):
        super().__init__("Type Conversion Node")

        self.input_type = input_type
        self.output_type = output_type

        self.add_input_port(InputPort("input", port_type=input_type))

        self.add_output_port(OutputPort("output", port_type=output_type))
        self.outputs["output"].output_generator = self.convert_type

    def convert_type(self):
        return self.output_type(self.inputs["input"].receive())


class PrintNode(Node):
    def __init__(self):
        super().__init__("Print Node")

        self.add_input_port(InputPort("value", port_type=str))

    def process(self):
        super().process()

        string_to_print = self.inputs["value"].receive()
        print(string_to_print)


def test_calculator_example():
    #                             Graph visualization
    #
    #   node_op1 ("value")                                     ("value") print_node_1
    #                \                                            /
    #              ("op1")                                       /
    #                  add_node ("result") - ("input") conv ("output")
    #              ("op2")                                       \
    #                /                                            \
    #   node_op2 ("value")                                   ("value") print_node_2

    # Create Nodes
    node_op1 = ValueNode(4)
    node_op2 = ValueNode(3)

    add_node = AddNode()
    int_to_str_node = TypeConversionNode(input_type=int, output_type=str)

    print_node_1 = PrintNode()
    print_node_2 = PrintNode()

    # Add connections
    node_op1.outputs["value"].connect_to(add_node.inputs["op1"])
    node_op2.outputs["value"].connect_to(add_node.inputs["op2"])

    add_node.outputs["result"].connect_to(int_to_str_node.inputs["input"])

    int_to_str_node.outputs["output"].connect_to(print_node_1.inputs["value"])
    int_to_str_node.outputs["output"].connect_to(print_node_2.inputs["value"])

    add_node.process()

    assert add_node.add_ops() == 7

    assert print_node_1.inputs["value"].receive() == "7"
    assert print_node_2.inputs["value"].receive() == "7"
