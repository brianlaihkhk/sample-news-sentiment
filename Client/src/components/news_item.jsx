import React, {Component} from "react";

class NewsItem extends Component {
    constructor(props){
        super(props);
        this.updateMain = props.updateMain;
        this.defaultError = props.defaultError;
        this.handle = props.handle;
    }

    readNews = (e, category, uuid) => {
        this.handle(null, "/news/" + category + "/" + uuid, "GET", null, this.updateMain, this.defaultError, 'article')  
    }

    render() {
        var news = this.props.news;

        return (
            <div >
                <div className="blog_post">
                    <div className="container_copy">
                    <h3>{news['news_day']}</h3>
                    <h1>{news['news_title']}</h1>
                    <p>{news['news_abstract']}...</p>
                    </div>
                    <a onClick={(e) => this.readNews(e, news['category'], news['uuid'])} href='#'>Read More</a>
                </div>
            </div>
            
        );
    }
};


export default NewsItem;