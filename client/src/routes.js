import React from 'react'
import { Route, Redirect } from 'react-router'
import RequireAuth from './components/RequireAuth'
import HomePage from './containers/Home'
import AdminPage from './containers/Admin'
import LoginPage from './containers/Login'

export default (
    <section>
        <Route path='/' component={HomePage}></Route>
        <Route path='/login' component={LoginPage}></Route>
        <Route path='/admin' component={RequireAuth(AdminPage)}></Route>
    </section>
);