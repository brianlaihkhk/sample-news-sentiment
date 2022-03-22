import React, {Component} from "react";

class Category extends Component {
    constructor(props){
        super(props);
        this.handle = props.handle;
        this.updateMain = props.updateMain;
        this.defaultError = props.defaultError;
    }
    
    categoryClick = (e) => {
        this.handle(null, "/search?category=" + e.target.name, "GET", null, this.updateMain, this.defaultError, 'search')  
    }

    render() {
        return (
            <div>Browse news by category : 
                <ul>
                    <li><a href='#' name='business' onClick={this.categoryClick} >Business</a></li>
                    <li><a href='#' name='tech' onClick={this.categoryClick} >Technology</a></li>
                    <li><a href='#' name='politics' onClick={this.categoryClick} >Politics</a></li>
                    <li><a href='#' name='entertainment' onClick={this.categoryClick} >Entertainment</a></li>
                    <li><a href='#' name='sport' onClick={this.categoryClick} >Sport</a></li>
                </ul>
            </div>
            
        );
    }
};


export default Category;