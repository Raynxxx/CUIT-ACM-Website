import * as types from '../constants/auth'

const initialState = {
  token: null,
  username: null,
  isAuthenticated: false,
  isAuthenticating: false,
  errorText: null,
}

export default function auth(state = initialState, action) {
  switch (action.type) {
    case types.LOGIN_REQUEST:
      return Object.assign({}, state, {
        isAuthenticating: true,
      })
    case types.LOGIN_SUCCESS:
      return Object.assign({}, state, {
        isAuthenticating: false,
        isAuthenticated: true,
        token: action.token,
        username: action.username,
        statusText: '登录成功',
      })
    case types.LOGIN_FAILURE:
      return Object.assign({}, state, {
        isAuthenticating: false,
        isAuthenticated: false,
        token: null,
        username: null,
        errorText: `登录失败: ${action.errorText}`,
      })
    case types.CHECK_TOKEN_REQUEST:
      return Object.assign({}, state, {
        isAuthenticating: true,
      })
    case types.CHECK_TOKEN_SUCCESS:
      return Object.assign({}, state, {
        isAuthenticating: false,
        isAuthenticated: true,
        username: action.username,
      })
    case types.CHECK_TOKEN_FAILURE:
      return Object.assign({}, state, {
        isAuthenticating: false,
        isAuthenticated: false,
        token: null,
      })
    default:
      return state
  }
}
