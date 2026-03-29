from offers.models import SkillCategory, Tag, SkillOffer
from accounts.models import AppUser

# Create categories if they don't exist
categories = ['Programming', 'Design', 'Music', 'Languages', 'Fitness']
category_objects = []

for cat_name in categories:
    cat, created = SkillCategory.objects.get_or_create(
        name=cat_name,
        defaults={'description': f'{cat_name} courses and tutoring'}
    )
    category_objects.append(cat)
    if created:
        print(f'Created category: {cat_name}')
    else:
        print(f'Category {cat_name} already exists')

# Create tags if they don't exist
tags_list = ['Python', 'Django', 'Photoshop', 'Figma', 'Guitar', 'Beginner Friendly', 'Remote', 'Intermediate', 'Advanced']
tag_objects = {}

for tag_name in tags_list:
    tag, created = Tag.objects.get_or_create(name=tag_name)
    tag_objects[tag_name] = tag
    if created:
        print(f'Created tag: {tag_name}')
    else:
        print(f'Tag {tag_name} already exists')

print('\nSample data setup complete!')
print('\nNow you can:')
print('1. Go to /admin/')
print('2. Create a user or use superuser')
print('3. Create some offers with categories and tags')
print('4. Test the offers list, detail, create, edit, delete pages')
