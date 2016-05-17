import React from 'react';
import { Route, Redirect } from 'react-router';
import AdminApp from './containers/Admin';
import LoginPage from './containers/LoginPage';

export default (
    <section>
        <Redirect from="/" to="login" />
        <Route path='login' component={LoginPage}></Route>
        <Route path='admin' component={AdminApp}></Route>
    </section>
);