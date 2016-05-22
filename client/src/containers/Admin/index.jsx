import React, { PropTypes } from 'react'
import { Menu, Breadcrumb, Icon } from 'antd'
import Header from '../../components/Header'
import cx from 'classnames'
import './style.less'

class Admin extends React.Component {

  constructor(props) {
    super(props)
    this.state = {
      contentHeight: window.innerHeight,
      collapse: false,
    }
    this.updateHeight = () => {
      this.setState({ contentHeight: window.innerHeight })
    }
    this.onCollapseChange = () => {
      this.setState({ collapse: !this.state.collapse })
    }
  }

  componentWillMount() {
    window.addEventListener('resize', this.updateHeight)
  }

  componentWillUnmount() {
    window.removeEventListener('resize', this.updateHeight)
  }

  render() {
    const { collapse, contentHeight } = this.state
    const containerClass = cx({
      'container-admin': true,
      collapse,
    })
    return (
      <div className={containerClass} style={{ minHeight: contentHeight }}>
        <aside className="sider">
          <div className="logo">
            {collapse ? 'ACM' : 'CUIT ACM Team'}
          </div>
          <Menu mode="inline" theme="dark" defaultSelectedKeys={['user']}>
            <Menu.Item key="user">
              <Icon type="user" /><span className="nav-text">导航一</span>
            </Menu.Item>
            <Menu.Item key="setting">
              <Icon type="setting" /><span className="nav-text">导航二</span>
            </Menu.Item>
            <Menu.Item key="laptop">
              <Icon type="laptop" /><span className="nav-text">导航三</span>
            </Menu.Item>
            <Menu.Item key="notification">
              <Icon type="notification" /><span className="nav-text">导航四</span>
            </Menu.Item>
            <Menu.Item key="folder">
              <Icon type="folder" /><span className="nav-text">导航五</span>
            </Menu.Item>
          </Menu>
          <div className="aside-action" onClick={this.onCollapseChange}>
            {collapse ? <Icon type="right" /> : <Icon type="left" />}
          </div>
        </aside>
        <div className="main">
          <Header {...this.props} />
          <div className="breadcrumb">
            <Breadcrumb>
              <Breadcrumb.Item>首页</Breadcrumb.Item>
              <Breadcrumb.Item>应用列表</Breadcrumb.Item>
              <Breadcrumb.Item>某应用</Breadcrumb.Item>
            </Breadcrumb>
          </div>
          <div className="wrapper">
            <div className="content" >
              <div style={{ minHeight: contentHeight - 235 }}>
                {this.props.children}
              </div>
            </div>
          </div>
          <div className="footer">
            Copyright © 2016 CUIT ACM Team
          </div>
        </div>
      </div>
    )
  }
}

Admin.propTypes = {
  children: PropTypes.element,
}

export default Admin
