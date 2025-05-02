from django.core.management.base import BaseCommand
from cloudinary.uploader import upload
from flipcart.models import Category, Products, Banner
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Uploads existing local images to Cloudinary and updates model fields.'

    def handle(self, *args, **kwargs):
        models_to_update = [Category, Products, Banner]
        for model in models_to_update:
            for obj in model.objects.all():
                # Skip if already uploaded to Cloudinary
                if "res.cloudinary.com" in str(obj.image):
                    continue

                local_path = obj.image.path if hasattr(obj.image, 'path') else None
                if local_path and os.path.exists(local_path):
                    print(f"Uploading {local_path} to Cloudinary...")
                    result = upload(local_path)
                    obj.image = result["public_id"]  # store as CloudinaryField
                    obj.save()
                    print(f"Uploaded and updated: {obj}")
                else:
                    print(f"Skipped: {obj} (no local image)")
