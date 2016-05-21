import React from 'react'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import { browserHistory } from 'react-router'
import * as actionCreaters from '../../actions/auth'
import { determineAuth } from '../../utils/auth'
import { Row, Col, Form, Input, Button, Checkbox } from 'antd'
import Style from './style'

const FormItem = Form.Item

class LoginPage extends React.Component {
    
    constructor(props) {
        super(props)
        this.state = {
            redirectRoute: this.props.location.query.next || '/'
        }
        this.handleSubmit = (e) => {
            e.preventDefault()
            const values = this.props.form.getFieldsValue()
            this.props.actions.login(values.username, values.password, values.remember)
        }
    }
    
    componentWillReceiveProps(nextProps) {
        if (nextProps.isAuthenticated) {
            setTimeout(() => {
                browserHistory.push(this.state.redirectRoute)
            }, 1000)
        }
    }
    
    render() {
        const { getFieldProps } = this.props.form
        const formItemLayout = {
            labelCol: { span: 6 },
            wrapperCol: { span: 15, offset: 1 },
        }
        return (
            <div className="container login-page">
            <Row type='flex' justify="center" align="middle">
            <Col span={24}>
                <div className="login-header">
                    <h2>CUIT ACM Team</h2>
                </div>
                <div className="login-box">
                    <Form horizontal onSubmit={this.handleSubmit}>
                        <FormItem {...formItemLayout} label="用户名">
                            <Input type="text" {...getFieldProps('username')} placeholder="请输入用户名" />
                        </FormItem>
                        <FormItem {...formItemLayout} label="密码">
                            <Input type="password" {...getFieldProps('password')} 
                                placeholder="请输入密码" />
                        </FormItem>
                        <FormItem {...formItemLayout} label="记住我">
                            <Checkbox {...getFieldProps('remember')}>是的</Checkbox>
                        </FormItem>
                        <FormItem wrapperCol={{ span: 6, offset: 7 }} style={{ marginTop: 24 }}>
                            <Button type="primary" htmlType="submit"
                                    loading={this.props.isAuthenticating}>
                                确定
                            </Button>
                        </FormItem>
                    </Form>
                </div>
            </Col>
            </Row>
            </div>
        )
    }
}


const mapStateToProps = (state) => ({
    isAuthenticated: state.auth.isAuthenticated,
    isAuthenticating: state.auth.isAuthenticating,
    errorText: state.auth.errorText
})

const mapDispatchToProps = (dispatch) => ({
    actions: bindActionCreators(actionCreaters, dispatch)
})

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(Form.create()(LoginPage))