from admin_tools.dashboard import modules, Dashboard

class CustomIndexDashboard(Dashboard):
    def init_with_context(self, context):
        self.children.append(modules.ModelList(
            title='Users and Inventory',
            models=('accounts.models.CustomUser', 'inventory.models.InventoryItem',),
        ))
        self.children.append(modules.LinkList(
            title='Important links',
            children=[
                {
                    'title': 'Django documentation',
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': 'Django "django-users" mailing list',
                    'url': 'http://groups.google.com/group/django-users',
                    'external': True,
                },
            ]
        ))
