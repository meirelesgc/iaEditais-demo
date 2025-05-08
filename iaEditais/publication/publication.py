from datetime import datetime

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
    oldest_typification = min(typifications, key=lambda t: t['created_at'])

    with st.form(key='create_order_form'):
        name = st.text_input('Nome do edital')
        _type = st.multiselect(
            'Tipo do edital',
            options=typifications,
            default=[oldest_typification],
            format_func=lambda t: t['name'],
        )
        uploaded_file = st.file_uploader('Escolha um arquivo PDF', type='pdf')
        if st.form_submit_button('Adicionar Edital'):
            if not _type:
                st.warning('Selecione pelo menos um tipo de edital.')
            elif not uploaded_file:
                st.warning('É necessário anexar a primeira versão do edital.')
            else:
                ord = order.post_order(name, _type)
                st.success('Edital criado com sucesso!')
                with st.status(
                    'Analisando versão...', expanded=True
                ) as status:
                    success = order.post_release(uploaded_file, ord['id'])
                    if success:
                        status.update(
                            label='Analise concluida!', state='complete'
                        )
                    else:
                        status.update(
                            label='Tivemos um problema!', state='error'
                        )
                        order.delete_order(ord['id'])


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
    typifications = taxonomy.get_typifications()

    if not orders:
        st.error('Nenhum edital encontrado.')
        return

    for index, o in enumerate(orders):
        container = st.container()
        a, b = container.columns([6, 1])
        a.subheader(f'{index + 1} - {o["name"]}')

        b_key = f'exclude_{o["id"]}'
        if b.button('🗑️ Excluir', key=b_key, use_container_width=True):
            order.delete_order(o['id'])
            st.rerun()

        with st.expander('Detalhes'):
            ty = ', '.join([
                t.get('name')
                for t in typifications
                if t.get('id') in o.get('typification')
            ])
            st.subheader(f'Tipificações: {ty}')
            st.subheader(f'Criado em: {format_date(o["created_at"])}')
            st.subheader(
                f'Atualizado em: {format_date(o["updated_at"]) if o["updated_at"] else "N/A"}'
            )
