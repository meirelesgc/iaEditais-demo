from datetime import datetime

import streamlit as st
from hooks import source
from streamlit_pdf_viewer import pdf_viewer


def format_date(date_str):
    if isinstance(date_str, str):
        dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f')
        return dt.strftime('%d/%m/%Y %H:%M:%S')
    return None


def main():
    @st.dialog('➕ Adicionar Fonte', width='large')
    def create_source():
        name = st.text_input('Nome da fonte')
        description = st.text_area('Descrição da fonte')
        file = st.file_uploader('Escolha um arquivo PDF', type='pdf')

        if st.button('Enviar'):
            if name and description:
                source.post_source(name, description, file)

    @st.dialog('➕ Editar Fonte', width='large')
    def edit_source(s):
        s['name'] = st.text_input('Nome da fonte', value=s['name'])
        s['description'] = st.text_area(
            'Descrição da fonte', value=s['description']
        )
        file = st.file_uploader('Escolha um arquivo PDF', type='pdf')
        if st.button('Enviar'):
            if s['name'] and s['description']:
                if file:
                    s['has_file'] = True
                    source.put_source_file(s, file)
                source.put_source(s)

    source_list = sorted(
        source.get_source(),
        key=lambda s: s['created_at'],
        reverse=True,
    )

    container = st.container()
    st.header('📌 Gestão de Fontes')

    st.divider()
    if st.button('➕ Adicionar', use_container_width=True):
        create_source()

    if not source_list:
        st.error('Nenhuma fonte encontrada.')

    for index, s in enumerate(source_list):
        container = st.container()
        a, b, c = container.columns([4, 1, 1])

        a.subheader(f'{index + 1} - {s["name"]}')

        if b.button(
            '✏️ Editar',
            key=f'edit_{s["id"]}',
            use_container_width=True,
        ):
            edit_source(s)
        if c.button(
            '🗑️ Excluir', key=f'exclude_{s["id"]}', use_container_width=True
        ):
            source.delete_source(s['id'])

        with st.expander('Detalhes'):
            st.subheader(f'Descrição da fonte: {s["description"]}')
            st.subheader(f'Criado em: {format_date(s["created_at"])}')
            st.subheader(
                f'Atualizado em: {format_date(s["updated_at"]) if s["updated_at"] else "N/A"}'
            )
            if s['has_file']:
                pdf_viewer(
                    input=source.get_source_file(s['id']),
                    key=f'pdf_viewer_{s["id"]}',
                    width='100%',
                )
