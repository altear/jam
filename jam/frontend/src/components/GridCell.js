import React, { Component } from "react";
import PropTypes from "prop-types";

let colorMap = {
  "-1": 'rgba(220, 250, 220)',
  0: 'rgba(220, 220, 220)',
  1: 'rgba(210, 205, 205)',
  2: 'rgba(210, 200, 200)',
  3: 'rgba(200, 150, 150)',
  4: 'rgba(180, 130, 130)',
  5: 'rgba(160, 110, 110)',
  6: 'rgba(130, 90, 90)',
  7: 'rgba(100, 70, 70)',
  7: 'rgba(50, 50, 50)'
}

class GridCell extends Component {
  static propTypes = {
    index: PropTypes.array, // We use the indices of the table as the key, since elements do not move
    display: PropTypes.number,
    clearArea: PropTypes.func,
    plantFlag: PropTypes.func
  }

  handleClick = (e) => {
    this.props.clearArea(this.props.index) 
  }

  onContextMenu = (e) => {
    e.preventDefault();
    this.props.plantFlag(this.props.index)
  }

  getStyle = () => {
    return { 
      display: "bock",
      width: '30px',
      height: '30px',
      backgroundColor: colorMap[this.props.display],
      textAlign: "center",
      verticalAlign: "middle",
      userSelect: "none"
    }
  };

  getDisplay = () => {
    if (this.props.display >= 0) {
      return this.props.display
    } else if (this.props.display == -1) {
      return ''
    } else if (this.props.display == -2) {
      return "?"
    }
  }
  
  render() {
    return (
      <td style={this.getStyle()} onClick={this.handleClick} onContextMenu={this.onContextMenu}> {this.getDisplay()} </td>
    )
  }
}
export default GridCell;
