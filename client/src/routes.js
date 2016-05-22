import React from 'react'
import { Route } from 'react-router'
import requireAuth from './components/RequireAuth'
import HomePage from './containers/Home'
import AdminPage from './containers/Admin'
import LoginPage from './containers/Login'

export default (
  <section>
    <Route path="/" component={HomePage} />
    <Route path="/login" component={LoginPage} />
    <Route path="/admin" component={requireAuth(AdminPage)} />
  </section>
)
