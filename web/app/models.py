from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


class Cocks(models.Model):
    id = models.AutoField(primary_key=True)
    bloodline = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    location = models.CharField(max_length=120)
    
    image1 = models.ImageField(upload_to='images/')
    image2 = models.ImageField(upload_to='images/')
    image3 = models.ImageField(upload_to='images/')
    broodcock = models.ImageField(upload_to='images/')
    broodhen = models.ImageField(upload_to='images/')
    
    comment = models.CharField(max_length=500)
    date_posted = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    liked = models.IntegerField(default=0)
    is_sold = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.bloodline} - {self.owner}"

    # --------------------------------------
    # COMPRESS IMAGE FUNCTION
    # --------------------------------------
    def compress_image(self, image_field):
        if not image_field:
            return image_field

        image = Image.open(image_field)
        output = BytesIO()

        # ---------- BEST OPTION: WebP ----------
        image.save(output, format="WEBP", quality=85)
        new_ext = "webp"
        mime = "image/webp"

        # ---------- If you prefer JPEG instead: ----------
        # image.save(output, format="JPEG", quality=90, optimize=True)
        # new_ext = "jpg"
        # mime = "image/jpeg"

        output.seek(0)

        return InMemoryUploadedFile(
            output,
            'ImageField',
            f"{image_field.name.rsplit('.',1)[0]}.{new_ext}",
            mime,
            output.getbuffer().nbytes,
            None
        )

    # --------------------------------------
    # SAVE OVERRIDE - compress all images
    # --------------------------------------
    def save(self, *args, **kwargs):
        if self.image1:
            self.image1 = self.compress_image(self.image1)
        if self.image2:
            self.image2 = self.compress_image(self.image2)
        if self.image3:
            self.image3 = self.compress_image(self.image3)
        if self.broodcock:
            self.broodcock = self.compress_image(self.broodcock)
        if self.broodhen:
            self.broodhen = self.compress_image(self.broodhen)

        super().save(*args, **kwargs)
