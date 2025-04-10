from datetime import datetime

import pandas as pd
import streamlit as st
from hooks import publication as order
from hooks import taxonomy


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

    for idx, (tab, t) in enumerate(zip(tabs, r['taxonomy'])):
        with tab:
            key = f'taxonomy_index_{idx}'
            if key not in st.session_state:
                st.session_state[key] = 0

            current_index = st.session_state[key]
            tx = t['taxonomy'][current_index]

            st.subheader(f'🪢 {tx["title"]}')
            for br in tx['branch']:
                st.caption(f'🪡 {br["title"]}')
                emote = '✅' if br['evaluate']['fulfilled'] else '❌'
                st.write(f'Critério cumprido: {emote}')
                st.write(f'Feedback: {br["evaluate"]["feedback"]}')
                st.divider()
            col1, col2 = st.columns(2)
            with col1:
                if (
                    st.button('◀️ Anterior', key=f'prev_{idx}')
                    and current_index > 0
                ):
                    st.session_state[key] -= 1
            with col2:
                if (
                    st.button('Próximo ▶️', key=f'next_{idx}')
                    and current_index < len(t['taxonomy']) - 1
                ):
                    st.session_state[key] += 1


def main():
    st.header('📊 Gestão de Editais')
    st.divider()
    if st.button('➕ Adicionar Edital', use_container_width=True):
        create_order()

    orders = order.get_order()
    if not orders:
        st.error('Nenhum edital encontrado.')
        return

    typifications = taxonomy.get_typifications()

    data = []

    for o in orders:
        related_typs = [
            ty['name'] for ty in typifications if ty['id'] in o['typification']
        ]

        data.append({
            'Ordem': o['name'],
            'Tipificações': '; '.join(related_typs)
            if related_typs
            else 'Nenhuma',
        })

    df = pd.DataFrame(data)
    st.table(df)
