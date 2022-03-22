import React, {Component} from "react";
import NewsItem from "./components/news_item";

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
                    <li name='business' onClick={this.menuClick} >Business</li>
                    <li name='tech' onClick={this.menuClick} >Technology</li>
                    <li name='politics' onClick={this.menuClick} >Politics</li>
                    <li name='entertainment' onClick={this.menuClick} >Entertainment</li>
                    <li name='sport' onClick={this.menuClick} >Sport</li>
                </ul>
            </div>
            
        );
    }
};


export default Category;