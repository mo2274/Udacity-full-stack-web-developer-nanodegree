#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import datetime

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
  '''
    This class store the information of the venue like name, city, 
    state, genres, address, phone, image link and facebook link   
  '''

  __tablename__ = 'venues'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  city = db.Column(db.String(120), nullable=False)
  state = db.Column(db.String(120), nullable=False)
  genres = db.Column(db.String(120), nullable=True)
  address = db.Column(db.String(120), nullable=False)
  phone = db.Column(db.String(120), nullable=False)
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  shows = db.relationship('Show', backref=('venues'))
    

class Artist(db.Model):
  '''
    This class store the information of an artist like name, city, 
    state, genres, address, phone, image link and facebook link   
  '''    
      
  __tablename__ = 'artists'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  city = db.Column(db.String(120), nullable=False)
  state = db.Column(db.String(120), nullable=False)
  phone = db.Column(db.String(120), nullable=False)
  genres = db.Column(db.String(120), nullable=False)
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  shows = db.relationship('Show', backref=('artists'))


class Show(db.Model):
  '''
    This class store the information of a show like the id of the venue,
    id of the artist and the start time of the show
  '''     
  __tablename__ = 'shows'

  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey(
        'venues.id'), nullable=False )
  artist_id = db.Column(db.Integer, db.ForeignKey(
        'artists.id'), nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)



