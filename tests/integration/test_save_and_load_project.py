# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from dial_core.node_editor import Node
from dial_core.project import ProjectManagerFactory


class TestNode(Node):
    def __init__(self, title: str = "Foo"):
        super().__init__(title)


def test_save_and_load_project():
    # Setup initial project with one node
    project_manager = ProjectManagerFactory()

    active_project = project_manager.active

    test_node = TestNode()

    active_project.scene.add_node(test_node)

    assert test_node in active_project.scene

    # Save project to memory
    project_manager.save_project_as("foo.dial")

    # Load project from memory
    opened_project = project_manager.open_project("foo.dial")

    # The last and new projects are different...
    assert active_project is not opened_project

    # ...but the scenes content should be the same
    assert active_project == opened_project
