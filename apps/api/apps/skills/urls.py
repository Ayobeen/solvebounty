from django.urls import path
from .views import SkillListView, MySkillsView, MySkillDeleteView

urlpatterns = [
    path('', SkillListView.as_view(), name='skill-list'),
    path('user/', MySkillsView.as_view(), name='user-skills'),
    path('user/<uuid:skill_id>/', MySkillDeleteView.as_view(), name='user-skill-delete'),
]
