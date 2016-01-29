import React from 'react';
import ReactDOM from 'react-dom';
import Layout from './pages/Layout/Layout';
import { Menu, Icon } from 'antd';
const SubMenu = Menu.SubMenu;

ReactDOM.render(
  <Layout>
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
  </Layout>,
  document.getElementById('app')
);
