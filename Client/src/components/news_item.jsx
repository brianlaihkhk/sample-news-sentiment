import React, {Component} from "react";

class NewsItem extends Component {
    constructor(props){
        super(props);
        this.news = props.news;
        this.updateMain = props.updateMain;
        this.defaultError = props.defaultError;
        this.handle = props.handle;
    }

    readNews = (e, category, uuid) => {
        this.handle(null, "/news/" + category + "/" + uuid, "GET", null, this.updateMain, this.defaultError, 'read_news')  
    }

    render() {
        return (
            <div class="wrapper">
                <div class="blog_post">
                    <div class="container_copy">
                    <h3>{this.news['news_day']}</h3>
                    <h1>{this.news['news_title']}</h1>
                    <p>{this.news['news_abstract']}...</p>
                    </div>
                    <a class="btn_primary" onClick={(e) => this.readNews(e, this.news['category'], this.news['uuid'])} href='#'>Read More</a>
                </div>
            </div>
            
        );
    }
};


export default NewsItem;