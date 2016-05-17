import React from 'react';
import Style from './style.less';
import { Menu, Breadcrumb, Icon } from 'antd';
const SubMenu = Menu.SubMenu;

export default class AdminPage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            contentHeight: window.innerHeight
        };
        this.updateHeight = this.updateHeight.bind(this);
    }
    
    updateHeight() {
        this.setState({ contentHeight: window.innerHeight });
    }
    
    componentWillMount() {
        window.addEventListener("resize", this.updateHeight);
    }
    
    componentWillUnmount() {
        window.removeEventListener("resize", this.updateHeight);
    }
    
    render() {
        const { title } = this.props;
        return (
        <div className="container-admin" style={{ minHeight: this.state.contentHeight }}>
            <aside className="sider">
                <div className="logo">{ title }</div>
                <Menu mode="inline" theme="dark" defaultSelectedKeys={['1']} defaultOpenKeys={['sub1']}>
                    <SubMenu key="sub1" title={<span><Icon type="user" />导航一</span>}>
                        <Menu.Item key="1">选项1</Menu.Item>
                        <Menu.Item key="2">选项2</Menu.Item>
                    </SubMenu>
                    <SubMenu key="sub2" title={<span><Icon type="laptop" />导航二</span>}>
                        <Menu.Item key="5">选项5</Menu.Item>
                        <Menu.Item key="6">选项6</Menu.Item>
                        <Menu.Item key="7">选项7</Menu.Item>
                        <Menu.Item key="8">选项8</Menu.Item>
                    </SubMenu>
                    <SubMenu key="sub3" title={<span><Icon type="notification" />导航三</span>}>
                        <Menu.Item key="9">选项9</Menu.Item>
                        <Menu.Item key="10">选项10</Menu.Item>
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
                <div className="container">
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
        );
    }
};