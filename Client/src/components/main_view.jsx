import React, {Component} from "react";
import MainTable from './main_table';
import NewsItem from './news_item';
import Article from './article';

class MainView extends Component {
    constructor(props){
        super(props);
        this.handle = props.handle;
        this.updateMain = props.updateMain;
        this.defaultError = props.defaultError;
    }

    handleView = () => {
        const {type, url, content} = this.props.state;

        var display = []

        switch (type) {
            case 'search' : for (const item of content) {
                                display.push(<NewsItem news={item} handle={this.handle} updateMain={this.updateMain} defaultError={this.defaultError}></NewsItem>);
                            }
                            break;
            case 'category' : display.push(
                                <MainTable type={type} content={content} handle={this.handle} url={url} updateMain={this.updateMain} defaultError={this.defaultError} /> );
                            break;
            case 'tag' : display.push(
                                <MainTable type={type} content={content} handle={this.handle} url={url} updateMain={this.updateMain} defaultError={this.defaultError} /> );
                            break;
            case 'topic' : display.push(
                                <MainTable type={type} content={content} handle={this.handle} url={url} updateMain={this.updateMain} defaultError={this.defaultError} /> );
                            break;
            case 'sentiment' : display.push(
                                <MainTable type={type} content={content} handle={this.handle} url={url} updateMain={this.updateMain} defaultError={this.defaultError} /> );
                            break;
            case 'news' : display.push(
                                <MainTable type={type} content={content} handle={this.handle} url={url} updateMain={this.updateMain} defaultError={this.defaultError} /> );
                            break;
            case 'article' : display.push(
                                <Article article={content} handle={this.handle} url={url} updateMain={this.updateMain} defaultError={this.defaultError} /> );
                            break;
            case 'error' : display.push(
                                <p name='message'>{content}</p>);
                            break;   
            case 'main' :           
            default :  display.push(
                <p name='message'>Welcome to News Analysis, please select from the menu.</p>);

        }
        return display;
    } 

    render() {
        var display = this.handleView();
        return (
            <>
                {display}
            </>
            
        );
    }
};


export default MainView;