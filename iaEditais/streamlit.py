import streamlit as st
from methodology import branch, taxonomy, typification
from publication import analysis, publication
from source import source

st.set_page_config(
    page_title='Ia Editais',
    page_icon='📄',
    layout='wide',
    initial_sidebar_state='expanded',
)

st.logo('storage/logo.png', size='large')

pages = {
    'Base de conhecimento': [
        st.Page(source.main, title='Fontes', url_path='source', default=True),
        st.Page(
            typification.main, title='Tipificação', url_path='typification'
        ),
        st.Page(taxonomy.main, title='Taxonomia', url_path='taxonomy'),
        st.Page(branch.main, title='Ramos', url_path='branch'),
    ],
    'Verificação de editais': [
        st.Page(publication.main, title='Incluir', url_path='order'),
        st.Page(
            analysis.main,
            title='Análise através de IA',
            url_path='analysis',
        ),
    ],
}

st.navigation(pages).run()
