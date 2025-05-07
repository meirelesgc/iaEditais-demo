from http import HTTPStatus

import httpx
import streamlit as st
from config import Settings


def post_order(name, typification):
    typification = [t['id'] for t in typification]
    data = {'name': name, 'typification': typification}
    response = httpx.post(f'{Settings().API}/doc/', json=data, verify=False)
    if response.status_code == HTTPStatus.CREATED:
        return response.json()


def get_order():
    response = httpx.get(f'{Settings().API}/doc/', verify=False)
    return response.json()


def delete_order(order_id):
    httpx.delete(f'{Settings().API}/doc/{order_id}/', verify=False)
    st.rerun()


def get_detailed_order(order_id):
    response = httpx.get(f'{Settings().API}/doc/{order_id}/', verify=False)
    return response.json()


def get_release(order_id):
    response = httpx.get(
        f'{Settings().API}/doc/{order_id}/release/', verify=False
    )
    return response.json()


def post_release(uploaded_file, order_id):
    files = {'file': (uploaded_file.name, uploaded_file, 'application/pdf')}
    response = httpx.post(
        f'{Settings().API}/doc/{order_id}/release/',
        files=files,
        timeout=2000,
        verify=False,
    )
    if response.status_code == HTTPStatus.UNSUPPORTED_MEDIA_TYPE:
        st.error(
            'Erro: o formato do arquivo não é suportado. Por favor, envie um arquivo PDF válido.'
        )
        return False
    elif response.status_code >= HTTPStatus.BAD_REQUEST:
        st.error(
            f'Erro ao fazer upload do arquivo. Código: {response.status_code}'
        )
        return False
    else:
        st.rerun()
        return True


def delete_release(release_id):
    httpx.delete(f'{Settings().API}/doc/release/{release_id}/', verify=False)
    st.rerun()


def get_release_file(release_id):
    result = httpx.get(
        f'{Settings().API}/doc/release/{release_id}/',
        verify=False,
    )
    return result.content
