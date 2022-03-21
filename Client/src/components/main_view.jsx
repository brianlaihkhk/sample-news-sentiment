import React, {Component} from "react";
import MainTable from './main_table';
import NewsItem from './news_item';


class MainView extends Component {
    constructor(props){
        super(props);
        this.type = props.type;
        this.content = props.content;
        this.handle = props.handle;
        this.updateMain = props.updateMain;
        this.defaultError = props.defaultError;
    }

    handleView = () => {
        display = []
        switch (this.type) {
            case 'search' : for (item in this.content) {
                                display.push(<NewsItem news={item} handle={this.handle} updateMain={this.updateMain} defaultError={this.defaultError}></NewsItem>);
                            }
                            break;
            case 'category' : display.push(
                                <MainTable type={this.type} content={this.content} handle={this.handle} updateMain={this.updateMain} defaultError={this.defaultError} /> );
                            break;
            case 'tag' : display.push(
                                <MainTable type={this.type} content={this.content} handle={this.handle} updateMain={this.updateMain} defaultError={this.defaultError} /> );
                            break;
            case 'topic' : display.push(
                                <MainTable type={this.type} content={this.content} handle={this.handle} updateMain={this.updateMain} defaultError={this.defaultError} /> );
                            break;
            case 'sentiment' : display.push(
                                <MainTable type={this.type} content={this.content} handle={this.handle} updateMain={this.updateMain} defaultError={this.defaultError} /> );
                            break;
            case 'news' : display.push(
                                <MainTable type={this.type} content={this.content} handle={this.handle} updateMain={this.updateMain} defaultError={this.defaultError} /> );
                            break;
        }
        return display;
    } 

    drill = (e, category, uuid) => {
        this.handle(null, "/news/" + category + "/" + uuid, "GET", null, this.updateMain, this.defaultError, 'read_news')  
    }

    render() {
        return (
            <div>
                {this.handleView}
            </div>
            
        );
    }
};


export default MainView;