from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import EstadoCivil, Nacionalidad, Sexo, Estado, estado
from app.models.persona import Persona
from app.models.persona_x_tipodoc import PersonaXTipoDoc
from app.models.tipo_documento import TipoDocumento
from app.models.tipo_persona import TipoPersona
from app.models.persona_x_tipo import PersonaXTipo

persona_bp = Blueprint('personas', __name__, url_prefix='/personas')

# Definir combinaciones de tipos de persona no permitidas
COMBINACIONES_NO_PERMITIDAS = [
    {"Alumno", "Profesor"},
    {"Tutor", "Alumno"},
    {"Alumno", "Operador"},
    {"Profesor", "Operador"},
]

@persona_bp.route('/registrar', methods=['GET', 'POST'])
def registrar_persona():
    if request.method == 'POST':
        # Obtener datos del formulario y convertirlos a mayúsculas
        nombres = request.form.get('nombres').upper()
        apellidos = request.form.get('apellidos').upper()
        tipo_documento_id = request.form.get('tipo_documento')
        nro_documento = request.form.get('nro_documento')
        correo = request.form.get('correo').lower()  # Convertir el correo a mayúsculas
        fecha_nacimiento = request.form.get('fecha_nacimiento')
        direccion = request.form.get('direccion').upper()  # Convertir la dirección a mayúsculas
        ciudad = request.form.get('ciudad').upper()  # Convertir la ciudad a mayúsculas
        telefono = request.form.get('telefono')
        sexo_id = request.form.get('sexo')
        estado_civil_id = request.form.get('estado_civil')
        nacionalidad_id = request.form.get('nacionalidad')
        tipos_persona_seleccionados = request.form.getlist('tipos_persona')

        # Validaciones
        documento_existente = PersonaXTipoDoc.query.filter_by(
            tipo_documento_id=tipo_documento_id, nro_documento=nro_documento,nacionalidad_id=nacionalidad_id
        ).first()

        if documento_existente:
            flash('Este número de documento ya existe', 'danger')
            return render_template('personas/registrar_persona.html', **contexto_formulario(
                nombres=nombres, apellidos=apellidos, tipo_documento_id=tipo_documento_id,
                nro_documento=nro_documento, correo=correo, fecha_nacimiento=fecha_nacimiento,
                direccion=direccion, ciudad=ciudad, telefono=telefono, sexo_id=sexo_id,
                estado_civil_id=estado_civil_id, nacionalidad_id=nacionalidad_id,
                tipos_persona_seleccionados=tipos_persona_seleccionados
            ))

        if not telefono.isdigit():
            flash('El número de teléfono debe contener solo dígitos.', 'danger')
            return render_template('personas/registrar_persona.html', **contexto_formulario(
                nombres=nombres, apellidos=apellidos, tipo_documento_id=tipo_documento_id,
                nro_documento=nro_documento, correo=correo, fecha_nacimiento=fecha_nacimiento,
                direccion=direccion, ciudad=ciudad, telefono=telefono, sexo_id=sexo_id,
                estado_civil_id=estado_civil_id, nacionalidad_id=nacionalidad_id,
                tipos_persona_seleccionados=tipos_persona_seleccionados
            ))

        correo_existente = Persona.query.filter_by(correo=correo).first()
        if correo_existente:
            flash('El correo ya existe, por favor use otro', 'danger')
            return render_template('personas/registrar_persona.html', **contexto_formulario(
                nombres=nombres, apellidos=apellidos, tipo_documento_id=tipo_documento_id,
                nro_documento=nro_documento, correo=correo, fecha_nacimiento=fecha_nacimiento,
                direccion=direccion, ciudad=ciudad, telefono=telefono, sexo_id=sexo_id,
                estado_civil_id=estado_civil_id, nacionalidad_id=nacionalidad_id,
                tipos_persona_seleccionados=tipos_persona_seleccionados
            ))

        # Obtener nombres de los tipos de persona seleccionados
        tipos_persona_nombres = [TipoPersona.query.get(tipo_id).nombre for tipo_id in tipos_persona_seleccionados]

        # Verificar combinaciones no permitidas
        tipos_seleccionados_set = set(tipos_persona_nombres)
        for combinacion_no_permitida in COMBINACIONES_NO_PERMITIDAS:
            if combinacion_no_permitida.issubset(tipos_seleccionados_set):
                flash(f'No puedes seleccionar las opciones: {", ".join(combinacion_no_permitida)} al mismo tiempo.',
                      'danger')
                return render_template('personas/registrar_persona.html', **contexto_formulario(
                    # Pasar valores al formulario para recargarlo con datos
                ))

        estado_activo = Estado.query.filter_by(nombre='Activo').first()

        # Guardar los datos en la base de datos
        nueva_persona = Persona(
            nombres=nombres,
            apellidos=apellidos,
            correo=correo,
            fecha_nacimiento=fecha_nacimiento,
            direccion=direccion,
            ciudad=ciudad,
            telefono=telefono,
            sexo_id=sexo_id,
            estado_civil_id=estado_civil_id,
            estado=estado_activo
        )
        db.session.add(nueva_persona)
        db.session.commit()

        persona_doc = PersonaXTipoDoc(
            persona_id=nueva_persona.id,
            tipo_documento_id=tipo_documento_id,
            nro_documento=nro_documento,
            nacionalidad_id=nacionalidad_id
        )
        db.session.add(persona_doc)
        db.session.commit()

        for tipo_id in tipos_persona_seleccionados:
            persona_tipo = PersonaXTipo(
                persona_id=nueva_persona.id,
                tipo_persona_id=tipo_id
            )
            db.session.add(persona_tipo)

        db.session.commit()

        flash('Persona registrada exitosamente', 'success')
        return redirect(url_for('personas.registrar_persona'))

    # GET request (mostrar formulario)
    return render_template('personas/registrar_persona.html', **contexto_formulario())

