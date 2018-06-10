SECRET_KEY='123654789'
# Set the application in debug mode so that the server is reloaded on any code change & helps debug
DEBUG=True
# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED=True

# DB Config
SQLALCHEMY_DATABASE_URI='postgresql://dev_user:dev_pass@localhost/projetofinal_dev'
SQLALCHEMY_TRACK_MODIFICATIONS=False


# Security package configurations == Feature Flags
SECURITY_REGISTERABLE=True
SECURITY_RECOVERABLE=True
SECURITY_CHANGEABLE=True
# Tirar isto quando se colocar confirmacao conta por email
SECURITY_SEND_REGISTER_EMAIL=False


WTF_CSRF_ENABLED=False
JWT_TOKEN_LOCATION='cookies'
# app.config['JWT_COOKIE_SECURE'] = False
JWT_ACCESS_COOKIE_PATH='/'
JWT_REFRESH_COOKIE_PATH='/token/refresh'
JWT_COOKIE_CSRF_PROTECT=False
# app.config['JWT_SECRET_KEY'] = 'abva'

SECURITY_PASSWORD_HASH='bcrypt'
SECURITY_PASSWORD_SALT='$2a$16$PnnIgfMwkOjGX4SkHqSOPO'

MAIL_SERVER=''

# To solve: (insecure_transport) OAuth 2 MUST utilize https.
OAUTHLIB_INSECURE_TRANSPORT=1

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

DEBUG_TB_INTERCEPT_REDIRECTS=False
