from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone


# ─────────────────────────────────────────────
# Core user models (renamed + naming conflicts fixed)
# ─────────────────────────────────────────────

class UserUploadedImage(models.Model):
    """Stores user-uploaded images for classification. Previously: uimage."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='uploaded_images',
    )
    caption = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='img/%y')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Uploaded Image'
        verbose_name_plural = 'Uploaded Images'
        ordering = ['-created_at']

    def __str__(self):
        return self.caption or f'Image #{self.pk}'


class UserProfile(models.Model):
    """Demographic/location profile for a user. Previously: UserModal (fixes choices/field name conflicts)."""
    AREA_CHOICES = (('U', 'Urban'), ('R', 'Rural'))
    OCCUPATION_CHOICES = (
        ('S', 'Student'), ('T', 'Teacher'), ('B', 'Businessman'),
        ('D', 'Doctor'), ('E', 'Engineer'),
    )
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))
    EDUCATION_CHOICES = (
        ('M', 'Matriculation'), ('I', 'Intermediate'),
        ('B', 'Bachelor_Degree'), ('MS', 'Master_Degree'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_profiles')
    area = models.CharField(max_length=2, choices=AREA_CHOICES, default='')
    city = models.CharField(max_length=100, default='')
    occupation = models.CharField(max_length=2, choices=OCCUPATION_CHOICES, default='')
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, default='')
    age = models.PositiveIntegerField(null=True, blank=True)
    education = models.CharField(max_length=3, choices=EDUCATION_CHOICES, default='')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} — Profile'


class UserFashionPreference(models.Model):
    """Fashion style preferences for a user. Previously: FashionModel (fixes choices/field name conflicts)."""
    FAV_COLOR_CHOICES = (
        ('B', 'Black'), ('R', 'Red'), ('W', 'White'), ('G', 'Green'),
    )
    DRESSING_TYPE_CHOICES = (
        ('F', 'Formal'), ('C', 'Casual'), ('SF', 'Semi-Formal'),
    )
    DESIGN_CHOICES = (('CK', 'Check'), ('P', 'Plain'), ('L', 'Lines'))

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fashion_preferences')
    fashion_conscious = models.CharField(max_length=20, default='')
    brand_conscious = models.CharField(max_length=20, default='')
    fav_color = models.CharField(max_length=2, choices=FAV_COLOR_CHOICES, default='')
    fav_dressing_type = models.CharField(max_length=3, choices=DRESSING_TYPE_CHOICES, default='')
    fav_design = models.CharField(max_length=3, choices=DESIGN_CHOICES, default='')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = 'Fashion Preference'
        verbose_name_plural = 'Fashion Preferences'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} — Fashion Preference'


class EventPlan(models.Model):
    """User event plans. Previously: PlanModel (fixes choices/field name conflict, adds source + timestamps)."""
    EVENT_CHOICES = (
        ('S', 'Social'), ('R', 'Religious'), ('I', 'Islamic'),
        ('P', 'Party'), ('W', 'Wedding'), ('O', 'Office'),
    )
    PRIORITY_CHOICES = (('L', 'Low'), ('M', 'Medium'), ('H', 'High'))
    SOURCE_CHOICES = (('manual', 'Manual Form'), ('stylebot', 'StyleBot Chat'))

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='event_plans')
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    event = models.CharField(max_length=2, choices=EVENT_CHOICES, default='S')
    created = models.DateField(default=timezone.now)
    due_date = models.DateField(default=timezone.now)
    time = models.TimeField()
    priority = models.CharField(max_length=2, choices=PRIORITY_CHOICES, default='M')
    source = models.CharField(max_length=10, choices=SOURCE_CHOICES, default='manual')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = 'Event Plan'
        verbose_name_plural = 'Event Plans'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# ─────────────────────────────────────────────
# CSV-to-DB replacement tables
# ─────────────────────────────────────────────

class GalleryImage(models.Model):
    """Replaces gallery.csv — image classification results for gallery display."""
    predicted_label = models.CharField(max_length=100, db_index=True)
    image_url = models.CharField(max_length=500)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='gallery_images',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.predicted_label} — {self.image_url}'


class FashionItem(models.Model):
    """Replaces input_rec_images.csv / Text_Similarity.csv product catalog."""
    external_id = models.IntegerField(unique=True, db_index=True)
    gender = models.CharField(max_length=20, blank=True)
    master_category = models.CharField(max_length=50, blank=True)
    sub_category = models.CharField(max_length=50, blank=True)
    article_type = models.CharField(max_length=100, blank=True)
    base_colour = models.CharField(max_length=50, blank=True)
    season = models.CharField(max_length=20, blank=True)
    usage = models.CharField(max_length=50, blank=True)
    display_name = models.CharField(max_length=300, blank=True)
    image_filename = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = 'Fashion Item'
        verbose_name_plural = 'Fashion Items'

    def __str__(self):
        return self.display_name or f'Item #{self.external_id}'


class FashionItemReaction(models.Model):
    """Replaces Recommendation_Table.csv — user reactions/scores against fashion items."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='item_reactions', null=True, blank=True,
    )
    item_id = models.IntegerField(db_index=True)
    title = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=100, blank=True)
    reaction_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Fashion Item Reaction'
        verbose_name_plural = 'Fashion Item Reactions'
        ordering = ['-created_at']

    def __str__(self):
        return f'User {self.user_id} → {self.title}'


