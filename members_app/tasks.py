# Create your tasks here

from celery import shared_task
from termcolor import cprint
import stripe
from membership.models import (Subscription)
from datetime import datetime


@shared_task
def add(x, y):
    cprint("ADD SHARED TASKS", 'yellow')
    return x + y


@shared_task
def check_subscription_status_for_members():
    # schedule
    subscriptions_list = stripe.Subscription.list(limit=100)
    cprint(f"Total length of the list {len(subscriptions_list)}", 'blue')
    now = datetime.now()
    # now = datetime.fromtimestamp(1612058508)
    cprint(now, 'red')
    import time
    all_subscriptions_ids = []
    # cprint(time.ctime(), 'cyan')  # 'Mon Oct 18 13:35:29 2010'
    cprint(time.strftime('%H:%M:%-S %p %Z on %b %d, %Y'), 'cyan')  # 'Mon Oct 18 13:35:29 2010'
    # cprint(type(subscriptions_list), 'blue')
    # cprint(len(subscriptions_list), 'blue')
    # cprint(type(subscriptions_list['data'][0]), 'green')
    # cprint(subscriptions_list['data'][0], 'green')
    # cprint(subscriptions_list['data'][1]['id'], 'green')
    # loop through the subscriptions and save the id of every one
    for sub in subscriptions_list['data']:
        all_subscriptions_ids.append({
            'id': sub['id'],
            "current_period_start": sub['current_period_start'],
            'current_period_end': sub['current_period_end'],
            "customer": sub['customer']
        })

    # loop through the sub ids for every one and save the information to db
    for sub in all_subscriptions_ids:
        start = datetime.fromtimestamp(sub['current_period_start'])
        end = datetime.fromtimestamp(sub['current_period_end'])
        # end = datetime.fromtimestamp(1611194508)
        subscription_object = Subscription.objects.filter(stripe_subscription_id=sub['id'])
        if subscription_object.count() > 0:
            subscription_object = subscription_object.first()
            # cprint(subscription_object.stripe_subscription_id, 'cyan')
            # fetched_stripe = stripe.Subscription.retrieve(subscription_object.stripe_subscription_id)
            fetched_stripe = stripe.Subscription.retrieve('sub_IhJ0TdBz6kqpyu')
            cprint(fetched_stripe, 'magenta')
            # compare between the current date and the saved in the db
            # if now > end:
            #     subscription_object.subscription_status = False
            #     subscription_object.save()
            # cprint(subscription_object.subscription_status, 'magenta')

