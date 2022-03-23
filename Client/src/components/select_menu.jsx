import React, {Component} from "react";

class SelectMenu extends Component {
    constructor(props){
        super(props);
        this.handle = props.handle;
        this.updateMain = props.updateMain;
        this.defaultError = props.defaultError;
        this.switchWeekDay = props.switchWeekDay;
    }

    menuClick = (e) => {
        this.handle(null, "/" + e.target.name, "GET", null, this.updateMain, this.defaultError, e.target.name)  
    }

    render() {
        return (
            <div>
                <div>Browse news statistics by : 
                    <button name='news' onClick={this.menuClick} >Date</button>
                    <button name='category' onClick={this.menuClick} >Category</button>
                    <button name='sentiment' onClick={this.menuClick} >Sentiment</button>
                    <button name='topic' onClick={this.menuClick} >Topic</button>
                    <button name='tag' onClick={this.menuClick} >Tag</button> 
                </div>
                <div>
                    Display result by weekday :
                    <select name="switch" id="switch" onChange={this.switchWeekDay}>
                        <option value="Default" default>Show all</option>
                        <option value="Sun">Sunday</option>
                        <option value="Mon">Monday</option>
                        <option value="Tue">Tuesday</option>
                        <option value="Wed">Wednesday</option>
                        <option value="Thu">Thursday</option>
                        <option value="Fri">Friday</option>
                        <option value="Sat">Saturday</option>
                    </select>
                </div>
            </div>
        );
    }
};


export default SelectMenu;