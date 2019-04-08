import React, { Component } from "react";
import MinesweeperMenuItem from "./MinesweeperMenuItem"
import PropTypes from "prop-types";

class MinesweeperMenu extends Component {
    menuStyle = {
        width: '100%',
        height: '100%',
        display: 'flex',
        flexDirection: 'row',
        justifyContent: 'center',
        justifySelf: 'flex-start',
        alignItems: 'center',
        flexWrap: 'wrap',
        backgroundColor: 'rgba(0,0,0,0.2)'
    }

    menuContainerStyle = {
        width: '100%',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center'
    }
    
    menuTitleStyle = {
        paddingTop: "30px",
        fontSize: '1.5em'
    }

    static propTypes = {
        api: PropTypes.string,
        updateUri: PropTypes.func
    }

    render () {
        return (
            <div style={this.menuContainerStyle}>
                <p style={this.menuTitleStyle}> New Game? </p>
                <div style={this.menuStyle}>
                    <MinesweeperMenuItem text="Small" api={this.props.api} action="create-small-game" updateUri={this.props.updateUri}/>
                    <MinesweeperMenuItem text="Medium" api={this.props.api} action="create-medium-game" updateUri={this.props.updateUri}/> 
                    <MinesweeperMenuItem text="Large" api={this.props.api} action="create-large-game" updateUri={this.props.updateUri}/> 
                </div>
            </div>
        )
    }
}

export default MinesweeperMenu;