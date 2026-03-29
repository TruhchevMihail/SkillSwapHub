
from django.core.management.base import BaseCommand
from offers.models import SkillCategory, Tag


class Command(BaseCommand):
    help = 'Populate sample categories and tags'

    def handle(self, *args, **options):
        # Create categories
        categories = [
            ('Programming', 'Programming courses and tutoring'),
            ('Design', 'Design and UI/UX courses'),
            ('Music', 'Music lessons and tutoring'),
            ('Languages', 'Language learning courses'),
            ('Fitness', 'Fitness and wellness courses'),
        ]

        for cat_name, cat_desc in categories:
            cat, created = SkillCategory.objects.get_or_create(
                name=cat_name,
                defaults={'description': cat_desc}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created category: {cat_name}'))
            else:
                self.stdout.write(f'- Category {cat_name} already exists')

        # Create tags
        tags_list = [
            'Python', 'Django', 'JavaScript', 'React',
            'Photoshop', 'Figma', 'UI/UX',
            'Guitar', 'Piano', 'Singing',
            'Spanish', 'English', 'French',
            'Yoga', 'Running', 'Weight Training',
            'Beginner Friendly', 'Remote', 'Intermediate', 'Advanced'
        ]

        for tag_name in tags_list:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created tag: {tag_name}'))
            else:
                self.stdout.write(f'- Tag {tag_name} already exists')

        self.stdout.write(self.style.SUCCESS('\n✓ Sample data setup complete!'))
        self.stdout.write('\nNow you can:')
        self.stdout.write('1. Go to /admin/')
        self.stdout.write('2. Create a user or use superuser')
        self.stdout.write('3. Create some offers with categories and tags')
        self.stdout.write('4. Test the offers list, detail, create, edit, delete pages')

