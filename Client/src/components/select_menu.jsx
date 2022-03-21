import React, {Component} from "react";

class SelectMenu extends Component {
    constructor(props){
        super(props);
        this.handle = props.handle;
        this.success = props.success;
        this.fail = props.fail;
    }

    
    processSelection = (payload, type) => {
        switch (type) {
            case "news" : output = (

         
                            );
                            break;
            case 'category' : output = (

         
                                );
                                break;

            default :
        }

        this.success(output, )
    }

    menuClick = (e) => {
        this.handle(null, "/" + e.target.name, "GET", null, this.processSelection, this.fail, e.target.name)  
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