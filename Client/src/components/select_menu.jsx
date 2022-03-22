import React, {Component} from "react";

class SelectMenu extends Component {
    constructor(props){
        super(props);
        this.handle = props.handle;
        this.updateMain = props.updateMain;
        this.defaultError = props.defaultError;
    }

    menuClick = (e) => {
        this.handle(null, "/" + e.target.name, "GET", null, this.updateMain, this.defaultError, e.target.name)  
    }

    render() {
        return (
            <div>Browse news statistics by : 
                <button name='news' onClick={this.menuClick} >Date</button>
                <button name='category' onClick={this.menuClick} >Category</button>
                <button name='sentiment' onClick={this.menuClick} >Sentiment</button>
                <button name='topic' onClick={this.menuClick} >Topic</button>
                <button name='tag' onClick={this.menuClick} >Tag</button>
            </div>
            
        );
    }
};


export default SelectMenu;