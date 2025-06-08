import phonenumbers


# Normalize phone numbers to E.164 format
def normalize_phone_number(raw_phone, default_region='US'):
    if not raw_phone or not isinstance(raw_phone, str):
        return None
    try:
        phone = phonenumbers.parse(raw_phone, default_region)
        if phonenumbers.is_valid_number(phone):
            return phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.E164)
    except phonenumbers.NumberParseException:
        return None
    return None



