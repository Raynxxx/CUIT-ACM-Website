import React, { PropTypes } from 'react'
import { Spin } from 'antd'
import './style.less'

export default class LoadingBox extends React.Component {

  constructor(props) {
    super(props)
    this.state = {}
  }

  render() {
    return (
      <div className="loading-box">
        <Spin tip={this.props.tip} size="large" />
      </div>
    )
  }
}

LoadingBox.propTypes = {
  tip: PropTypes.string,
}
