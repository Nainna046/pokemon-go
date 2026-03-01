from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from pokemon.extensions import db
from pokemon.models import Pokemon, Type   # ✅ เพิ่ม Type

pokemon_bp = Blueprint('pokemon', __name__, template_folder='templates')


# ================= POKEMON LIST =================
@pokemon_bp.route('/pokemon')
@login_required
def index():
    pokemons = Pokemon.query.order_by(Pokemon.id).all()
    return render_template(
        'pokemon.html',
        title='Pokemon Page',
        pokemons=pokemons
    )


# ================= CREATE POKEMON =================
@pokemon_bp.route('/pokemon/new', methods=['GET', 'POST'])
@login_required
def create_pokemon():

    # ✅ ดึง type ทั้ง 18
    types = Type.query.order_by(Type.name).all()

    if request.method == 'POST':
        name = request.form.get('name')
        height = request.form.get('height')
        weight = request.form.get('weight')
        description = request.form.get('description')
        img_url = request.form.get('img_url')

        # ✅ รับ type ที่เลือก (หลายค่า)
        type_ids = request.form.getlist('types')

        # 🔍 กันชื่อซ้ำ
        exists = Pokemon.query.filter_by(name=name).first()
        if exists:
            flash('Pokemon name already exists!', 'warning')
            return redirect(url_for('pokemon.create_pokemon'))

        # ✅ สร้าง pokemon
        new_pokemon = Pokemon(
            name=name,
            height=height,
            weight=weight,
            description=description,
            img_url=img_url,
            user_id=current_user.id
        )

        # ✅ ผูก type
        if type_ids:
            selected_types = Type.query.filter(Type.id.in_(type_ids)).all()
            new_pokemon.types = selected_types

        db.session.add(new_pokemon)
        db.session.commit()

        flash('Pokemon created successfully!', 'success')
        return redirect(url_for('pokemon.index'))

    return render_template(
        'pokemon_form.html',
        title='New Pokemon',
        types=types   # ✅ สำคัญ!!!
    )