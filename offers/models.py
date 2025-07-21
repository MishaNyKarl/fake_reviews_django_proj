from django.db import models


class Offer(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='offers/')
    rating = models.FloatField(default=4.9)
    votes_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Review(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/')
    rating = models.PositiveIntegerField(default=5)
    text_en = models.TextField("Text (English)")
    text_fr = models.TextField("Text (French)", blank=True, null=True)
    text_el = models.TextField("Text (Greek)", blank=True, null=True)
    text_es = models.TextField("Text (Spanish)", blank=True, null=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.offer.name}"

    def get_translated_text(self, lang_code):
        return getattr(self, f"text_{lang_code}", None) or self.text_en
