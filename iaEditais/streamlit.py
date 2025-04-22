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
    st.title('Bem-vindo ao iaEditais! ✨')

    st.subheader(
        '🔍 Uma Plataforma Inteligente para Avaliação de Editais Públicos'
    )

    st.info(
        """
        O **iaEditais** utiliza o poder da Inteligência Artificial para transformar a maneira como órgãos públicos e empresas interagem com editais de contratação. 
        Nossa plataforma foi cuidadosamente desenvolvida para oferecer:
        - **Precisão Aprimorada:** Identificação automática de erros e inconsistências.
        - **Conformidade Garantida:** Alinhamento com as legislações e regulamentos vigentes.
        - **Eficiência Operacional:** Redução do tempo gasto na elaboração e revisão de documentos.
        - **Transparência Reforçada:** Processos licitatórios mais claros e acessíveis.
        """
    )

    st.title('Por que usar o iaEditais?')

    st.markdown(
        """
        A complexidade do cenário regulatório brasileiro exige ferramentas inteligentes para otimizar a gestão de editais. 
        Com o **iaEditais**, você não apenas simplifica o processo, mas também eleva o nível de qualidade e segurança de suas licitações.
        """
    )
    st.empty()
    if st.button(
        '📚 Explore a Base de Conhecimento', use_container_width=True
    ):
        st.session_state['page_loaded'] = 'knowledge'
        st.rerun()
        st.switch_page('source')
    st.divider()
    if st.button(
        '🧠 Inicie a Verificação de Editais', use_container_width=True
    ):
        st.session_state['page_loaded'] = 'verification'
        st.rerun()
        st.switch_page('order')

    st.divider()
    st.markdown(
        '💡 Caso tenha dúvidas ou precise de suporte, entre em contato com nossa equipe através do canal oficial de atendimento.'
    )
    st.markdown(
        '🤝 Aproveite os recursos do iaEditais para transformar a gestão de editais e elevar os padrões de eficiência e conformidade na administração pública.'
    )


if 'page_loaded' not in st.session_state:
    st.navigation(
        [st.Page(home, title='Principal', url_path='home')], expanded=False
    ).run()


elif st.session_state['page_loaded'] == 'knowledge':
    st.navigation(pages_1).run()
elif st.session_state['page_loaded'] == 'verification':
    st.navigation(pages_2).run()
