import React, { Component } from "react";
import PropTypes from "prop-types";

class MinesweeperMenuItem extends Component {
    menuItemStyle = {
        width: '100%',
        minWidth: '100px',
        maxWidth: '180px',
        margin: '5px',
        backgroundColor: 'rgba(0,0,0,0.8)',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        userSelect: "none",
        MozUserSelect:"none",
        WebkitUserSelect:"none",
        msUserSelect:"none",
    }

    menuItemTextStyle = {
        fontSize: '1em',
        color: 'rgba(255,255,255,0.8)',
        userSelect: "none",
        MozUserSelect:"none",
        WebkitUserSelect:"none",
        msUserSelect:"none"
    }

    static propTypes = {
        api: PropTypes.string,
        action: PropTypes.string,
        updateUri: PropTypes.func
    }

    createNewGame = () => {
        fetch(this.props.api + this.props.action)
            .then((response) => response.json())
            .then((data) => this.props.updateUri(data.uuid)) // the games/ path is part of the frontend and not the api
    }

    render () {
        return (
            <a style={this.menuItemStyle} onClick={this.createNewGame}> 
                <p style={this.menuItemTextStyle}> 
                    {this.props.text} 
                </p> 
            </a>
        )
    }
}

export default MinesweeperMenuItem;