def contexto_formulario(nombres='', apellidos='', tipo_documento_id=None, nro_documento='', correo='', fecha_nacimiento='', direccion='', ciudad='', telefono='', sexo_id=None, estado_civil_id=None, nacionalidad_id=None, tipos_persona_seleccionados=[]):
    return {
        'nombres': nombres,
        'apellidos': apellidos,
        'tipo_documento': tipo_documento_id,
        'nro_documento': nro_documento,
        'correo': correo,
        'fecha_nacimiento': fecha_nacimiento,
        'direccion': direccion,
        'ciudad': ciudad,
        'telefono': telefono,
        'sexo_id': sexo_id,
        'estado_civil_id': estado_civil_id,
        'nacionalidad_id': nacionalidad_id,
        'tipos_persona_seleccionados': tipos_persona_seleccionados,
        'tipos_documento': TipoDocumento.query.all(),
        'tipos_persona': TipoPersona.query.all(),
        'sexos': Sexo.query.all(),
        'nacionalidades': Nacionalidad.query.all(),
        'estados_civiles': EstadoCivil.query.all()
    }


@persona_bp.route('/listar', methods=['GET', 'POST'])
def listar_personas():
    # Obtener el término de búsqueda si existe
    termino_busqueda = request.args.get('q', '').lower()

    # Concatenar apellidos y nombres en formato 'Apellido, Nombre'
    personas = Persona.query.filter(
        db.func.concat(Persona.apellidos, ', ', Persona.nombres).ilike(f"%{termino_busqueda}%")
    ).all()

    return render_template('personas/listar_personas.html', personas=personas, termino_busqueda=termino_busqueda)


@persona_bp.route('/buscar_personas')
def buscar_personas():
    query = request.args.get('query', '')
    if query:
        # Realiza la búsqueda en la base de datos
        personas = Persona.query.filter(
            (Persona.nombres.like(f'%{query}%')) |
            (Persona.apellidos.like(f'%{query}%'))
        ).all()

        # Combina apellidos y nombres y crea una lista para el JSON
        resultados = [f"{persona.apellidos}, {persona.nombres}" for persona in personas]
    else:
        resultados = []

    return jsonify(resultados)



@persona_bp.route('/editar/<int:persona_id>', methods=['GET', 'POST'])
def editar_persona(persona_id):
    persona = Persona.query.get_or_404(persona_id)  # Obtener la persona por ID

    if request.method == 'POST':
        # Actualizar los datos de la persona con los datos del formulario
        persona.nombres = request.form.get('nombres').upper()
        persona.apellidos = request.form.get('apellidos').upper()
        persona.correo = request.form.get('correo').lower()
        persona.telefono = request.form.get('telefono')

        db.session.commit()
        flash('Persona actualizada exitosamente', 'success')
        return redirect(url_for('personas.listar_personas'))

    # Mostrar el formulario con los datos actuales de la persona
    return render_template('personas/editar_persona.html', persona=persona)