class FashionTag(models.Model):
    """Replaces Fashion_Tags_rec.csv and fashions_tags.csv — style tag associations."""
    fashion_choice = models.CharField(max_length=300, db_index=True)
    fashion_tag = models.CharField(max_length=100, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Fashion Tag'
        verbose_name_plural = 'Fashion Tags'

    def __str__(self):
        return f'{self.fashion_tag} — {self.fashion_choice}'


# ─────────────────────────────────────────────
# Activity & prediction log tables
# ─────────────────────────────────────────────

class ImagePredictionLog(models.Model):
    """Logs every image classification prediction."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='image_predictions',
    )
    image_path = models.CharField(max_length=500)
    predicted_label = models.CharField(max_length=100, db_index=True)
    model_version = models.CharField(max_length=50, default='CNN_v1')
    confidence_score = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Image Prediction Log'
        verbose_name_plural = 'Image Prediction Logs'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.predicted_label}'


class ImageRecommendationLog(models.Model):
    """Logs every image-based fashion recommendation request."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='image_recommendations',
    )
    input_image_id = models.IntegerField()
    recommended_item_ids = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Image Recommendation Log'
        verbose_name_plural = 'Image Recommendation Logs'
        ordering = ['-created_at']

    def __str__(self):
        return f'ImgRec input={self.input_image_id}'


class TextPredictionLog(models.Model):
    """Logs text-based fashion predictions (dress_category, event, dress)."""
    PREDICTION_TYPE_CHOICES = (
        ('dress_category', 'Dress Category'),
        ('event', 'Event'),
        ('dress', 'Dress'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='text_predictions',
    )
    prediction_type = models.CharField(max_length=20, choices=PREDICTION_TYPE_CHOICES, db_index=True)
    input_features = models.JSONField(default=list)
    predicted_label = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Text Prediction Log'
        verbose_name_plural = 'Text Prediction Logs'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.prediction_type}: {self.predicted_label}'


class TextRecommendationLog(models.Model):
    """Logs text-based fashion recommendation requests."""
    RECOMMENDATION_TYPE_CHOICES = (
        ('popularity', 'Popularity Based'),
        ('user_based', 'User Based'),
        ('category_based', 'Category Based'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='text_recommendations',
    )
    query_category = models.CharField(max_length=200, blank=True)
    recommendation_type = models.CharField(max_length=20, choices=RECOMMENDATION_TYPE_CHOICES, db_index=True)
    recommended_items = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Text Recommendation Log'
        verbose_name_plural = 'Text Recommendation Logs'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.recommendation_type}: {self.query_category}'


class TagRecommendationLog(models.Model):
    """Logs tag-based fashion recommendation lookups."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='tag_recommendations',
    )
    tag_input = models.CharField(max_length=100, db_index=True)
    matched_fashion_choices = models.JSONField(default=list)
    total_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Tag Recommendation Log'
        verbose_name_plural = 'Tag Recommendation Logs'
        ordering = ['-created_at']

    def __str__(self):
        return f'Tag: {self.tag_input}'


class ContentSimilarityLog(models.Model):
    """Logs content-based similarity / content classification lookups."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='similarity_lookups',
    )
    query_text = models.CharField(max_length=500)
    similar_items = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Content Similarity Log'
        verbose_name_plural = 'Content Similarity Logs'
        ordering = ['-created_at']

    def __str__(self):
        return f'Similarity: {self.query_text[:60]}'


# ─────────────────────────────────────────────
# StyleBot chat session tables
# ─────────────────────────────────────────────

class StyleBotSession(models.Model):
    """Tracks each StyleBot conversational session."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stylebot_sessions')
    session_key = models.CharField(max_length=100, blank=True, db_index=True)
    model_used = models.CharField(max_length=100, default='openai/gpt-4o-mini')
    message_count = models.PositiveIntegerField(default=0)
    plan_saved = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    last_active_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'StyleBot Session'
        verbose_name_plural = 'StyleBot Sessions'
        ordering = ['-started_at']

    def __str__(self):
        return f'{self.user} — StyleBot Session'


class StyleBotMessage(models.Model):
    """Stores individual messages within a StyleBot session."""
    ROLE_CHOICES = (('user', 'User'), ('assistant', 'Assistant'))

    session = models.ForeignKey(StyleBotSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, db_index=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'StyleBot Message'
        verbose_name_plural = 'StyleBot Messages'
        ordering = ['created_at']

    def __str__(self):
        return f'[{self.role}] {self.content[:80]}'


# ─── backward-compat aliases (used by existing views / chatbot engine) ───
UserModal = UserProfile
FashionModel = UserFashionPreference
PlanModel = EventPlan

