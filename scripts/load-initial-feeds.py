#!/usr/bin/env python3
"""
Load Initial Feeds from CSV
Populates Firestore /sources collection from data/initial_feeds.csv
"""

import csv
import sys
from pathlib import Path
from firebase_admin import firestore, initialize_app

# Initialize Firebase Admin
initialize_app()
db = firestore.client()

def load_feeds_from_csv(csv_path: str):
    """Load feeds from CSV and write to Firestore /sources collection"""

    if not Path(csv_path).exists():
        print(f"❌ CSV file not found: {csv_path}")
        sys.exit(1)

    print(f"📂 Loading feeds from: {csv_path}\n")

    sources_added = 0
    sources_skipped = 0

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)

        for row in reader:
            source_id = row['source_id']
            source_ref = db.collection('sources').document(source_id)

            # Check if source already exists
            if source_ref.get().exists:
                print(f"⏭️  Skipped (exists): {row['name']}")
                sources_skipped += 1
                continue

            # Create source document
            source_doc = {
                'id': source_id,
                'name': row['name'],
                'type': row['type'],
                'url': row['url'],
                'category': row['category'],
                'topicTags': [],
                'status': 'active' if row['enabled'] == 'true' else 'disabled',
                'lastChecked': None,
                'lastSuccess': None,
                'lastError': None,
                'articlesLast24h': 0,
                'createdAt': firestore.SERVER_TIMESTAMP,
                'updatedAt': firestore.SERVER_TIMESTAMP
            }

            source_ref.set(source_doc)
            print(f"✅ Added: {row['name']} ({row['type']} - {row['url']})")
            sources_added += 1

    print(f"\n📊 Summary:")
    print(f"   Sources added: {sources_added}")
    print(f"   Sources skipped: {sources_skipped}")
    print(f"   Total in CSV: {sources_added + sources_skipped}")

if __name__ == '__main__':
    csv_file = 'data/initial_feeds.csv'

    if len(sys.argv) > 1:
        csv_file = sys.argv[1]

    load_feeds_from_csv(csv_file)
