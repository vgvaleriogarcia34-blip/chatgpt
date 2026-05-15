const DB_KEY = 'mini-crm-db';

const state = JSON.parse(localStorage.getItem(DB_KEY) || '{"contactos":[],"oportunidades":[],"tareas":[]}');

const save = () => localStorage.setItem(DB_KEY, JSON.stringify(state));

const renderList = (items, targetId, formatter, removeCb) => {
  const ul = document.getElementById(targetId);
  ul.innerHTML = '';
  items.forEach((item, idx) => {
    const li = document.createElement('li');
    const main = document.createElement('div');
    main.className = 'item-main';
    main.innerHTML = formatter(item);

    const del = document.createElement('button');
    del.textContent = 'Eliminar';
    del.className = 'delete';
    del.addEventListener('click', () => removeCb(idx));

    li.append(main, del);
    ul.appendChild(li);
  });
};

function render() {
  renderList(
    state.contactos,
    'contact-list',
    (c) => `<strong>${c.nombre}</strong><br>${c.empresa}<br>${c.email}`,
    (idx) => { state.contactos.splice(idx, 1); save(); render(); }
  );

  renderList(
    state.oportunidades,
    'deal-list',
    (d) => `<strong>${d.titulo}</strong><br>Valor: $${Number(d.valor).toLocaleString()}<br>Etapa: ${d.etapa}`,
    (idx) => { state.oportunidades.splice(idx, 1); save(); render(); }
  );

  renderList(
    state.tareas,
    'task-list',
    (t) => `<strong>${t.descripcion}</strong><br>Vence: ${t.fecha}`,
    (idx) => { state.tareas.splice(idx, 1); save(); render(); }
  );
}

const bindForm = (formId, targetArray, fields) => {
  document.getElementById(formId).addEventListener('submit', (e) => {
    e.preventDefault();
    const form = e.target;
    const data = Object.fromEntries(fields.map((f) => [f, form[f].value.trim()]));
    targetArray.push(data);
    save();
    form.reset();
    render();
  });
};

bindForm('contact-form', state.contactos, ['nombre', 'empresa', 'email']);
bindForm('deal-form', state.oportunidades, ['titulo', 'valor', 'etapa']);
bindForm('task-form', state.tareas, ['descripcion', 'fecha']);

render();
