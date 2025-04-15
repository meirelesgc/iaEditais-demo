from datetime import datetime

import streamlit as st
from hooks import publication as order
from hooks import taxonomy
from streamlit_pdf_viewer import pdf_viewer


def format_date(date_str):
    if isinstance(date_str, str):
        dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f')
        return dt.strftime('%d/%m/%Y %H:%M:%S')
    return None


@st.dialog('Adicionar Edital', width='large')
def create_order():
    typifications = taxonomy.get_typifications()
    with st.form(key='create_order_form'):
        name = st.text_input('Nome do edital')
        type = st.multiselect(
            'Tipo do edital',
            options=typifications,
            format_func=lambda t: t['name'],
        )
        uploaded_file = st.file_uploader('Escolha um arquivo PDF', type='pdf')
        if st.form_submit_button('Adicionar Edital') and uploaded_file:
            ord = order.post_order(name, type)
            st.success('Edital criado com sucesso!')
            with st.status('Analisando versão...', expanded=True) as status:
                order.post_release(uploaded_file, ord['id'])
                status.update(label='Analise concluida!', state='complete')


@st.dialog('Adicionar Versão', width='large')
def create_release(ord):
    uploaded_file = st.file_uploader('Escolha um arquivo PDF', type='pdf')
    if st.button('Enviar arquivo') and uploaded_file:
        with st.status('Analisando versão...', expanded=True) as status:
            order.post_release(uploaded_file, ord['id'])
            status.update(label='Analise concluida!', state='complete')


def show_release(r):
    tabs = st.tabs([f'🧵 {t["name"]}' for t in r['taxonomy']])

    for tab_index, (tab, t) in enumerate(zip(tabs, r['taxonomy'])):
        tab_key = f'taxonomy_index_{tab_index}'

        if tab_key not in st.session_state:
            st.session_state[tab_key] = 0

        with tab:
            container = st.container()
            a, b, c = container.columns([1, 5, 1])

            if not t['taxonomy']:
                st.write('Não há itens de taxonomia disponíveis.')
                continue

            current_index = st.session_state[tab_key]
            current_index = min(current_index, len(t['taxonomy']) - 1)

            disabled_next = current_index >= len(t['taxonomy']) - 1
            next_button = c.button(
                '➡️ Proximo',
                disabled=disabled_next,
                key=f'next_{tab_index}_{current_index}',
            )

            disabled_back = current_index <= 0
            prev_button = a.button(
                '⬅️ Anterior',
                disabled=disabled_back,
                key=f'prev_{tab_index}_{current_index}',
            )

            if next_button and not disabled_next:
                st.session_state[tab_key] = current_index + 1
                st.rerun()

            if prev_button and not disabled_back:
                st.session_state[tab_key] = current_index - 1
                st.rerun()

            tx = t['taxonomy'][current_index]

            b.subheader(f'🪢 {tx["title"]}')
            for br in tx['branch']:
                st.caption(f'🪡 {br["title"]}')
                emote = '✅' if br['evaluate']['fulfilled'] else '❌'
                st.write(f'Critério cumprido: {emote}')
                st.write(f'Feedback: {br["evaluate"]["feedback"]}')
                st.divider()


def main():
    orders = order.get_order()
    if not orders:
        st.error('Nenhum edital encontrado.')
        return

    orders.sort(key=lambda x: x['created_at'], reverse=True)
    o = st.selectbox(
        'Selecione o edital',
        options=orders,
        format_func=lambda x: x['name'],
    )

    if st.button('🗑️ Excluir', use_container_width=True):
        order.delete_order(o['id'])

    if st.button(
        '➕ Adicionar Versão',
        key=o['id'],
        use_container_width=True,
    ):
        create_release(o)

    releases = sorted(
        order.get_release(o['id']) or [],
        key=lambda r: r['created_at'],
        reverse=True,
    )

    r = st.selectbox(
        'Selecione a versão',
        options=releases,
        format_func=lambda x: f'Edital {releases.index(x) + 1} - {format_date(x["created_at"])}',
    )
    if not releases:
        st.error('Nenhuma versão encontrada.')

    if r:
        col1, col2 = st.columns(2, gap='small')
        with col1:
            pdf_viewer(
                input=order.get_release_file(r['id']),
                key=f'pdf_viewer_{r["id"]}',
                width='100%',
                height=1000,
            )
        with col2:
            with st.container(height=1000):
                show_release(r)
