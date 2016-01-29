import React from 'react';
import CSSModules from 'react-css-modules';
import styles from './Layout.css'
import { Menu, Breadcrumb, Icon } from 'antd';
const SubMenu = Menu.SubMenu;

class Layout extends React.Component {
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
    this.updateHeight();
  }

  componentDidMount() {
    window.addEventListener("resize", this.updateHeight);
  }

  componentWillUnmount() {
    window.removeEventListener("resize", this.updateHeight);
  }

  render() {
    return (
      <div className="ant-layout-aside">
        <aside className="ant-layout-sider">
          <div className="ant-layout-logo">
            <span>CUIT ACM Team</span>
          </div>
          <Menu mode="inline" theme="dark"
            defaultSelectedKeys={['1']} defaultOpenKeys={['sub1']}>
            { this.props.children }
          </Menu>
        </aside>
        <div className="ant-layout-main">
          <div className="ant-layout-header">
          </div>
          <div className="ant-layout-breadcrumb">
            <Breadcrumb>
              <Breadcrumb.Item>首页</Breadcrumb.Item>
              <Breadcrumb.Item>应用列表</Breadcrumb.Item>
              <Breadcrumb.Item>某应用</Breadcrumb.Item>
            </Breadcrumb>
          </div>
          <div className="ant-layout-container">
            <div className="ant-layout-content" style={{ height: this.state.contentHeight }}>
              <div>
                内容区域
              </div>
            </div>
          </div>
          <div className="ant-layout-footer">
            Ant Design 版权所有 © 2015 由蚂蚁金服体验技术部支持
          </div>
        </div>
      </div>
    );
  }
}

export default CSSModules(Layout, styles);
