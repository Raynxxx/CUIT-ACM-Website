import { browserHistory } from 'react-router'

export function determineAuth() {
    if (!this.props.isAuthenticated) {
        const token = localStorage.getItem('token')
        if (!token) {
            console.log('determineAuth => redirect login')
            const redirectAfterLogin = this.props.location.pathname
            browserHistory.push(`/login?next=${redirectAfterLogin}`)
        } else {
            console.log('determineAuth => checkToken')
            this.props.actions.checkToken(token)
        }
    }
    console.log('determineAuth => ok')
}