from django.core.management.base import BaseCommand
from ticket.models import TicketType

class Command(BaseCommand):
    help = 'Seeds the database with initial ticket types and prices.'

    def handle(self, *args, **kwargs):
        
        ticket_data = [
            {'nationality': 'domestik', 'age_group': 'adult', 'price': 30000},
            {'nationality': 'domestik', 'age_group': 'child', 'price': 20000},
            {'nationality': 'asing', 'age_group': 'adult', 'price': 75000},
            {'nationality': 'asing', 'age_group': 'child', 'price': 40000},
        ]

        self.stdout.write('Mulai proses seeding data tipe tiket...')

        for data in ticket_data:
            # get_or_create: Cek dulu apakah sudah ada, jika belum, baru buat.
            # Ini mencegah duplikasi data jika perintah dijalankan berkali-kali.
            ticket_type, created = TicketType.objects.get_or_create(
                nationality=data['nationality'],
                age_group=data['age_group'],
                defaults={'price': data['price']}
            )

            if created:
                self.stdout.write(self.style.SUCCESS(
                    f'Berhasil membuat tipe tiket: {ticket_type}'
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f'Tipe tiket "{ticket_type}" sudah ada, proses dilewati.'
                ))
        
        self.stdout.write(self.style.SUCCESS('Proses seeding selesai.'))