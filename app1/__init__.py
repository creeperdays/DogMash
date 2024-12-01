import os 

from flask import (Flask, render_template, request, session, url_for, redirect) 

from app1.db import get_db

from . import elo 

def create_app():
    app = Flask(__name__, instance_relative_config = True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'application.sqlite'),
    )


    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass



    from . import db
    db.init_app(app)


    @app.route('/')
    def hello():
        elo.InsertImages()
        return render_template('buttons.html')
    
    @app.route('/play', methods = ('GET', 'POST'))
    def play():
        if request.method == 'POST':
            db = get_db()

            if request.form['Image'] == session.get('Image1'):
                image1 = db.execute(
                    'SELECT * FROM images WHERE link = ?', (session.get('Image1'),)
                ).fetchone()

                image2 = db.execute(
                    'SELECT * FROM images WHERE link = ?', (session.get('Image2'),)
                ).fetchone()

                newRatings = elo.calculateElo(image1['elo'], image2['elo'], 0)

                db.execute(
                    'UPDATE images SET elo = ? WHERE link = ?', (newRatings[0], session.get('Image1'))
                )

                db.commit()

                db.execute(
                    'UPDATE images SET elo = ? WHERE link = ?', (newRatings[1], session.get('Image2'))
                )

                db.commit()

                db = get_db()

                indexes = elo.matchMake()
                i1 = indexes[0]
                i2 = indexes[1]
                image1 = db.execute(
                    'SELECT * FROM images WHERE id = ?', (i1,)
                ).fetchone()
                image2 = db.execute(
                    'SELECT * FROM images WHERE id = ?', (i2,)
                ).fetchone() 
                link1 = image1['link']
                link2 = image2['link']
                session.clear()
                session['Image1'] = image1['link']
                session['Image2'] = image2['link']
                return render_template('Play.html', Image1 = link1, Image2 = link2, elo1 = image1['elo'], elo2 = image2['elo'])

                
            
            elif request.form['Image'] == session.get('Image2'):
                image1 = db.execute(
                    'SELECT * FROM images WHERE link = ?', (session.get('Image1'),)
                ).fetchone()

                image2 = db.execute(
                    'SELECT * FROM images WHERE link = ?', (session.get('Image2'),)
                ).fetchone()

                newRatings = elo.calculateElo(image1['elo'], image2['elo'], 1)

                db.execute(
                    'UPDATE images SET elo = ? WHERE link = ?', (newRatings[0], session.get('Image1'))
                )

                db.commit()

                db.execute(
                    'UPDATE images SET elo = ? WHERE link = ?', (newRatings[1], session.get('Image2'))
                )

                db.commit()

                indexes = elo.matchMake()
                i1 = indexes[0]
                i2 = indexes[1]
                image1 = db.execute(
                    'SELECT * FROM images WHERE id = ?', (i1,)
                ).fetchone()
                image2 = db.execute(
                    'SELECT * FROM images WHERE id = ?', (i2,)
                ).fetchone() 
                link1 = image1['link']
                link2 = image2['link']
                session.clear()
                session['Image1'] = image1['link']
                session['Image2'] = image2['link']
                return render_template('Play.html', Image1 = link1, Image2 = link2, elo1 = image1['elo'], elo2 = image2['elo'])


        db = get_db()

        indexes = elo.matchMake()

        

        i1 = indexes[0]

        i2 = indexes[1]

        image1 = db.execute(
            'SELECT * FROM images WHERE id = ?', (i1,)
        ).fetchone()

      

        image2 = db.execute(
            'SELECT * FROM images WHERE id = ?', (i2,)
        ).fetchone() 

        link1 = image1['link']

        link2 = image2['link']

        session.clear()

        session['Image1'] = image1['link']
        session['Image2'] = image2['link']



        return render_template('Play.html', Image1 = link1, Image2 = link2, elo1 = image1['elo'], elo2 = image2['elo'])
    
    @app.route('/rules')
    def rules():
        return render_template('Rules.html')

    return app





