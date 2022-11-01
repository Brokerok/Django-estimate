from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserCreationForm, UploadFileForm
from .models import Pdf, Order, User
import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta


stripe.api_key = settings.STRIPE_SECRET_KEY


class Register(View):
     template_name = 'registration/register.html'

     def get(self, request):
          context = {
               'form': UserCreationForm()
          }
          return render(request, self.template_name, context)

     def post(self, request):
          form = UserCreationForm(request.POST)

          if form.is_valid():
               form.save()
               username = form.cleaned_data.get('username')
               password = form.cleaned_data.get('password1')
               user = authenticate(password=password, username=username)
               login(request, user)
               return redirect('home')
          context = {
               'form': form
          }
          return render(request, self.template_name, context)


class Estimate(View):
     template_name = 'estimate.html'

     def get(self, request):
          date_off = request.user.date_joined + timedelta(days=21)
          if date_off < timezone.now():
               user = User.objects.get(pk=request.user.id)
               user.tariff = False
               user.save()
          if request.user.tariff == True:
               order_number = len(Order.objects.filter(user=request.user)) + 1
               queryset = Pdf.objects.filter(order=order_number)
               context = {
                    'form': UploadFileForm(),
                    'queryset': queryset,
                    'order_number': order_number
               }
               return render(request, self.template_name, context)
          else:

               return render(request, 'estimateFalse.html')

     def post(self, request):
          order_number = len(Order.objects.filter(user=request.user)) + 1
          form = UploadFileForm(request.POST, request.FILES)
          if form.is_valid() and request.FILES:
               for f in request.FILES.getlist('file'):
                    pdf = Pdf.objects.create(user=request.user, pdf=f, order=order_number)
                    pdf.save()
          else:
               pass
          queryset = Pdf.objects.filter(order=order_number)
          context = {
               'form': form,
               'queryset': queryset,
               'order_number': order_number
          }
          return render(request, self.template_name, context)


class Account(View):
     template_name = 'account.html'

     def get(self, request):
          date_off = request.user.date_joined + timedelta(days=21)
          if date_off < timezone.now():
               user = User.objects.get(pk=request.user.id)
               user.tariff = False
               user.save()
               tariff  = "No access"
          else:
               tariff = "access"
          queryset = Order.objects.filter(user=request.user)
          context = {
               'queryset': queryset,
               'tariff': tariff
          }
          return render(request, self.template_name, context)


def delete_item(request, item_id):
     item = Pdf.objects.get(pk=item_id)
     item.delete()
     return redirect('estimate')


def create_order(request, item_order):
     Order.objects.get_or_create(user=request.user, number=item_order)
     context = {
          'order': item_order,
     }
     return render(request, 'order.html', context)


def payment(request):
     return render(request, 'payment.html')


class CreateCheckoutSessionView(View):
     def post(self, request):
          YOUR_DOMAIN = 'http://127.0.0.1:8000'
          checkout_session = stripe.checkout.Session.create(
               line_items=[
                    {
                         'price': 'price_1Lx9DnHaFA26pYW5dscGxm5R',
                         'quantity': 1,
                    },
               ],
               mode='payment',
               success_url=YOUR_DOMAIN + '/success/',
               cancel_url=YOUR_DOMAIN + '/cancel/',
               metadata={'user_id': request.user.id}
          )
          return redirect(checkout_session.url, code=303)


@csrf_exempt
def stripe_webhook(request):
     payload = request.body
     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
     event = None

     try:
          event = stripe.Webhook.construct_event(
               payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
          )
     except ValueError as e:
          return HttpResponse(status=400)
     except stripe.error.SignatureVerificationError as e:
          return HttpResponse(status=400)

     if event['type'] == 'checkout.session.completed':
          session = event['data']['object']
          user_id = int(session['metadata']["user_id"])
          user = User.objects.get(pk=user_id)
          user.tariff = True
          user.save()

     return HttpResponse(status=200)
