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

    # Имена
    name_en = models.CharField("Name (English)", max_length=100)
    name_fr = models.CharField("Name (French)", max_length=100, blank=True, null=True)
    name_el = models.CharField("Name (Greek)", max_length=100, blank=True, null=True)
    name_es = models.CharField("Name (Spanish)", max_length=100, blank=True, null=True)

    # Аватарки
    avatar_en = models.ImageField("Avatar (English)", upload_to='avatars/')
    avatar_fr = models.ImageField("Avatar (French)", upload_to='avatars/', blank=True, null=True)
    avatar_el = models.ImageField("Avatar (Greek)", upload_to='avatars/', blank=True, null=True)
    avatar_es = models.ImageField("Avatar (Spanish)", upload_to='avatars/', blank=True, null=True)

    # Остальные данные
    rating = models.PositiveIntegerField(default=5)
    text_en = models.TextField("Text (English)")
    text_fr = models.TextField("Text (French)", blank=True, null=True)
    text_el = models.TextField("Text (Greek)", blank=True, null=True)
    text_es = models.TextField("Text (Spanish)", blank=True, null=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.name_en} - {self.offer.name}"

    def get_translated_text(self, lang_code):
        return getattr(self, f"text_{lang_code}", None) or self.text_en

    def get_translated_name(self, lang_code):
        return getattr(self, f"name_{lang_code}", None) or self.name_en

    def get_translated_avatar(self, lang_code):
        return getattr(self, f"avatar_{lang_code}", None) or self.avatar_en
