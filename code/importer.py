import os
import sys
sys.path.append(os.path.abspath(os.path.join(__file__, *[os.pardir] * 3)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'simplelms.settings'
import django
django.setup()

import csv
from django.contrib.auth.models import User
from core.models import Course, CourseMember

with open('./csv_data/user-data.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for num, row in enumerate(reader):
        if not User.objects.filter(username=row['username']).exists():
            User.objects.create_user(
                id=num+2,
                username=row['username'],
                password=row['password'],
                email=row['email']
            )

    
with open('./csv_data/course-data.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for num, row in enumerate(reader):           
        if not Course.objects.filter(pk=num+1).exists():
            try:
                teacher = User.objects.get(pk=int(row['teacher']))
            except User.DoesNotExist:
                print(f"Teacher with ID {row['teacher']} does not exist.")
                continue
            
            Course.objects.create(
                id=num+1,
                name=row['name'],
                description=row['description'],
                price=row['price'],
                teacher=teacher
            )

            
with open('./csv_data/member-data.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for num, row in enumerate(reader):
        try:
            course = Course.objects.get(pk=int(row['course_id']))
            user = User.objects.get(pk=int(row['user_id']))
        except Course.DoesNotExist:
            print(f"Course with ID {row['course_id']} does not exist.")
            continue
        except User.DoesNotExist:
            print(f"User with ID {row['user_id']} does not exist.")
            continue

        if not CourseMember.objects.filter(pk=num+1).exists():
            CourseMember.objects.create(
                course_id=course,
                user_id=user,
                id=num+1,
                roles=row['roles']
            )
