import React from 'react';
import ReactDOM from 'react-dom';
import { Menu, Breadcrumb, Icon } from 'antd';
import styles from './index.css';

const SubMenu = Menu.SubMenu;

ReactDOM.render(
  <div className={styles.antLayoutAside}>
    <aside className={styles.antLayoutSider}>
      <div className={styles.antLayoutLogo}>CUIT ACM Team</div>
      <Menu mode="inline" theme="dark"
        defaultSelectedKeys={['1']} defaultOpenKeys={['sub1']}>
        <SubMenu key="sub1" title={<span><Icon type="user" />导航一</span>}>
          <Menu.Item key="1">选项1</Menu.Item>
          <Menu.Item key="2">选项2</Menu.Item>
          <Menu.Item key="3">选项3</Menu.Item>
          <Menu.Item key="4">选项4</Menu.Item>
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
          <Menu.Item key="11">选项11</Menu.Item>
          <Menu.Item key="12">选项12</Menu.Item>
        </SubMenu>
      </Menu>
    </aside>
    <div className={styles.antLayoutMain}>
      <div className={styles.antLayoutHeader}></div>
      <div className={styles.antLayoutBreadcrumb}>
        <Breadcrumb>
          <Breadcrumb.Item>首页</Breadcrumb.Item>
          <Breadcrumb.Item>应用列表</Breadcrumb.Item>
          <Breadcrumb.Item>某应用</Breadcrumb.Item>
        </Breadcrumb>
      </div>
      <div className={styles.antLayoutContainer}>
        <div className={styles.antLayoutContent}>
          <div style={{ height: 590 }}>
            内容区域
          </div>
        </div>
      </div>
      <div className={styles.antLayoutFooter}>
      Ant Design 版权所有 © 2015 由蚂蚁金服体验技术部支持
      </div>
    </div>
  </div>,
  document.getElementById('app')
);
