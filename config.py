from app import app 
import os 

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/projetofinal'
app.config['SECRET_KEY'] = '123654789'
# Set the application in debug mode so that the server is reloaded on any code change & helps debug
app.config['DEBUG'] = True
# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Security package configurations == Feature Flags
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_RECOVERABLE'] = True
app.config['SECURITY_CHANGEABLE'] = True
# Tirar isto quando se colocar confirmação conta por email
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False


app.config['WTF_CSRF_ENABLED'] = False
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
# app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
# app.config['JWT_SECRET_KEY'] = 'abva'

app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
app.config['SECURITY_PASSWORD_SALT'] = '$2a$16$PnnIgfMwkOjGX4SkHqSOPO'

app.config['MAIL_SERVER'] = ''

# To solve: (insecure_transport) OAuth 2 MUST utilize https.
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False
