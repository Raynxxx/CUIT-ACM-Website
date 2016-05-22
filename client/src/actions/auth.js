import fetch from 'isomorphic-fetch'
import jwtDecode from 'jwt-decode'
import { parseJSON } from '../utils/fetch'
import * as authAPI from '../api/auth'
import * as types from '../constants/auth'


function loginRequest() {
  return {
    type: types.LOGIN_REQUEST,
  }
}

function loginSuccess(data) {
  localStorage.setItem('token', data.token)
  return {
    type: types.LOGIN_SUCCESS,
    token: data.token,
    username: data.username,
  }
}

function loginFailure(error) {
  localStorage.removeItem('token')
  return {
    type: types.LOGIN_FAILURE,
    errorText: error,
  }
}

function checkTokenRequest() {
  return {
    type: types.CHECK_TOKEN_REQUEST,
  }
}

function checkTokenSuccess(data) {
  return {
    type: types.CHECK_TOKEN_SUCCESS,
    username: data.username,
  }
}

function checkTokenFailure(error) {
  localStorage.removeItem('token')
  return {
    type: types.CHECK_TOKEN_FAILURE,
    errorText: error,
  }
}

export function login(username, password, remember) {
  return dispatch => {
    dispatch(loginRequest())
    const options = {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username, password, remember,
      }),
    }
    return fetch(authAPI.login, options).then(parseJSON)
        .then(json => {
          if (json.error) {
            dispatch(loginFailure(json.text))
          } else {
            const decoded = jwtDecode(json.token)
            dispatch(loginSuccess({
              token: json.token,
              username: decoded.username,
            }))
          }
        })
        .catch(error => {
          window.console.log(error)
          dispatch(loginFailure(error))
        })
  }
}

export function checkToken(token) {
  return dispatch => {
    dispatch(checkTokenRequest())
    const options = {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ token }),
    }
    window.console.log('start fetch')
    return fetch(authAPI.checkToken, options).then(parseJSON)
        .then(json => {
          if (json.valid) {
            dispatch(checkTokenSuccess(json.data))
          } else {
            dispatch(checkTokenFailure(json.text))
          }
        })
        .catch(error => {
          window.console.log(error)
          dispatch(checkTokenFailure(error))
        })
  }
}
