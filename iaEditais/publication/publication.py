from datetime import datetime

import streamlit as st
from hooks import publication as order
from hooks import taxonomy
from streamlit_pdf_viewer import pdf_viewer


def main():
    typifications = taxonomy.get_typifications()

    def format_date(date_str):
        if isinstance(date_str, str):
            dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f')
            return dt.strftime('%d/%m/%Y %H:%M:%S')
        return None

    @st.dialog('Adicionar Edital', width='large')
    def create_order():
        with st.form(key='create_order_form'):
            name = st.text_input('Nome do edital')
            type = st.multiselect(
                'Tipo do edital',
                options=typifications,
                format_func=lambda t: t['name'],
            )
            if st.form_submit_button('Adicionar Edital'):
                order.post_order(name, type)
                st.success('Edital criado com sucesso!')

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

    st.header('📊 Gestão de Editais')
    st.divider()
    if st.button('➕ Adicionar Edital', use_container_width=True):
        create_order()

    orders = order.get_order()

    if not orders:
        st.error('Nenhum edital encontrado.')

    o = st.selectbox(
        'Selecione o edital', options=orders, format_func=lambda x: x['name']
    )

    if o:
        if st.button(
            '➕ Adicionar Versão',
            key=o['id'],
            use_container_width=True,
        ):
            create_release(o)

        if st.button(
            '🗑️ Excluir',
            use_container_width=True,
            key=f'delete_{o["id"]}',
        ):
            order.delete_order(o['id'])

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
                    height=800,
                )
            with col2:
                with st.container(height=800):
                    show_release(r)
