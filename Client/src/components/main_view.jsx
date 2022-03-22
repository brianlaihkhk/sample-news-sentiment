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
        this.url = props.url;
    }

    handleView = () => {
        display = []
        switch (this.type) {
            case 'search' : for (item in this.content) {
                                display.push(<NewsItem news={item} handle={this.handle} updateMain={this.updateMain} defaultError={this.defaultError}></NewsItem>);
                            }
                            break;
            case 'category' : display.push(
                                <MainTable type={this.type} content={this.content} handle={this.handle} url={url} updateMain={this.updateMain} defaultError={this.defaultError} /> );
                            break;
            case 'tag' : display.push(
                                <MainTable type={this.type} content={this.content} handle={this.handle} url={url} updateMain={this.updateMain} defaultError={this.defaultError} /> );
                            break;
            case 'topic' : display.push(
                                <MainTable type={this.type} content={this.content} handle={this.handle} url={url} updateMain={this.updateMain} defaultError={this.defaultError} /> );
                            break;
            case 'sentiment' : display.push(
                                <MainTable type={this.type} content={this.content} handle={this.handle} url={url} updateMain={this.updateMain} defaultError={this.defaultError} /> );
                            break;
            case 'news' : display.push(
                                <MainTable type={this.type} content={this.content} handle={this.handle} url={url} updateMain={this.updateMain} defaultError={this.defaultError} /> );
                            break;
            case 'error' : display.push(
                                <span>{this.content}</span>);
                            break;               
            default :  display.push(
                <span>Welcome to News Analysis, please select from the menu.</span>);

        }
        return display;
    } 

    render() {
        return (
            <div>
                {display}
            </div>
            
        );
    }
};


export default MainView;