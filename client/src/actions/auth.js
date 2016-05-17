import fetch from 'isomorphic-fetch';
import jwtDecode from 'jwt-decode';
import { parseJSON } from '../utils/fetch';
import authAPI from '../api/auth';

export const LOGIN_REQUEST = 'LOGIN_REQUEST';
export const LOGIN_SUCCESS = 'LOGIN_SUCCESS';
export const LOGIN_FAILURE = 'LOGIN_FAILURE';

export function loginRequest() {
    return {
        type: LOGIN_REQUEST
    };
}

export function loginSuccess(data) {
    localStorage.setItem('token', token);
    return {
        type: LOGIN_SUCCESS,
        token: data.token,
        username: data.username
    };
}

export function loginFailure(error) {
    localStorage.removeItem('token');
    return {
        type: LOGIN_FAILURE,
        status: error.status,
        statusText: error.statusText
    };
}

export function login(username, password, redirect) {
    return dispatch => {
        dispatch(loginRequest());
        const options = {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username, password
            })
        };
        return fetch(authAPI.login, options).then(parseJSON)
            .then(json => {
                try {
                    let decoded = jwtDecode(json.token);
                    console.log(decoded);
                    dispatch(loginSuccess({
                        token: json.token,
                        username: decoded.username
                    }));
                } catch (e) {
                    console.log(e);
                }
            })
            .catch(error => {
                dispatch(loginFailure(error));
            });
    }
}