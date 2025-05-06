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


def reset_to_home():
    st.session_state.pop('page_loaded', None)
    st.rerun()


pages_1 = {
    'Base de conhecimento': [
        st.Page(source.main, title='Fontes', url_path='source'),
        st.Page(
            typification.main, title='Tipificação', url_path='typification'
        ),
        st.Page(taxonomy.main, title='Taxonomia', url_path='taxonomy'),
        st.Page(branch.main, title='Ramos', url_path='branch'),
    ],
    'Voltar ao início': [
        st.Page(reset_to_home, title='🔙 Voltar ao início', url_path='reset')
    ],
}

pages_2 = {
    'Verificação de editais': [
        st.Page(publication.main, title='Incluir', url_path='order'),
        st.Page(
            analysis.main, title='Análise através de IA', url_path='analysis'
        ),
    ],
    'Voltar ao início': [
        st.Page(reset_to_home, title='🔙 Voltar ao início', url_path='reset')
    ],
}


def home():
    _, center, _ = st.columns([1, 2, 1])
    center.markdown(
        "<h1 style='text-align: center;'>🚀 Plataforma de Avaliação de Editais</h1>",
        unsafe_allow_html=True,
    )
    center.caption('🔖 Versão 1.3.0')

    center.markdown(
        """
        <div style='text-align: justify; font-size: 1.1em;'>
        👋 <strong>Bem-vindo ao iaEditais!</strong><br><br>
        Esta é uma prova de conceito inovadora que utiliza Inteligência Artificial para auxiliar na <strong>elaboração</strong> e <strong>verificação automática</strong> de editais de contratação pública.
        Nosso objetivo é oferecer mais <strong>precisão</strong>, <strong>padronização</strong> e <strong>eficiência</strong> ao processo de construção e revisão de documentos oficiais.
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown(
        "<h2 style='text-align: center;'>🧭 Escolha uma funcionalidade para começar</h2>",
        unsafe_allow_html=True,
    )
    st.markdown('<br>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('### 📚 Base de Conhecimento')
        st.markdown("""
            Acesse uma coleção estruturada de normas, critérios e boas práticas usadas na avaliação de editais.  
            Utilize a árvore de conhecimento 🌳 do iaEditais para navegar pelos tópicos de forma lógica e orientada.
        """)
        if st.button('🔍 Explorar Base', use_container_width=True):
            st.session_state['page_loaded'] = 'knowledge'
            st.rerun()
            st.switch_page('source')

    with col2:
        st.markdown('### 🤖 Verificação Automatizada')
        st.markdown("""
            Faça upload de um edital e receba uma análise inteligente, com identificação de potenciais inconsistências, lacunas e oportunidades de melhoria.  
            Aproveite o poder da IA para revisões mais seguras e rápidas. ⚡
        """)
        if st.button('✅ Iniciar Verificação', use_container_width=True):
            st.session_state['page_loaded'] = 'verification'
            st.rerun()
            st.switch_page('order')

    st.divider()
    st.markdown(
        "<p style='text-align: center; color: gray;'>Desenvolvido com ❤️ por iaEditais - Transformando o futuro das compras públicas</p>",
        unsafe_allow_html=True,
    )


if 'page_loaded' not in st.session_state:
    home_page = [st.Page(home, title='Principal', url_path='home')]
    st.navigation(home_page, expanded=False).run()
elif st.session_state['page_loaded'] == 'knowledge':
    st.navigation(pages_1).run()
elif st.session_state['page_loaded'] == 'verification':
    st.navigation(pages_2).run()
