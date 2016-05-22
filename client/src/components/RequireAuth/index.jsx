import React from 'react'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import * as actionCreaters from '../../actions/auth'
import { determineAuth } from '../../utils/auth'
import LoadingBox from '../LoadingBox'


export default function requireAuth(Component) {
  class AuthWrapper extends React.Component {

    constructor(props) {
      super(props)
      this.state = {
        canLoad: false,
      }
    }

    componentWillMount() {
      determineAuth.call(this)
    }

    componentWillReceiveProps(nextProps) {
      if (!nextProps.isAuthenticated && !nextProps.isAuthenticating) {
        determineAuth.call(this)
      }
      if (nextProps.isAuthenticated && !nextProps.isAuthenticating) {
        setTimeout(() => {
          this.setState({ canLoad: true })
        }, 1200)
      }
    }

    render() {
      return (
        this.state.canLoad
          ? <Component {...this.props} />
          : <LoadingBox />
      )
    }
  }

  const mapStateToProps = (state) => ({
    username: state.auth.username,
    isAuthenticated: state.auth.isAuthenticated,
    isAuthenticating: state.auth.isAuthenticating,
  })

  const mapDispatchToProps = (dispatch) => ({
    actions: bindActionCreators(actionCreaters, dispatch),
  })

  return connect(mapStateToProps, mapDispatchToProps)(AuthWrapper)
}
