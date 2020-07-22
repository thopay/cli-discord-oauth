import os, time, webbrowser, threading, logging, sys
from flask import Flask, g, session, redirect, request, url_for, jsonify, render_template
from requests_oauthlib import OAuth2Session

cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None
user = {
    'logged_in' : False,
    'authorized' : False,
    'details' : None
}

def thread_oauth():
    log = logging.getLogger('werkzeug')
    log.disabled = True
    webbrowser.open('http://127.0.0.1:5000/', new=1) #This is where it opens the browser window

    SERVER_ID = '504471685898960969' #Server ID
    OAUTH2_CLIENT_ID = '735187543242309693' #Client ID
    OAUTH2_CLIENT_SECRET = 'lS3hffV-fyGawrDNkvjI-VomNG8XI8yw' #Client Secret
    OAUTH2_REDIRECT_URI = 'http://localhost:5000/callback' 

    API_BASE_URL = os.environ.get('API_BASE_URL', 'https://discordapp.com/api')
    AUTHORIZATION_BASE_URL = API_BASE_URL + '/oauth2/authorize'
    TOKEN_URL = API_BASE_URL + '/oauth2/token'

    app = Flask(__name__)
    app.config['SECRET_KEY'] = OAUTH2_CLIENT_SECRET

    if 'http://' in OAUTH2_REDIRECT_URI:
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'


    def token_updater(token):
        session['oauth2_token'] = token


    def make_session(token=None, state=None, scope=None):
        return OAuth2Session(
            client_id=OAUTH2_CLIENT_ID,
            token=token,
            state=state,
            scope=scope,
            redirect_uri=OAUTH2_REDIRECT_URI,
            auto_refresh_kwargs={
                'client_id': OAUTH2_CLIENT_ID,
                'client_secret': OAUTH2_CLIENT_SECRET,
            },
            auto_refresh_url=TOKEN_URL,
            token_updater=token_updater)


    @app.route('/')
    def index():
        scope = request.args.get(
            'scope',
            'identify guilds')
        discord = make_session(scope=scope.split(' '))
        authorization_url, state = discord.authorization_url(AUTHORIZATION_BASE_URL)
        session['oauth2_state'] = state
        return redirect(authorization_url)


    @app.route('/callback')
    def callback():
        if request.values.get('error'):
            return request.values['error']
        discord = make_session(state=session.get('oauth2_state'))
        token = discord.fetch_token(
            TOKEN_URL,
            client_secret=OAUTH2_CLIENT_SECRET,
            authorization_response=request.url)
        session['oauth2_token'] = token
        return redirect(url_for('.me'))


    @app.route('/me')
    def me():
        global user
        discord = make_session(token=session.get('oauth2_token'))
        guilds = discord.get(API_BASE_URL + '/users/@me/guilds').json() #Fetches Servers
        discord_user = discord.get(API_BASE_URL + '/users/@me').json() #Fetches users
        user['logged_in'] = True
        for guild in guilds: #Searches through servers
            if(str(guild['id']) == SERVER_ID): #If user is in server, do whatever here
                user['authorized'] = True
                user['details'] = discord_user
                return "You've been authorized, you may now close this window."
        #If user is not in server, it just returns simple print statement
        return "You have not been authorized, you may now close this window."

    app.run(debug=True, use_reloader=False)

def login():
    t_oauth = threading.Thread(name='Login', target=thread_oauth)
    t_oauth.setDaemon(True)
    t_oauth.start()

    try:
        time_passed = 0
        while True:
            global user
            if (time_passed < 30):
                if (user['logged_in'] == False):
                    time.sleep(1)
                    time_passed += 1
                elif (user['authorized'] == False):
                    return user
                else:
                    return user
            else:
                return user
    except KeyboardInterrupt:
        exit(0)
