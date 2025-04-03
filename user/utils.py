from jwt import decode
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse






def unhash_token(request_header):
    token = request_header.get("Authorization", "")
    if token:
        try:
            token = token.split(" ")[1]
            decoded_token = decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return decoded_token
        except IndexError:
            raise AuthenticationFailed("Invalid token format")
        except Exception as e:
            raise AuthenticationFailed("Invalid or expired token")
    else:
        raise AuthenticationFailed("Authorization header missing")





def generate_verification_link(user):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    return reverse('verify-email', kwargs={'uidb64': uidb64, 'token': token})




