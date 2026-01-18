from menubar.menu import menu_registry

menu_registry.register(
    section="main", label="Status", order="10", url_name="status:group_list"
    
)
menu_registry.register(
    section="main",
    parent="Status",
    label="Add Group",
    #admin_required=True,
    order="10",
    url_name="status:sb-group-create"
)
