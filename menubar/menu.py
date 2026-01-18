# core/menu.py
from collections import defaultdict


class MenuRegistry:
    def __init__(self):
        self._items = defaultdict(list)

    def register(
        self,
        section,
        label,
        url_name=None,
        order=100,
        icon=None,
        parent=None,
        admin_required=False,
    ):
        """
        Register a new menu item.
        section: which menu section (e.g. "main", "user")
        label: text shown in navbar
        url_name: Django URL name to reverse (None if parent only)
        order: sorting order (default 100)
        icon: optional Bootstrap icon class
        parent: label of parent item (for dropdowns)
        """
        self._items[section].append(
            {
                "label": label,
                "url_name": url_name,
                "order": order,
                "icon": icon,
                "admin_required": admin_required,
                "parent": parent,
            }
        )

    def get_items(self, section):
        items = sorted(self._items[section], key=lambda x: x["order"])
        tree = []
        lookup = {}

        for item in items:
            if item["parent"] is None:
                node = {**item, "children": []}
                tree.append(node)
                lookup[item["label"]] = node
            else:
                parent_node = lookup.get(item["parent"])
                if parent_node:
                    parent_node["children"].append(item)

        # Sort children
        for node in tree:
            node["children"].sort(key=lambda x: x["order"])

        return tree


menu_registry = MenuRegistry()
