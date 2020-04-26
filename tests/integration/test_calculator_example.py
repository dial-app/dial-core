# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from dial_core.node_editor import Node


class ValueNode(Node):
    def __init__(self, value=0):
        super().__init__("Value Node")

        # Port configuration
        self.add_output_port(name="value", port_type=int)
        self.outputs["value"].set_generator_function(self._generate_value)

        # Attributes
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

        self.outputs["value"].send()

    def _generate_value(self):
        return self.value


class AddNode(Node):
    def __init__(self):
        super().__init__("Addition Node")

        self.add_input_port(name="op1", port_type=int)
        self.add_input_port(name="op2", port_type=int)

        self.add_output_port(name="result", port_type=int)

        self.inputs["op1"].triggers(self.outputs["result"])
        self.inputs["op2"].triggers(self.outputs["result"])

        self.outputs["result"].set_generator_function(self.add_ops)

    def add_ops(self):
        value_op1 = self.inputs["op1"].receive()
        value_op2 = self.inputs["op2"].receive()
        result = value_op1 + value_op2

        return result


class TypeConversionNode(Node):
    def __init__(self, input_type, output_type):
        super().__init__("Type Conversion Node")

        self.input_type = input_type
        self.output_type = output_type

        self.add_input_port(name="input", port_type=input_type)
        self.add_output_port(name="output", port_type=output_type)

        self.inputs["input"].triggers(self.outputs["output"])
        self.outputs["output"].set_generator_function(self._convert_type)

    def _convert_type(self):
        return self.output_type(self.inputs["input"].receive())


class PrintNode(Node):
    def __init__(self):
        super().__init__("Print Node")

        self.add_input_port(name="value", port_type=str)
        self.inputs["value"].set_processor_function(self._print_value)

    def print_input(self):
        value = self.inputs["value"].receive()
        self._print_value(value)

    def _print_value(self, value):
        print(value)


def test_calculator_example(capsys):
    #                             Graph visualization
    #
    #   node_op1 ("value")                                     ("value") print_node_1
    #                \                                            /
    #              ("op1")                                       /
    #                  add_node ("result") - ("input") conv ("output")
    #              ("op2")                         (int -> str)  \
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

    assert add_node.add_ops() == 7

    add_node.outputs["result"].connect_to(int_to_str_node.inputs["input"])
    int_to_str_node.outputs["output"].connect_to(print_node_1.inputs["value"])

    captured = capsys.readouterr()
    assert "7\n" == captured.out

    node_op1.value = 7
    captured = capsys.readouterr()
    assert "10\n" == captured.out

    int_to_str_node.outputs["output"].connect_to(print_node_2.inputs["value"])

    captured = capsys.readouterr()
    assert "10\n" == captured.out
