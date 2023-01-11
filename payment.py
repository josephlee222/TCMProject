import stripe
charge = stripe.Charge.retrieve(
  "ch_3MOupr2eZvKYlo2C1SmdNGHe",
  api_key="sk_test_4eC39HqLyjWDarjtT1zdp7dc"
)
charge.capture() # Uses the same API Key.

charge = stripe.Charge.retrieve(
  "ch_3MOupr2eZvKYlo2C1SmdNGHe",
  stripe_account="acct_1032D82eZvKYlo2C"
)
charge.capture() # Uses the same account

try:
  # Use Stripe's library to make requests...
  pass
except stripe.error.CardError as e:
  # Since it's a decline, stripe.error.CardError will be caught

  print('Status is: %s' % e.http_status)
  print('Code is: %s' % e.code)
  # param is '' in this case
  print('Param is: %s' % e.param)
  print('Message is: %s' % e.user_message)
except stripe.error.RateLimitError as e:
  # Too many requests made to the API too quickly
  pass
except stripe.error.InvalidRequestError as e:
  # Invalid parameters were supplied to Stripe's API
  pass
except stripe.error.AuthenticationError as e:
  # Authentication with Stripe's API failed
  # (maybe you changed API keys recently)
  pass
except stripe.error.APIConnectionError as e:
  # Network communication with Stripe failed
  pass
except stripe.error.StripeError as e:
  # Display a very generic error to the user, and maybe send
  # yourself an email
  pass
except Exception as e:
  # Something else happened, completely unrelated to Stripe
  pass