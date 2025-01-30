from django.core.management.base import BaseCommand
from django.apps import apps
from django.conf import settings
from faker import Faker
import random
from django.core.files.base import ContentFile
import requests
import os
import time

fake = Faker(['en_US', 'fa_IR'])  

def get_random_image(category='education'):
    """Return a placeholder image from Lorem Picsum with retries"""
    width, height = 800, 600
    max_retries = 3
    
    for _ in range(max_retries):
        image_id = random.randint(1, 1000) 
        image_url = f'https://picsum.photos/id/{image_id}/{width}/{height}'
        
        try:
            response = requests.get(image_url, timeout=10)
            if response.status_code == 200:
                return ContentFile(response.content, name=f'image_{fake.uuid4()}.jpg')
        except (requests.RequestException, TimeoutError):
            continue
    
    return None

def generate_instructor_data():
    return {
        'description': ' '.join(fake.sentences(nb=3)),
        'experience': random.randint(1, 20),
        'telegram_id': fake.user_name(),
        'youtube_id': fake.user_name(),
        'instagram_id': fake.user_name(),
        'img': get_random_image('people'),
        'is_master': random.choice([True, False]),
        'is_active': True,
    }

def generate_course_data():
    price = random.randint(100000, 1000000)
    max_discount = min(price * 0.5, 99.99)  
    
    return {
        'title': fake.sentence(nb_words=4),
        'slug': fake.slug(),
        'description': ' '.join(fake.sentences(nb=5)),
        'age_range': f'{random.randint(10,18)}-{random.randint(19,50)}',
        'duration': f'{random.randint(1,12)} ماه',
        'img': get_random_image('education'),
        'price': price,
        'discount_amount': round(random.uniform(0, max_discount), 2),
        'status': True,
        'certificate_status': random.choice([True, False]),
        'analysis_room_status': random.choice([True, False]),
        'extra_movments_status': random.choice([True, False]),
        'injury_prevention_status': random.choice([True, False]),
    }

def generate_blog_data():
    return {
        'title': fake.sentence(),
        'slug': fake.slug(),
        'description': ' '.join(fake.sentences(nb=5)),
        'img': get_random_image('technology'),
        'status': random.choice(['p', 'r']),
        'enable_comments': True,
    }

def generate_faq_data():
    return {
        'question': fake.sentence(nb_words=6) + '?',
        'answer': fake.text(max_nb_chars=500),
        'slug': fake.slug(),
        'status': True,
    }

list_of_models = {
    'accounts.CustomUser': {
        'count': 20,
        'fields': {
            'first_name': lambda x: fake.first_name(),
            'last_name': lambda x: fake.last_name(),
            'email': lambda x: fake.email(),
            'phone_number': lambda x: f'+98{fake.numerify(text="##########")}',
        }
    },
    'instructors.Instructor': {
        'count': 5,
        'fields': generate_instructor_data
    },
    'courses.Course': {
        'count': 15,
        'fields': generate_course_data
    },
    'blogs.Blog': {
        'count': 10,
        'fields': generate_blog_data
    },
    'faq.QuestionAnswer': {
        'count': 8,
        'fields': generate_faq_data
    }
}

class Command(BaseCommand):
    help = 'Seed database with sample data'

    def ensure_media_dirs(self):
        """Ensure media directories exist"""
        media_dirs = [
            settings.MEDIA_ROOT,
            os.path.join(settings.MEDIA_ROOT, 'instructors'),
            os.path.join(settings.MEDIA_ROOT, 'courses'),
            os.path.join(settings.MEDIA_ROOT, 'blogs'),
        ]
        
        for directory in media_dirs:
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
                self.stdout.write(f'Created directory: {directory}')

    def wait_for_db(self):
        """Wait for database to be available"""
        self.stdout.write('Waiting for database...')
        max_retries = 10
        retry_interval = 3 
        
        for attempt in range(max_retries):
            try:
               
                apps.get_model('accounts.CustomUser').objects.first()
                self.stdout.write(self.style.SUCCESS('Database available!'))
                return True
            except Exception as e:
                if attempt < max_retries - 1:
                    self.stdout.write(f'Database unavailable, retrying in {retry_interval} seconds...')
                    time.sleep(retry_interval)
                continue
        
        raise Exception('Could not connect to database')

    def handle(self, *args, **options):
        try:
            
            self.wait_for_db()
            
            self.ensure_media_dirs()
            
            # Clear existing data
            self.stdout.write("Deleting old data...")
            for model_name in reversed(list_of_models.keys()):
                try:
                    model = apps.get_model(model_name)
                    count = model.objects.count()
                    model.objects.all().delete()
                    self.stdout.write(f'Deleted {count} {model_name} objects')
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Error deleting {model_name}: {str(e)}'))

       
            try:
                User = apps.get_model('accounts.CustomUser')
                user_config = list_of_models['accounts.CustomUser']
                self.stdout.write(f'Creating {user_config["count"]} users...')
                created_users = []
                for _ in range(user_config["count"]):
                    user = User.objects.create_user(
                        password='password123',
                        **{k: v(None) if callable(v) else v for k, v in user_config['fields'].items()}
                    )
                    created_users.append(user)
                self.stdout.write(self.style.SUCCESS(f'Created {len(created_users)} users'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating users: {str(e)}'))
                return

           
            instructor_config = list_of_models['instructors.Instructor']
            Instructor = apps.get_model('instructors.Instructor')
            self.stdout.write(f'Creating {instructor_config["count"]} instructors...')
            users = User.objects.all()[:instructor_config['count']]
            created_instructors = []
            for user in users:
                instructor = Instructor.objects.create(
                    user=user,
                    **instructor_config['fields']()
                )
                created_instructors.append(instructor)
            self.stdout.write(self.style.SUCCESS(f'Created {len(created_instructors)} instructors'))

           
            Course = apps.get_model('courses.Course')
            course_config = list_of_models['courses.Course']
            self.stdout.write(f'Creating {course_config["count"]} courses...')
            for _ in range(course_config['count']):
                Course.objects.create(
                    instructor=random.choice(created_instructors),
                    **course_config['fields']()
                )
            self.stdout.write(self.style.SUCCESS(f'Created {course_config["count"]} courses'))

           
            Blog = apps.get_model('blogs.Blog')
            blog_config = list_of_models['blogs.Blog']
            self.stdout.write(f'Creating {blog_config["count"]} blogs...')
            for _ in range(blog_config['count']):
                Blog.objects.create(
                    author=random.choice(created_instructors),
                    **blog_config['fields']()
                )
            

            
            FAQ = apps.get_model('faq.QuestionAnswer')
            faq_config = list_of_models['faq.QuestionAnswer']
            self.stdout.write(f'Creating {faq_config["count"]} FAQs...')
            for _ in range(faq_config['count']):
                FAQ.objects.create(**faq_config['fields']())
            self.stdout.write(self.style.SUCCESS(f'Created {faq_config["count"]} FAQs'))

            self.stdout.write(self.style.SUCCESS('Successfully seeded database'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding database: {str(e)}'))
