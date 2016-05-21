import React from 'react'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import { Link } from 'react-router'
import * as actionCreaters from '../../actions/auth'

class Home extends React.Component {
    
    constructor(props) {
        super(props)
    }
    
    componentWillMount() {
        
    }
    
    render() {
        return (
            <div class="container">
                <h2>主页</h2>
                <Link to='/login'>登录</Link><br/>
                <Link to='/admin'>后台管理</Link>
                { this.props.isAuthenticated ? this.props.username : null }
            </div>
        )
    }
}

const mapStateToProps = (state) => ({
    username            : state.auth.username,
    isAuthenticated     : state.auth.isAuthenticated,
    isAuthenticating    : state.auth.isAuthenticating
    
})

const mapDispatchToProps = (dispatch) => ({
    actions: bindActionCreators(actionCreaters, dispatch)
})

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(Home)