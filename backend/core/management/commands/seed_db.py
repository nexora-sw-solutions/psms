from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import User, Organization
from clients.models import Client
from service_requests.models import ServiceRequest
from core.constants import RequestStatus, Priority, TaskStatus

class Command(BaseCommand):
    help = 'Seeds the database with initial test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        
        # 0. Clean (Optional - for dev)
        # ServiceRequest.objects.all().delete()
        # Client.objects.all().delete()
        # User.objects.all().delete()
        # Organization.objects.all().delete()

        # 1. Organization
        org, created = Organization.objects.get_or_create(
            name='TechFlow Solutions'
        )
        if created:
            self.stdout.write(f'Created Organization: {org.name}')

        # 2. Users
        # Password for all: 'password123'
        
        # Super Admin
        if not User.objects.filter(email='super@admin.com').exists():
            User.objects.create_superuser(
                email='super@admin.com',
                password='password123',
                first_name='Super',
                last_name='Admin',
                organization=org
            )
            self.stdout.write('Created Super Admin')

        # Firm Admin
        firm_admin, _ = User.objects.get_or_create(
            email='admin@techflow.com',
            defaults={
                'first_name': 'Alice',
                'last_name': 'Admin',
                'role': 'FIRM_ADMIN',
                'organization': org
            }
        )
        firm_admin.set_password('password123')
        firm_admin.save()

        # Manager
        manager, _ = User.objects.get_or_create(
            email='manager@techflow.com',
            defaults={
                'first_name': 'Bob',
                'last_name': 'Manager',
                'role': 'MANAGER',
                'organization': org
            }
        )
        manager.set_password('password123')
        manager.save()

        # Consultant
        consultant, _ = User.objects.get_or_create(
            email='lead@techflow.com',
            defaults={
                'first_name': 'Charlie',
                'last_name': 'Consultant',
                'role': 'CONSULTANT',
                'organization': org
            }
        )
        consultant.set_password('password123')
        consultant.save()

        # Client User
        client_user, _ = User.objects.get_or_create(
            email='client@acme.com',
            defaults={
                'first_name': 'David',
                'last_name': 'Client',
                'role': 'CLIENT',
                'organization': org
            }
        )
        client_user.set_password('password123')
        client_user.save()

        # 3. Client (Entity)
        client_entity, created = Client.objects.get_or_create(
            name='Acme Corp',
            organization=org
        )
        if created:
            self.stdout.write(f'Created Client: {client_entity.name}')

        # 4. Service Request
        if not ServiceRequest.objects.filter(title='Cloud Migration Strategy').exists():
            ServiceRequest.objects.create(
                organization=org,
                client=client_entity,
                manager=manager,
                lead_consultant=consultant,
                title='Cloud Migration Strategy',
                description='Migrate legacy on-prem servers to AWS.',
                status=RequestStatus.DRAFT,
                priority=Priority.HIGH,
                due_date=timezone.now() + timezone.timedelta(days=30)
            )
            self.stdout.write('Created Service Request: Cloud Migration Strategy')

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
