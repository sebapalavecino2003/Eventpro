from rest_framework.throttling import ScopedRateThrottle


class RegisterThrottle(ScopedRateThrottle):
    scope = 'register'


class LoginThrottle(ScopedRateThrottle):
    scope = 'login'


class ForgotPasswordThrottle(ScopedRateThrottle):
    scope = 'forgot_password'


class ResendVerificationThrottle(ScopedRateThrottle):
    scope = 'resend_verification'
