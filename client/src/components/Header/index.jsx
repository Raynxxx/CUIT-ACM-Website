import React, { PropsTypes } from 'react'

export default class Header extends React.Component {

  constructor(props) {
    super(props)
    this.state = {}
  }

  render() {
    return (
      <div className="header">
        {this.props.username}
      </div>
    )
  }
}

Header.propTypes = {
  username: PropsTypes.string,
}
