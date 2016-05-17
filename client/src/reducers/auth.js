import jwtDecode from 'jwt-decode';
import * as types from '../actions/auth';

const initialState = {
    token: null,
    username: null,
    isAuthenticated: false,
    isAuthenticating: false,
    statusText: null,
}

export default function auth(state = initialState, action) {
    switch (action.type) {
        case types.LOGIN_REQUEST:
            return Object.assign({}, state, {
                isAuthenticating: true
            });
        case types.LOGIN_SUCCESS:
            return Object.assign({}, state, {
                isAuthenticating: false,
                isAuthenticated: true,
                token: action.token,
                username: action.username,
                statusText: '登录成功'
            });
        case types.LOGIN_FAILURE:
            return Object.assign({}, state, {
                isAuthenticating: false,
                isAuthenticated: false,
                token: null,
                username: null,
                statusText: `登录失败: ${action.statusText}`
            });
        default:
            return state;
    }
}