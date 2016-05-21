import React, { PropTypes } from 'react'
import { Spin } from 'antd'
import Style from './style'

export default class LoadingBox extends React.Component {
    
    constructor(props) {
        super(props)
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
    tip: PropTypes.string
}