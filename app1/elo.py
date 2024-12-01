from app1.db import get_db

import random









'''
This function calculates the elo rating of the players and returns their output as a two dimensional array 
of the updated elo ratings of the two players. 

A - Elo of Player A 

B - Elo of Player B 

winner - Which player won out of the two (denoted by a 0 for player A and 1 for player B)

Draws are excluded from this calculation

'''
def calculateElo(A, B, winner):
    if winner == 0:
        #Means that Player A won 
        expectedA = expectedScore(A, B)

        expectedB = expectedScore(B, A)

        newEloA = A + 32*(1 - expectedA)

        newEloB = B + 32*(0 - expectedB)

        newEloRatings = [newEloA, newEloB]

        return newEloRatings


    else:
        #Means that Player B won 
        expectedA = expectedScore(A, B)

        expectedB = expectedScore(B, A)

        newEloA = A + 32*(0 - expectedA)

        newEloB = B + 32*(1 - expectedB)

        newEloRatings = [newEloA, newEloB]

        return newEloRatings


'''

Expected score calculator

A - denotes the elo of player A 

B - denotes the elo of player B

Finds the Expected score of player A.

'''
def expectedScore(A, B):
    elo = 1 / (1 + 10**((B - A)/400))

    return elo

"""
This inserts an image into the database. It first checks if the image is already there, if it is, then makes sure that 
its elo is 1400 at the beginning of the game
"""
def insertImage(imageLink, id):

    db = get_db()
    
    image = db.execute(
        'SELECT * FROM images WHERE link = ?', (imageLink,)
    ).fetchone()

    if image is None: 
        db.execute(
            'INSERT INTO images (id, link, elo) VALUES (?, ?)', (id, imageLink, 1400),
        )

        db.commit()

    else:
        db.execute (
            'UPDATE images SET elo = 1400 where link = ?', (imageLink,)
        )

        db.commit()


"""
This function will insert all the images in the game, 
the images in the game are up to the discretion of the developer. 

Images can be added or removed by changing the array below. 
It is paramount that images are only added if they occur in the static files, otherwise this 
will break the application.
"""
def InsertImages():
    images = ['cat.jpeg', 'dachshund.jpg', 'Groodle.jpg', 'shiba.jpg', 'spoodle.jpg']

    id = 0

    for image in images:
        insertImage(image, id)
        id = id + 1





"""
This function will display the images that the user has to choose from

Currently, the matchmaking is random, however will hope to update this method soon

returns an array of two integers
"""
def matchMake():
    db = get_db()

    numImages = db.execute(
        'SELECT count(*) AS count FROM images'
    ).fetchone()



    n = numImages['count']

    


    index1 = random.randrange(1, n)

    index2 = random.randrange(1, n)

    while index2 == index1:
        index2 = random.randrange(1, n)
    

    array = [index1, index2]

    return array





    
















    



    

    

