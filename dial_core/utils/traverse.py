# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:


def find_parent_of(obj, instance_type):
    if hasattr(obj, "parent"):
        if isinstance(obj.parent, instance_type):
            return obj.parent

        return find_parent_of(obj.parent, instance_type)

    return None
