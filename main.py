# -*- coding: utf-8 -*-

# A simple script to show the Oauth2.0 authentication process in Python. I've attempted to keep everything in as few files as possible.
# You will have to create the client secret and set up an application in Google. The README has more information on this.
# By Kevin Ellen

# main.py
# Entry to set up the server and set up the routing.

# Import the flask framework
import os
import flask

# Import the authorisation scrupts and tools
from src.utils.authorise import authorise_process, oauth2callback_process, clear_process, API_SERVICE_NAME, API_VERSION

# Import the Google libraries required for credentials and the Search Console API; normally I would put this somewhere else, but I leave it here to keep everything in a single file.
import google.oauth2.credentials
import googleapiclient.discovery

# Init the app
app = flask.Flask(__name__)
# Note: A secret key is included in the sample so that it works.
# If you use this code in your application, replace this with a truly secret
# key. See https://flask.palletsprojects.com/quickstart/#sessions.
app.secret_key = 'REPLACE ME - this value is here as a placeholder.'

# First two helper functions so they don't have to be repeated.

# Check if user is logged in. Returns TRUE or FALSE.
def check_login_status():
  return 'credentials' in flask.session

# Create the body content based on whether user is logged in or not.
def body(status):

  # if user is logged in:
  if status:

    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
      **flask.session['credentials']
    )

    # Retrieve list of properties in account
    search_console_service = googleapiclient.discovery.build(
      API_SERVICE_NAME, API_VERSION, credentials=credentials
    )
    site_list = search_console_service.sites().list().execute()

    # Filter for verified URL-prefix websites.
    verified_sites_urls = [
      s['siteUrl'] for s in site_list['siteEntry']
        if s['permissionLevel'] != 'siteUnverifiedUser'
          and s['siteUrl']
    ]

    # Create an unordered HTML list and iterate through the 'verified_sites_urls' list, adding each item to the unordered list.
    html_list = '<ul>'
    for site_url in verified_sites_urls:
      html_list += f'<li>{site_url}</li>'
    html_list += '</ul>'

    # Return the content.
    return f'''
      <p><a href="/clear">Sign out of current Google account.</a></p>
      <p>You are logged in and can see these profiles:</p>
      {html_list}
    '''

  # User is not logged in
  else:

    # Return the content.
    return '''
      <p>You are not logged in.</p>
      <p><a href="/authorise">Sign in with a Google account</a></p>
    '''

# Entry point for the homepage (path: /)
@app.route('/')
def index():
  status = 'You are logged in' if check_login_status() else 'You are not logged in'
  return f'''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Python Google Oauth2.0</title>
      </head>
      <body>
        <h1>{status}</h1>
        {body(check_login_status())}
      </body>
    </html>
  '''

# Route for the '/authorise' path - calls the authorise_process() - which can be found in the file 'src.utils.authorise'
@app.route('/authorise')
def authorise():
  return authorise_process()

# Route for the '/oauth2callback' path - calls the oauth2callback_process() - which can be found in the file 'src.utils.authorise'
@app.route('/oauth2callback')
def oauth2callback():
  return oauth2callback_process()

# Route for the '/clear' path - calls the clear_process() - which can be found in the file 'src.utils.authorise' - This empties the credentials in flask, thus unauthorising the user (logging them out)
@app.route('/clear')
def clear():
  return clear_process()


# Below is where the server etc set up. If the application is hosted on HTTPS, please disallow insecure transport of course.
if __name__ == '__main__':
  # When running locally, disable OAuthlib's HTTPs verification.
  # ACTION ITEM for developers:
  #     When running in production *do not* leave this option enabled.
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
  app.run('localhost', 8080, debug=True)