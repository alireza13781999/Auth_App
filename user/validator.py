from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


phone_number_validator = RegexValidator(
    regex=r"^(?:0|98|\+98|\+980|0098|098|00980)?(9\d{9})$",
    message="Phone number must be entered in this format: 09123456789 or 989123456789 or 00989123456789 or +989123456789 or +9809123456789 or 009809123456789. Maximum 15 digits allowed.",
    code="invalid_phone_number",
)