#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  '''
    This function is used to format the date and the time in a specific format.

    Arg: 
        value: the value of the date and the time
        format: the needed format of the date and the time (medium by default)
    Return: 
            the fromated date the time    
  '''        
  date = dateutil.parser.parse(str(value))
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  '''
    This function is used to get all venues data from the database and group them by 
    city and state and send then to the view.

    Return: 
            The venues data to be viewed in venue.html page    
  '''  
  venues = Venue.query.all() 
  data = []
  status = 1
  for venue in venues:
    status = 1
    for item in data:
      if item['city'] == venue.city and item['state'] == venue.state:
        status = 0    
        item['venues'].append({
          'id' : venue.id,
          'name': venue.name
        })
    if status == 1:
      data.append({
        'city' : venue.city,
        'state' : venue.state,
        'venues' :[ {
          'id': venue.id,
          'name': venue.name
        }]
      })  
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  '''
    This function is used to search for a specific venue by the name of the venue
    and the search is case insensitive.
    It takes the name of the venue from the form and return all the venues the match this name.

    Return: 
            send the data of all the matched venue to the view.   
  '''      
  venue_name = request.form['search_term']
  search = "%{}%".format(venue_name)
  venues = Venue.query.filter(Venue.name.ilike(search)).all()
  data = []
  upcoming_shows_num = 0

  for venue in venues:
    shows = Show.query.filter_by(venue_id=venue.id).all()
    for show in shows:
      if show.start_time >= datetime.today():
        upcoming_shows_num += 1

    data.append({
      'id': venue.id,
      'name' : venue.name,
      'num_upcoming_shows' : upcoming_shows_num
    })    
    
  response={
    "count": len(venues),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  '''
    This function is used to show the data of a specific venue.

    Arg: 
        venue_id : the id of the venue you want to show
    Return: 
            the data of the venue to the show_venue.html page    
  '''      
  venue = Venue.query.get(venue_id) 
  shows = Show.query.filter_by(venue_id=venue_id).all()
  past_shows = []
  upcoming_shows = []

  for show in shows:
    if show.start_time < datetime.today():
      past_shows.append({
        "venue_id": show.artist_id,
        "venue_name": show.artists.name,
        "venue_image_link": show.artists.image_link,
        "start_time": show.start_time
      })
    else:
      upcoming_shows.append({
        "venue_id": show.artist_id,
        "venue_name": show.artists.name,
        "venue_image_link": show.artists.image_link,
        "start_time": show.start_time
      })
  data = {
    "id": venue.id,
    "name": venue.name,
    "genres": str(venue.genres).split(','),
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": "https://www.themusicalhop.com",
    "facebook_link": venue.facebook_link,
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  '''
    This function is used to create a venue form.   
  '''      
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  '''
    This function is used to create a new venue in the database.
    it takes all the information of the venue from the form and create a new venue and 
    store it in the database.

    Return: 
            return to the home page   
  '''      
  error = False
  try:
    recored = Venue()
    recored.name = request.form['name']
    recored.city = request.form['city']
    recored.state = request.form['state']
    recored.address = request.form['address']
    recored.phone = request.form['phone']
    recored.facebook_link = request.form['facebook_link']
    recored.genres = ','.join(request.form.getlist('genres'))
    db.session.add(recored)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close() 
  if not error:
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  else:
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  '''
    This function is used to delete a venue from the database.

    Arg: 
        venue_id : the id of the venue to be deleted    
  '''      
  try:
    recored = Venue.query.get(venue_id)
    db.session.delete(recored)
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close() 
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  '''
    This function is used to show the data of the all artists in the artists.html page.   
  '''      
  data = Artist.query.all()  
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  '''
    This function is used to search for a specific artist by the name of the artist
    and the search is case insensitive.
    It takes the name of the artist from the form and return all the artists the match this name.

    Return: 
            send the data of all the matched artists to the view.   
  '''       
  artist_name = request.form['search_term']
  search = "%{}%".format(artist_name)
  artists = Artist.query.filter(Artist.name.ilike(search)).all()
  data = []
  upcoming_shows_num = 0

  for artist in artists:
    shows = Show.query.filter_by(artist_id=artist.id).all()
    for show in shows:
      if show.start_time >= datetime.today():
        upcoming_shows_num += 1

    data.append({
      'id': artist.id,
      'name' : artist.name,
      'num_upcoming_shows' : upcoming_shows_num
    })
  response={
    "count": len(artists),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id): 
  '''
    This function is used to show the data of a specific artist.

    Arg: 
        artist_id : the id of the artist you want to show
    Return: 
            the data of the artist to the show_artist.html page    
  ''' 
  artist = Artist.query.get(artist_id) 
  shows = Show.query.filter_by(artist_id=artist_id).all()
  past_shows = []
  upcoming_shows = []

  for show in shows:
    if show.start_time < datetime.today():
      past_shows.append({
        "venue_id": show.venue_id,
        "venue_name": show.venues.name,
        "venue_image_link": show.venues.image_link,
        "start_time": show.start_time
      })
    else:
      upcoming_shows.append({
        "venue_id": show.venue_id,
        "venue_name": show.venues.name,
        "venue_image_link": show.venues.image_link,
        "start_time": show.start_time 
      })

  data = {
    "id": artist.id,
    "name": artist.name,
    "genres": str(artist.genres).split(','),
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": artist.facebook_link,
    "seeking_venue": False,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  '''
    This function is used to edit the data of a specific artist in the view.

    Arg: 
        artist_id : the id of the artist you want to edit his data
    Return: 
            the new data to the edit_artist.html page   
  '''      
  form = ArtistForm()
  recored = Artist.query.get(artist_id)
  artist={
    "id": recored.id,
    "name": recored.name,
    "genres": str(recored.genres).split(','),
    "city": recored.city,
    "state": recored.state,
    "phone": recored.phone,
    "facebook_link": recored.facebook_link,
    "seeking_venue": False,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!"
  }
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  '''
    This function is used to edit the data of a specific artist.
    it takes new data from the form and edit an existing artist

    Arg: 
        artist_id : the id of the artist you want to edit his data
    Return: 
            redirect to the show_artist page  
  '''      
  error = False
  try:
    artist = Artist.query.get(artist_id)
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.facebook_link = request.form['facebook_link']
    artist.genres = ','.join(request.form.getlist('genres'))
    db.session.add(artist)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close() 
  if not error:
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
  else:
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  '''
    This function is used to edit the data of a specific venue in the view.

    Arg: 
        venue_id : the id of the venue you want to edit his data
    Return: 
            the new data to the edit_venue.html page   
  '''      
  form = VenueForm()
  recored = Venue.query.get(venue_id)
  venue={
    "id": recored.id,
    "name": recored.name,
    "genres": str(recored.genres).split(','),
    "address": recored.address,
    "city": recored.city,
    "state": recored.state,
    "phone": recored.phone,
    "facebook_link": recored.facebook_link,
    "seeking_talent": False,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us."
  }
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  '''
    This function is used to edit the data of a specific venue.
    it takes new data from the form and edit an existing venue

    Arg: 
        venue_id : the id of the venue you want to edit his data
    Return: 
            redirect to the show_venue page  
  '''     
  error = False
  try:    
    venue = Venue.query.get(venue_id)
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.address = request.form['address']
    venue.phone = request.form['phone']
    venue.facebook_link = request.form['facebook_link']
    venue.genres = ','.join(request.form.getlist('genres'))
    db.session.add(venue)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close() 
  if not error:
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  else:
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')  
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  '''
    This function is used to create an artist form   
  '''      
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  '''
    This function is used to create a new artist in the database.
    it takes all the information of the artist from the form and create a new artist and 
    store it in the database.

    Return: 
            return to the home page
  '''  
            
  error = False
  try:
    recored = Artist()
    recored.name = request.form['name']
    recored.city = request.form['city']
    recored.state = request.form['state']
    recored.phone = request.form['phone']
    recored.facebook_link = request.form['facebook_link']
    recored.genres = ','.join(request.form.getlist('genres'))
    db.session.add(recored)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close() 
  if not error:
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
  else:
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  '''
    This function is used to send the data of the shows from the database to the view.

    Return: 
            the data to the shows.html page   
  '''      
  shows = Show.query.all()
  data = []
  for show in shows:
        data.append({
          "venue_id": show.venue_id,
          "venue_name": show.venues.name,
          "artist_id": show.artist_id,
          "artist_name": show.artists.name,
          "artist_image_link": show.artists.image_link,
          "start_time": str(show.start_time)
        })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  '''
    This function is used to create a new show in the database.
    it takes all the information of the show from the form and create a new show and 
    store it in the database.

    Return: 
            return to the home page
  '''       
  error = False
  try:
    recored = Show()
    recored.venue_id = request.form['venue_id']
    recored.artist_id = request.form['artist_id']
    recored.start_time = request.form['start_time']
    db.session.add(recored)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close() 
  if not error:
      flash('Show was successfully listed!')
  else:
    flash('An error occurred. Show could not be listed.')
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
