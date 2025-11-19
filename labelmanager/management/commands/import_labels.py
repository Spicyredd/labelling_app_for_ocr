from django.core.management.base import BaseCommand
from labelmanager.models import ValidLabelPair
import tqdm

class Command(BaseCommand):
    help = "Import labels from a txt file into ValidLabelPair table"

    def add_arguments(self, parser):
        parser.add_argument("filepath", type=str, help="Path to the txt file")

    def handle(self, *args, **options):
        filepath = options["filepath"]

        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in tqdm.tqdm(lines):
                line = line.strip()

                if not line:
                    continue

                # Split on first space only (image path may not have spaces, label may)
                parts = line.split(" ", 1)

                if len(parts) != 2:
                    self.stdout.write(self.style.WARNING(f"Skipping malformed line: {line}"))
                    continue

                image_path, label = parts
                image_path = image_path
                ValidLabelPair.objects.create(
                    image_path=image_path,
                    label=label,
                    label_status="not_checked"
                )

                # self.stdout.write(self.style.SUCCESS(f"Imported: {image_path} — {label}"))

        self.stdout.write(self.style.SUCCESS("Done!"))
