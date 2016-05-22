import { browserHistory } from 'react-router'

export function determineAuth() {
  if (!this.props.isAuthenticated) {
    const token = localStorage.getItem('token')
    if (!token) {
      window.console.log('determineAuth => redirect login')
      const redirectAfterLogin = this.props.location.pathname
      browserHistory.push(`/login?next=${redirectAfterLogin}`)
    } else {
      window.console.log('determineAuth => checkToken')
      this.props.actions.checkToken(token)
    }
  }
  window.console.log('determineAuth => ok')
}
