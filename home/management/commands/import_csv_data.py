"""
Management command: import_csv_data
Imports legacy CSV data into the new database tables.

Usage:
    python manage.py import_csv_data              # import all
    python manage.py import_csv_data --only gallery
    python manage.py import_csv_data --only items
    python manage.py import_csv_data --only reactions
    python manage.py import_csv_data --only tags
"""

import csv
import os

from django.core.management.base import BaseCommand

from home.models import GalleryImage, FashionItem, FashionItemReaction, FashionTag

BASE = 'Saved_Models'


class Command(BaseCommand):
    help = 'Import legacy CSV data into database tables'

    def add_arguments(self, parser):
        parser.add_argument(
            '--only',
            choices=['gallery', 'items', 'reactions', 'tags'],
            default=None,
            help='Import only a specific dataset',
        )

    def handle(self, *args, **options):
        only = options['only']

        if only is None or only == 'gallery':
            self._import_gallery()
        if only is None or only == 'items':
            self._import_fashion_items()
        if only is None or only == 'reactions':
            self._import_reactions()
        if only is None or only == 'tags':
            self._import_tags()

    def _import_gallery(self):
        path = os.path.join(BASE, 'gallery.csv')
        if not os.path.exists(path):
            self.stdout.write(self.style.WARNING(f'  gallery.csv not found at {path}, skipping.'))
            return
        created = 0
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                url = row.get('URL', '').strip()
                label = row.get('RESULT', '').strip()
                if url and label:
                    GalleryImage.objects.get_or_create(image_url=url, defaults={'predicted_label': label})
                    created += 1
        self.stdout.write(self.style.SUCCESS(f'  gallery: {created} rows processed from gallery.csv'))

    def _import_fashion_items(self):
        path = os.path.join(BASE, 'Text_Similarity.csv')
        if not os.path.exists(path):
            self.stdout.write(self.style.WARNING(f'  Text_Similarity.csv not found, skipping items.'))
            return
        created = skipped = 0
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            batch = []
            for row in reader:
                try:
                    eid = int(row.get('id') or row.get('idl') or 0)
                except ValueError:
                    skipped += 1
                    continue
                if not eid:
                    skipped += 1
                    continue
                if not FashionItem.objects.filter(external_id=eid).exists():
                    batch.append(FashionItem(
                        external_id=eid,
                        gender=str(row.get('gender', ''))[:20],
                        master_category=str(row.get('masterCategory', ''))[:50],
                        sub_category=str(row.get('subCategory', ''))[:50],
                        article_type=str(row.get('articleType', ''))[:100],
                        base_colour=str(row.get('baseColour', ''))[:50],
                        season=str(row.get('season', ''))[:20],
                        usage=str(row.get('usage', ''))[:50],
                        display_name=str(row.get('productDisplayName', ''))[:300],
                        image_filename=f"{eid}.jpg",
                    ))
                    created += 1
                if len(batch) >= 500:
                    FashionItem.objects.bulk_create(batch, ignore_conflicts=True)
                    batch = []
            if batch:
                FashionItem.objects.bulk_create(batch, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(
            f'  fashion_items: {created} created, {skipped} skipped from Text_Similarity.csv'
        ))

    def _import_reactions(self):
        path = os.path.join(BASE, 'Recommendation_Table.csv')
        if not os.path.exists(path):
            self.stdout.write(self.style.WARNING('  Recommendation_Table.csv not found, skipping reactions.'))
            return
        created = 0
        # Import first 2000 rows as seed data (file has 25K rows)
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            batch = []
            for i, row in enumerate(reader):
                if i >= 2000:
                    break
                try:
                    item_id = int(row.get('item_id', 0))
                    reaction_count = int(row.get('Reaction_Count', 0))
                except (ValueError, TypeError):
                    continue
                batch.append(FashionItemReaction(
                    item_id=item_id,
                    title=str(row.get('Title', ''))[:200],
                    category=str(row.get('Category', ''))[:100],
                    reaction_count=reaction_count,
                ))
                created += 1
            FashionItemReaction.objects.bulk_create(batch, ignore_conflicts=False)
        self.stdout.write(self.style.SUCCESS(
            f'  reactions: {created} rows imported from Recommendation_Table.csv (first 2000)'
        ))

    def _import_tags(self):
        path = os.path.join(BASE, 'Fashion_Tags_rec.csv')
        if not os.path.exists(path):
            self.stdout.write(self.style.WARNING('  Fashion_Tags_rec.csv not found, skipping tags.'))
            return
        created = 0
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            batch = []
            for i, row in enumerate(reader):
                if i >= 3000:
                    break
                choice = str(row.get('Fashion_Choice', '')).strip()
                tag = str(row.get('Fashion_Tag', '')).strip()
                if choice and tag:
                    batch.append(FashionTag(fashion_choice=choice[:300], fashion_tag=tag[:100]))
                    created += 1
            FashionTag.objects.bulk_create(batch, ignore_conflicts=False)
        self.stdout.write(self.style.SUCCESS(
            f'  tags: {created} rows imported from Fashion_Tags_rec.csv (first 3000)'
        ))
