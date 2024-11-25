import csv
from core.models import Course

# python3 manage.py runscript core.webscraper.populate_courses

try:
    with open('./core/webscraper/courses.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            
            course_code = row['Course Code']
            course_name = row['Course Name']
            short_name = row['Short names']
            description = row['Description']

            
            Course.objects.update_or_create(
                course_code=course_code,
                course_name=course_name,
                short_name=short_name,
                description=description
            )
    print("Courses imported successfully!")
except Exception as e:
    print(f"An error occurred: {e}")