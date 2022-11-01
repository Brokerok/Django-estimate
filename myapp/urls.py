from django.urls import path, include
from .api import PdfViewSet
from rest_framework import routers
from . import views
from django.views.generic import TemplateView

router = routers.SimpleRouter()
router.register('api/pdf', PdfViewSet, 'pdf')

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.Register.as_view(), name='register'),
    path('estimate/', views.Estimate.as_view(), name='estimate'),
    path('account/', views.Account.as_view(), name='account'),
    path('delete_item/<item_id>', views.delete_item, name='delete_item'),
    path('create_order/<item_order>', views.create_order, name='create_order'),
    path('payment/', views.payment, name='payment'),
    path('payment/create-checkout-session/', views.CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('success/', TemplateView.as_view(template_name='success.html'), name="success"),
    path('cancel/', TemplateView.as_view(template_name='cancel.html'), name="cancel"),
    path('webhooks/stripe/', views.stripe_webhook, name="stripe-webhook"),
]

urlpatterns += router.urls
