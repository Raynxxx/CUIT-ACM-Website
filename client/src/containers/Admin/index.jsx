import React, { PropTypes } from 'react'
import { Menu, Breadcrumb, Icon } from 'antd'
import Style from './style'

const SubMenu = Menu.SubMenu

class Admin extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            contentHeight: window.innerHeight
        }
        this.updateHeight = () => {
            this.setState({ contentHeight: window.innerHeight })
        }
    }

    componentWillMount() {
        window.addEventListener("resize", this.updateHeight)
    }

    componentWillUnmount() {
        window.removeEventListener("resize", this.updateHeight)
    }

    render() {
        const { title } = this.props
        return (
            <div className="container-admin" style={{ minHeight: this.state.contentHeight }}>
                <aside className="sider">
                    <div className="logo">CUIT ACM Team</div>
                    <Menu mode="inline" theme="dark" defaultSelectedKeys={['1']} defaultOpenKeys={['sub1']}>
                        <SubMenu key="sub1" title={<span><Icon type="user" />用户管理</span>}>
                            <Menu.Item key="1">选项1</Menu.Item>
                            <Menu.Item key="2">选项2</Menu.Item>
                        </SubMenu>
                        <SubMenu key="sub2" title={<span><Icon type="user" />用户管理</span>}>
                            <Menu.Item key="1">选项1</Menu.Item>
                            <Menu.Item key="2">选项2</Menu.Item>
                        </SubMenu>
                        <SubMenu key="sub3" title={<span><Icon type="user" />用户管理</span>}>
                            <Menu.Item key="1">选项1</Menu.Item>
                            <Menu.Item key="2">选项2</Menu.Item>
                        </SubMenu>
                    </Menu>
                </aside>
                <div className="main">
                    <div className="header"></div>
                    <div className="breadcrumb">
                        <Breadcrumb>
                            <Breadcrumb.Item>首页</Breadcrumb.Item>
                            <Breadcrumb.Item>应用列表</Breadcrumb.Item>
                            <Breadcrumb.Item>某应用</Breadcrumb.Item>
                        </Breadcrumb>
                    </div>
                    <div className="wrapper">
                        <div className="content" >
                            <div style={{ minHeight: this.state.contentHeight - 233 }}>
                                { this.props.children }
                            </div>
                        </div>
                    </div>
                    <div className="footer">
                        Copyright © 2016 Raynxxx
                    </div>
                </div>
            </div>
        )
    }
}

export default Admin