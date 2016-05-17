import React from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import * as actions from '../../actions/auth';

function mapStateToProps(state) {
    return {
        isAuthenticating: state.auth.isAuthenticating,
        statusText: state.auth.statusText
    };
};

function mapDispatchToProps(dispatch) {
    return bindActionCreators(actions, dispatch);
};

class LoginPage extends React.Component {
    
    constructor(props) {
        super(props);
    }
    
    render() {
        return (
            <div className="container">
                <h2>登录</h2>
            </div>
        );
    }
};

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(LoginPage);