from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


GROUP_PERMISSIONS = {
    'Mentors': [
        'add_skilloffer', 'change_skilloffer', 'delete_skilloffer', 'view_skilloffer',
        'view_booking', 'change_booking',
        'view_review',
    ],
    'Learners': [
        'view_skilloffer',
        'add_booking', 'view_booking',
        'add_review', 'change_review', 'delete_review', 'view_review',
    ],
}


class Command(BaseCommand):
    help = 'Create Mentors/Learners groups and assign project permissions.'

    def handle(self, *args, **options):
        for group_name, codenames in GROUP_PERMISSIONS.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created group: {group_name}'))
            else:
                self.stdout.write(f'Group already exists: {group_name}')

            permissions = Permission.objects.filter(codename__in=codenames)
            group.permissions.set(permissions)
            self.stdout.write(self.style.SUCCESS(
                f'Assigned {permissions.count()} permissions to {group_name}.'
            ))

        self.stdout.write(self.style.SUCCESS('Groups and permissions are ready.'))

