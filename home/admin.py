from django.contrib import admin
from .models import (
	UserUploadedImage, UserProfile, UserFashionPreference, EventPlan,
	GalleryImage, FashionItem, FashionItemReaction, FashionTag,
	ImagePredictionLog, ImageRecommendationLog,
	TextPredictionLog, TextRecommendationLog,
	TagRecommendationLog, ContentSimilarityLog,
	StyleBotSession, StyleBotMessage,
)


@admin.register(UserUploadedImage)
class UserUploadedImageAdmin(admin.ModelAdmin):
	list_display = ('id', 'caption', 'user', 'created_at')
	list_filter = ('created_at',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'city', 'gender', 'occupation', 'education', 'created_at')
	list_filter = ('gender', 'occupation', 'area')


@admin.register(UserFashionPreference)
class UserFashionPreferenceAdmin(admin.ModelAdmin):
	list_display = ('user', 'fav_color', 'fav_dressing_type', 'fav_design', 'created_at')


@admin.register(EventPlan)
class EventPlanAdmin(admin.ModelAdmin):
	list_display = ('title', 'user', 'event', 'due_date', 'priority', 'source', 'created_at')
	list_filter = ('event', 'priority', 'source')


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
	list_display = ('predicted_label', 'image_url', 'uploaded_by', 'created_at')
	list_filter = ('predicted_label',)


@admin.register(FashionItem)
class FashionItemAdmin(admin.ModelAdmin):
	list_display = ('external_id', 'display_name', 'article_type', 'base_colour', 'season')
	search_fields = ('display_name', 'article_type')


@admin.register(FashionItemReaction)
class FashionItemReactionAdmin(admin.ModelAdmin):
	list_display = ('user', 'title', 'category', 'reaction_count', 'created_at')
	list_filter = ('category',)


@admin.register(FashionTag)
class FashionTagAdmin(admin.ModelAdmin):
	list_display = ('fashion_tag', 'fashion_choice', 'created_at')
	list_filter = ('fashion_tag',)


@admin.register(ImagePredictionLog)
class ImagePredictionLogAdmin(admin.ModelAdmin):
	list_display = ('predicted_label', 'user', 'model_version', 'created_at')
	list_filter = ('predicted_label', 'model_version')


@admin.register(ImageRecommendationLog)
class ImageRecommendationLogAdmin(admin.ModelAdmin):
	list_display = ('user', 'input_image_id', 'created_at')


@admin.register(TextPredictionLog)
class TextPredictionLogAdmin(admin.ModelAdmin):
	list_display = ('user', 'prediction_type', 'predicted_label', 'created_at')
	list_filter = ('prediction_type',)


@admin.register(TextRecommendationLog)
class TextRecommendationLogAdmin(admin.ModelAdmin):
	list_display = ('user', 'recommendation_type', 'query_category', 'created_at')
	list_filter = ('recommendation_type',)


@admin.register(TagRecommendationLog)
class TagRecommendationLogAdmin(admin.ModelAdmin):
	list_display = ('user', 'tag_input', 'total_count', 'created_at')


@admin.register(ContentSimilarityLog)
class ContentSimilarityLogAdmin(admin.ModelAdmin):
	list_display = ('user', 'query_text', 'created_at')


@admin.register(StyleBotSession)
class StyleBotSessionAdmin(admin.ModelAdmin):
	list_display = ('user', 'model_used', 'message_count', 'plan_saved', 'started_at', 'last_active_at')
	list_filter = ('plan_saved', 'model_used')


@admin.register(StyleBotMessage)
class StyleBotMessageAdmin(admin.ModelAdmin):
	list_display = ('session', 'role', 'created_at')
	list_filter = ('role',)
