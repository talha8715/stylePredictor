from django.db.models import Count
from django.contrib.auth.models import User

from .models import (
	UserFashionPreference,
	EventPlan,
	ImagePredictionLog,
	StyleBotSession,
)


class DataVisulaizer:
	def __init__(self, s):
		pass

	def get_user_growth(self):
		"""Returns (month_labels, user_counts) grouped by account creation month."""
		from django.db.models.functions import TruncMonth
		qs = (
			User.objects
			.annotate(month=TruncMonth('date_joined'))
			.values('month')
			.annotate(count=Count('id'))
			.order_by('month')
		)
		labels = [r['month'].strftime('%b %Y') if r['month'] else '' for r in qs]
		counts = [r['count'] for r in qs]
		return labels, counts

	def get_prediction_label_counts(self):
		"""Returns (labels, counts) for image prediction logs."""
		qs = (
			ImagePredictionLog.objects
			.values('predicted_label')
			.annotate(count=Count('id'))
			.order_by('-count')[:10]
		)
		labels = [r['predicted_label'] for r in qs]
		counts = [r['count'] for r in qs]
		return labels, counts

	def get_event_plan_distribution(self):
		"""Returns (event_types, counts) from EventPlan."""
		event_label = dict(EventPlan.EVENT_CHOICES)
		qs = (
			EventPlan.objects
			.values('event')
			.annotate(count=Count('id'))
			.order_by('-count')
		)
		labels = [event_label.get(r['event'], r['event']) for r in qs]
		counts = [r['count'] for r in qs]
		return labels, counts

	def get_plan_source_split(self):
		"""Returns (source_labels, counts) for manual vs stylebot plans."""
		source_label = dict(EventPlan.SOURCE_CHOICES)
		qs = EventPlan.objects.values('source').annotate(count=Count('id'))
		labels = [source_label.get(r['source'], r['source']) for r in qs]
		counts = [r['count'] for r in qs]
		return labels, counts

	def get_fashion_preferences(self):
		"""Returns (color_labels, color_counts) for fav_color distribution."""
		color_label = dict(UserFashionPreference.FAV_COLOR_CHOICES)
		qs = (
			UserFashionPreference.objects
			.values('fav_color')
			.annotate(count=Count('id'))
			.order_by('-count')
		)
		labels = [color_label.get(r['fav_color'], r['fav_color']) for r in qs]
		counts = [r['count'] for r in qs]
		return labels, counts

	def get_stylebot_activity(self):
		"""Returns (date_labels, session_counts) grouped by day."""
		from django.db.models.functions import TruncDate
		qs = (
			StyleBotSession.objects
			.annotate(day=TruncDate('started_at'))
			.values('day')
			.annotate(count=Count('id'))
			.order_by('day')
		)
		labels = [str(r['day']) for r in qs]
		counts = [r['count'] for r in qs]
		return labels, counts