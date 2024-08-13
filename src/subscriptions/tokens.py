from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


# Questions:
# 1 - token must expire
# 2 - verify is user recovery password send tokens for inactive users
class TokenGenerator(PasswordResetTokenGenerator):
  def _make_hash_value(self, user, timestamp):
    return (
      six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
    )

account_activation_token = TokenGenerator()

