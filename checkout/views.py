from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MakePaymentForm, OrderForm
from .models import OrderLineItem
from django.conf import settings
from django.utils import timezone
from issue_tracker.models import Issue
import stripe

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET


@login_required()
def checkout(request):

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        payment_form = MakePaymentForm(request.POST)

        if order_form.is_valid() and payment_form.is_valid():
            order = order_form.save(commit=False)
            order.date = timezone.now()
            order.buyer = request.user
            order.save()

            cart = request.session.get('cart', {})
            # initialize a value of 0
            total = 0
            for id, quantity in cart.items():
                product = get_object_or_404(Issue, pk=id)
                price = product.hourly_rate * product.hours_required
                total += quantity * price
                order_line_item = OrderLineItem(
                    product=product,
                    quantity=quantity,
                    order=order
                    )
                order_line_item.save()

            try:
                customer = stripe.Charge.create(
                    amount=int(total * 100),
                    currency="EUR",
                    description=request.user.email,
                    card=payment_form.cleaned_data['stripe_id'],
                )
                # stripe takes payments in cents, hence the order total
                # is multiplied by a factor of 100
            except stripe.error.CardError:
                messages.error(request, "Your card was declined!")
            # Collect statistics on features purchsed
            if customer.paid:

                for id, quantity in cart.items():
                    issue = get_object_or_404(Issue, pk=id)
                    purchased = issue.purchased
                    issue.purchased = purchased + 1
                    if issue.paid is False:
                        issue.paid = True
                    issue.save()

                messages.success(request, "your payment was successful")
                request.session['cart'] = {}
                # Empties the cart from the session after payment
                return redirect(reverse('get_issues'))
            else:
                messages.error(request, "Unable to take payment")
        else:
            print(payment_form.errors)
            messages.error(request,
                           "We were unable to take payment with that card!")
    else:
        payment_form = MakePaymentForm()
        order_form = OrderForm()

    return render(request, "checkout.html", {'order_form': order_form,
                                             'payment_form': payment_form,
                                             'publishable': settings.STRIPE_PUBLISHABLE})