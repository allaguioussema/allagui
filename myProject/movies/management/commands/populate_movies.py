from django.core.management.base import BaseCommand
from movies.models import Movie

class Command(BaseCommand):
    help = 'Populates the database with movies for each emotion'

    def handle(self, *args, **kwargs):
        # Clear existing movies
        Movie.objects.all().delete()

        movies_data = {
            'disgust': [
                {'title': 'The Human Centipede', 'year': 2009, 'rating': 4.4, 'description': 'A mad scientist kidnaps and mutilates three tourists.'},
                {'title': 'Pink Flamingos', 'year': 1972, 'rating': 6.1, 'description': 'Notorious Waters film about the filthiest person alive.'},
                {'title': 'Neon Demon', 'year': 2016, 'rating': 6.2, 'description': 'A dark tale of beauty and cannibalism in the fashion world.'},
                {'title': 'Tusk', 'year': 2014, 'rating': 5.3, 'description': 'A man is surgically transformed into a walrus.'},
                {'title': 'Society', 'year': 1989, 'rating': 6.5, 'description': 'Body horror film about upper-class society.'},
                {'title': 'Slither', 'year': 2006, 'rating': 6.5, 'description': 'Alien parasites turn townspeople into zombies.'},
                {'title': 'Eraserhead', 'year': 1977, 'rating': 7.4, 'description': 'Surreal horror about a man caring for his deformed child.'},
                {'title': 'Taxidermia', 'year': 2006, 'rating': 6.6, 'description': 'Three generations of men with bizarre obsessions.'},
                {'title': 'Salo', 'year': 1975, 'rating': 5.9, 'description': 'Controversial film about fascism and degradation.'},
                {'title': 'Feed', 'year': 2005, 'rating': 5.3, 'description': 'Detective investigates underground force-feeding fetish community.'},
            ],
            'fear': [
                {'title': 'The Conjuring', 'year': 2013, 'rating': 7.5, 'description': 'Paranormal investigators help a family terrorized by a dark presence.'},
                {'title': 'Hereditary', 'year': 2018, 'rating': 7.3, 'description': 'A family unravels cryptic and terrifying secrets about their ancestry.'},
                {'title': 'The Babadook', 'year': 2014, 'rating': 6.8, 'description': 'A single mother and her son battle a supernatural creature.'},
                {'title': 'A Quiet Place', 'year': 2018, 'rating': 7.5, 'description': 'A family must live in silence to avoid mysterious creatures.'},
                {'title': 'Get Out', 'year': 2017, 'rating': 7.7, 'description': "A young African-American visits his white girlfriend's parents."},
                {'title': 'The Thing', 'year': 1982, 'rating': 8.2, 'description': 'Scientists encounter a shape-shifting alien in Antarctica.'},
                {'title': 'Alien', 'year': 1979, 'rating': 8.5, 'description': 'Space crew battles a deadly extraterrestrial.'},
                {'title': 'The Shining', 'year': 1980, 'rating': 8.4, 'description': 'A family becomes isolated in a haunted hotel.'},
                {'title': 'It Follows', 'year': 2014, 'rating': 6.8, 'description': 'A teenager is pursued by a supernatural entity.'},
                {'title': 'The Descent', 'year': 2005, 'rating': 7.2, 'description': 'Six women encounter underground predators while caving.'},
            ],
            'happiness': [
                {'title': 'La La Land', 'year': 2016, 'rating': 8.0, 'description': 'A musician and aspiring actress fall in love in Los Angeles.'},
                {'title': 'The Intouchables', 'year': 2011, 'rating': 8.5, 'description': 'An unlikely friendship between a quadriplegic and his caregiver.'},
                {'title': 'Singing in the Rain', 'year': 1952, 'rating': 8.3, 'description': "Silent film production company transitions to talkies."},
                {'title': 'Toy Story', 'year': 1995, 'rating': 8.3, 'description': "Toys come to life when humans aren't present."},
                {'title': 'The Princess Bride', 'year': 1987, 'rating': 8.0, 'description': 'A classic tale of love and adventure.'},
                {'title': 'Mary Poppins', 'year': 1964, 'rating': 7.8, 'description': 'Magical nanny brings joy to a troubled family.'},
                {'title': 'Big', 'year': 1988, 'rating': 7.3, 'description': "A boy's wish to be big comes true."},
                {'title': 'School of Rock', 'year': 2003, 'rating': 7.1, 'description': 'Fake substitute teacher forms a rock band with students.'},
                {'title': 'The Lego Movie', 'year': 2014, 'rating': 7.7, 'description': 'An ordinary Lego figure leads a resistance movement.'},
                {'title': 'Up', 'year': 2009, 'rating': 8.2, 'description': 'Elderly widower goes on an adventure in his flying house.'},
            ],
            'sadness': [
                {'title': "Schindler's List", 'year': 1993, 'rating': 9.0, 'description': 'Businessman saves Jews during the Holocaust.'},
                {'title': 'The Green Mile', 'year': 1999, 'rating': 8.6, 'description': 'Death row inmates and guards are affected by a mysterious inmate.'},
                {'title': 'Grave of the Fireflies', 'year': 1988, 'rating': 8.5, 'description': 'Two siblings struggle to survive in WWII Japan.'},
                {'title': 'The Boy in the Striped Pajamas', 'year': 2008, 'rating': 7.8, 'description': 'Friendship between two boys on opposite sides of a concentration camp.'},
                {'title': 'Manchester by the Sea', 'year': 2016, 'rating': 7.8, 'description': 'A man becomes guardian of his teenage nephew.'},
                {'title': 'Dear Zachary', 'year': 2008, 'rating': 8.5, 'description': 'Documentary about a murdered man made for his unborn son.'},
                {'title': 'Million Dollar Baby', 'year': 2004, 'rating': 8.1, 'description': 'A boxing trainer takes a female boxer under his wing.'},
                {'title': 'Life is Beautiful', 'year': 1997, 'rating': 8.6, 'description': 'Father shields his son from Nazi concentration camp horrors.'},
                {'title': 'Requiem for a Dream', 'year': 2000, 'rating': 8.3, 'description': 'Four individuals struggle with drug addiction.'},
                {'title': 'The Road', 'year': 2009, 'rating': 7.2, 'description': 'Father and son journey through post-apocalyptic America.'},
            ],
            'anger': [
                {'title': 'Falling Down', 'year': 1993, 'rating': 7.6, 'description': 'Unemployed defense worker reaches his breaking point.'},
                {'title': 'Whiplash', 'year': 2014, 'rating': 8.5, 'description': 'Music student endures abuse from his instructor.'},
                {'title': 'Network', 'year': 1976, 'rating': 8.1, 'description': 'TV anchor has a mental breakdown on air.'},
                {'title': 'Taxi Driver', 'year': 1976, 'rating': 8.2, 'description': 'Vietnam veteran works as a taxi driver in New York City.'},
                {'title': '12 Angry Men', 'year': 1957, 'rating': 9.0, 'description': 'Jury members deliberate on a murder case.'},
                {'title': 'There Will Be Blood', 'year': 2007, 'rating': 8.2, 'description': "Oil prospector's ambition leads to conflict."},
                {'title': 'American History X', 'year': 1998, 'rating': 8.5, 'description': 'Former neo-nazi tries to prevent his brother from following his path.'},
                {'title': 'Oldboy', 'year': 2003, 'rating': 8.4, 'description': 'Man seeks revenge after being imprisoned for 15 years.'},
                {'title': 'The Hunt', 'year': 2012, 'rating': 8.3, 'description': "Teacher's life unravels after being falsely accused."},
                {'title': 'Inglourious Basterds', 'year': 2009, 'rating': 8.3, 'description': 'Jewish soldiers spread terror among Nazis in occupied France.'},
            ],
            'neutral': [
                {'title': 'The Grand Budapest Hotel', 'year': 2014, 'rating': 8.1, 'description': 'Adventures of a legendary hotel concierge.'},
                {'title': '2001: A Space Odyssey', 'year': 1968, 'rating': 8.3, 'description': 'Journey through space and time.'},
                {'title': 'Lost in Translation', 'year': 2003, 'rating': 7.7, 'description': 'Two Americans form an unlikely bond in Tokyo.'},
                {'title': 'Drive', 'year': 2011, 'rating': 7.8, 'description': 'Stunt driver moonlights as a getaway driver.'},
                {'title': 'Her', 'year': 2013, 'rating': 8.0, 'description': 'Man develops relationship with AI operating system.'},
                {'title': 'The Life Aquatic', 'year': 2004, 'rating': 7.3, 'description': 'Oceanographer seeks revenge on shark.'},
                {'title': 'Moon', 'year': 2009, 'rating': 7.8, 'description': 'Astronaut nearing end of solitary mission makes discovery.'},
                {'title': 'Under the Skin', 'year': 2013, 'rating': 6.3, 'description': 'Alien in human form journeys through Scotland.'},
                {'title': 'Only Lovers Left Alive', 'year': 2013, 'rating': 7.2, 'description': 'Centuries-old vampires reunite.'},
                {'title': 'Ghost Story', 'year': 2017, 'rating': 6.9, 'description': 'Ghost observes his grieving wife.'},
            ],
            'surprise': [
                {'title': 'The Usual Suspects', 'year': 1995, 'rating': 8.5, 'description': 'A sole survivor tells of the twisty events leading up to a horrific gun battle on a boat.'},
                {'title': 'Fight Club', 'year': 1999, 'rating': 8.8, 'description': 'An insomniac office worker and a devil-may-care soapmaker form an underground fight club.'},
                {'title': 'The Sixth Sense', 'year': 1999, 'rating': 8.1, 'description': 'A child psychologist tries to help a boy who can see dead people.'},
                {'title': 'Inception', 'year': 2010, 'rating': 8.8, 'description': 'A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea.'},
                {'title': 'Memento', 'year': 2000, 'rating': 8.4, 'description': 'A man with short-term memory loss attempts to track down his wife\'s murderer.'},
                {'title': 'Shutter Island', 'year': 2010, 'rating': 8.2, 'description': 'A U.S. Marshal investigates the disappearance of a murderer who escaped from a hospital for the criminally insane.'},
                {'title': 'Oldboy', 'year': 2003, 'rating': 8.4, 'description': 'After being kidnapped and imprisoned for fifteen years, Oh Dae-Su is released, only to find that he must find his captor in five days.'},
                {'title': 'Predestination', 'year': 2014, 'rating': 7.5, 'description': 'A temporal agent embarks on a final time-traveling assignment to prevent an elusive criminal from launching an attack.'},
                {'title': 'The Prestige', 'year': 2006, 'rating': 8.5, 'description': 'Two stage magicians engage in competitive one-upmanship in an attempt to create the ultimate stage illusion.'},
                {'title': 'Planet of the Apes', 'year': 1968, 'rating': 8.0, 'description': 'An astronaut crew crash-lands on a planet where intelligent talking apes are the dominant species.'},
            ],
        }

        for emotion, movies in movies_data.items():
            for movie in movies:
                Movie.objects.create(
                    title=movie['title'],
                    year=movie['year'],
                    rating=movie['rating'],
                    description=movie['description'],
                    emotion=emotion,
                    image_url=f'https://via.placeholder.com/300x450?text={movie["title"].replace(" ", "+")}'
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated movies database'))
