import click
import random

import datetime

from faker import Faker
from sqlalchemy_utils import database_exists, create_database

from magicride import create_app
from magicride.extensions import db

from magicride.modules.parks.models import Park
from magicride.modules.rides.models import Ride, RideType
from magicride.modules.bookmarks.models import Bookmark
from magicride.modules.users.models import User
from magicride.modules.reviews.models import Review
from magicride.modules.operators.models import Operator
from magicride.modules.businesshours.models import BusinessHours
from magicride.modules.geo.models import Location


# Create an app context for the database connection.
app = create_app()
db.app = app
fake = Faker()


@click.group()
def cli():
    """ Run PostgreSQL related tasks. """
    pass

def _log_status(count, model_label):
    """
    Log the output of how many records were created.

    :param count: Amount created
    :type count: int
    :param model_label: Name of the model
    :type model_label: str
    :return: None
    """
    click.echo('Created {0} {1}'.format(count, model_label))

    return None


def _bulk_insert(model, data, label):
    """
    Bulk insert data to a specific model and log it. This is much more
    efficient than adding 1 row at a time in a loop.

    :param model: Model being affected
    :type model: SQLAlchemy
    :param data: Data to be saved
    :type data: list
    :param label: Label for the output
    :type label: str
    :param skip_delete: Optionally delete previous records
    :type skip_delete: bool
    :return: None
    """
    with app.app_context():
        db.session.begin()
        model.query.delete()

        db.session.commit()
        db.engine.execute(model.__table__.insert(), data)

        _log_status(model.query.count(), label)

    return None


@click.group()
def cli():
    """ Add items to the database. """
    pass


@click.command()
def parks():
    """
    Generate random parks.
    """
    data = []
    num_of_rides = 99

    click.echo('Working on parks...')
    with app.app_context():
        operators = db.session.query(Operator).all()

        while num_of_rides >= 0:
            operator = random.choice(operators)
            park_name = operator.name + " - " + fake.city()
            address = fake.address()
            location = Location(fake.latitude(), fake.longitude()).to_wkt_element()
            price = round(random.uniform(50, 150), 2)

            params = {
                'name': park_name,
                'address': address,
                'location': location,
                'admission_price': price,
                'operator_id': operator.id,
                'business_hours': 1
            }

            data.append(params)
            num_of_rides -= 1

        return _bulk_insert(Park, data, 'parks')


@click.command()
def operators():
    """
    Generate random operators.
    """
    data = []
    operators = ['Disney', 'Six Flags', 'Universal Studios']

    for op in operators:

        params = {
            'name': op
        }

        data.append(params)
    with app.app_context():
        return _bulk_insert(Operator, data, 'operators')


@click.command()
def businesshours():
    """
    Generate random businesshours.
    """
    data = []
    with app.app_context():
        start = datetime.time(10, 00, 00)
        close = datetime.time(20, 00, 00)

        params = {
            'opening_time': start,
            'closing_time': close,
        }

        data.append(params)

        return _bulk_insert(BusinessHours, data, 'business_hours')


@click.command()
def ridetypes():
    """
    Generate random ridetypes.
    """
    data = []
    ride_types = ['Roller Coaster', 'Ferris Wheel', 'Animatronic']

    for ride in ride_types:

        params = {
            'ride_type': ride
        }

        data.append(params)
    with app.app_context():
        return _bulk_insert(RideType, data, 'ride_types')


@click.command()
def rides():
    """
    Generate random rides.
    """
    random_ride_names = ['Gale Force Rise', 'Bat Rush', 'Dragon Flight',
                         'Dragon Hunter', 'Adventure Express',
                         'Cedar Creek Mine Ride', 'Crazy Mouse']
    data = []

    click.echo('Working on rides...')
    with app.app_context():
        ride_types = db.session.query(RideType).all()
        parks = db.session.query(Park).all()

        for park in parks:
            name = random.choice(random_ride_names)
            min_height_in_cm = round(random.uniform(100, 227), 2)
            ride_type = random.choice(ride_types)
            min_age = random.randint(5, 18)
            park_id = park.id

            params = {
                'ride_name': name,
                'min_height_in_cm': min_height_in_cm,
                'ride_type_id': ride_type.id,
                'min_age': min_age,
                'park_id': park_id
            }

            data.append(params)
        return _bulk_insert(Ride, data, 'rides')


@click.command()
@click.option('--with-testdb/--no-with-testdb', default=False,
              help='Create a test db too?')
def init(with_testdb):
    """
    Initialize the database.

    :param with_testdb: Create a test database
    :return: None
    """
    db.drop_all()
    db.create_all()

    if with_testdb:
        db_uri = '{0}_test'.format(app.config['SQLALCHEMY_DATABASE_URI'])

        if not database_exists(db_uri):
            create_database(db_uri)

    return None


@click.command()
@click.option('--with-testdb/--no-with-testdb', default=False,
              help='Create a test db too?')
@click.pass_context
def reset(ctx, with_testdb):
    """
    Init and seed automatically.

    :param with_testdb: Create a test database
    :return: None
    """
    ctx.invoke(init, with_testdb=with_testdb)
    ctx.invoke(operators)
    ctx.invoke(businesshours)
    ctx.invoke(parks)
    ctx.invoke(ridetypes)
    ctx.invoke(rides)
    return None


cli.add_command(init)
cli.add_command(reset)
