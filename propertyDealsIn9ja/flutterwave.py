import os

from propertyDealsIn9ja.settings import DEBUG

if DEBUG:
    # test key
    FLUTTERWAVE_SECRET_KEY = 'FLWSECK_TEST-d917ff9b7854fe25486b22ff69ed614d-X'
    FLUTTERWAVE_PUBLIC_KEY = 'FLWPUBK_TEST-e12585f4c2da40025222b13315c5483c-X'
    FLUTTERWAVE_ENCRYPTION_KEY = 'FLWSECK_TEST9f81344e0682'
else:
    # live key
    FLUTTERWAVE_SECRET_KEY = os.environ.get("FLUTTERWAVE_SECRET_KEY")
    FLUTTERWAVE_PUBLIC_KEY = os.environ.get("FLUTTERWAVE_PUBLIC_KEY")
    FLUTTERWAVE_ENCRYPTION_KEY = os.environ.get("FLUTTERWAVE_ENCRYPTION_KEY")
