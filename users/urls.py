from django.urls import path
from .views import HomeView, LoginView, RegisterView, HealthPredictionView, DashboardView, EditRecordView, DeleteRecordView, LogoutView

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path( 'prediction/',HealthPredictionView.as_view(), name='health-prediction'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('record/edit/<int:record_id>/', EditRecordView.as_view(), name='edit_record'),
    path('record/delete/<int:record_id>/', DeleteRecordView.as_view(), name='delete_record'),
]