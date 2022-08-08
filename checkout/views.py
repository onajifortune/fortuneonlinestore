import json
import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm

from account.models import Address
from basket.basket import Basket
from orders.models import Order, OrderItem

from .models import DeliveryOptions


@login_required
def deliverychoices(request):
    deliveryoptions = DeliveryOptions.objects.filter(is_active=True)
    return render(request, "checkout/delivery_choices.html", {"deliveryoptions": deliveryoptions})


@login_required
def basket_update_delivery(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        delivery_option = int(request.POST.get("deliveryoption"))
        delivery_type = DeliveryOptions.objects.get(id=delivery_option)
        updated_total_price = basket.basket_update_delivery(
            delivery_type.delivery_price)

        session = request.session
        if "purchase" not in request.session:
            session["purchase"] = {
                "delivery_id": delivery_type.id,
            }
        else:
            session["purchase"]["delivery_id"] = delivery_type.id
            session.modified = True

        response = JsonResponse(
            {"total": updated_total_price, "delivery_price": delivery_type.delivery_price})
        return response


@login_required
def delivery_address(request):

    session = request.session
    if "purchase" not in request.session:
        messages.success(request, "Please select delivery option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    addresses = Address.objects.filter(
        customer=request.user).order_by("-default")

    if "address" not in request.session:
        session["address"] = {"address_id": str(addresses[0].id)}
    else:
        session["address"]["address_id"] = str(addresses[0].id)
        session.modified = True

    return render(request, "checkout/delivery_address.html", {"addresses": addresses})


@login_required
def payment_selection(request):

    session = request.session
    if "address" not in request.session:
        messages.success(request, "Please select address option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    return render(request, "checkout/payment_selection.html", {})


####
# PayPal
####

def view_that_asks_for_money(request):
    host = request.get_host()
    print(host)
    road = request.build_absolute_uri
    print(road)
    # What you want the button to do.
    paypal_dict = {
        "business": "receiver_email@example.com",
        "amount": "1000.00",
        "item_name": "name of the item",
        "invoice": str(uuid.uuid4()),
        "notify_url": road(reverse('paypal-ipn')),
        "return": road(reverse('checkout:payment_successful')),
        "cancel_return": road(reverse("checkout:payment_cancel")),
        # Custom command to correlate to some function later (optional)
        "custom": "premium_plan",
    }
    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "payment.html", context)


# @login_required
def payment_complete(request):
    messages.success(request, 'You\'ve completed a payment')
    return redirect("checkout:your-return-view")


# @login_required
def payment_successful(request):
    messages.success(request, 'You\'ve successfully made a payment')
    return redirect("checkout:your-return-view")


# @login_required
def payment_cancel(request):
    messages.success(request, 'You\'re order has been canceled')
    return redirect("view_that_asks_for_money")
