from flask import Blueprint, render_template, request
from pokemon.models import Pokemon


core = Blueprint('core', __name__, template_folder='templates')

@core.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pokemons = Pokemon.query.paginate(page=page, per_page=10)

    return render_template(
        'core/index.html',
        title='Home Page',
        pokemons=pokemons
    )
