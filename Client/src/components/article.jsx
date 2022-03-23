import React, {Component} from "react";

class Article extends Component {
    constructor(props){
        super(props);
        this.article = props.article;   
        this.handle = props.handle;
        this.updateMain = props.updateMain;
        this.defaultError = props.defaultError;
    }

    searchTag = (e, tag) => {
        this.handle(null, "/search/?tag=" + tag, "GET", null, this.updateMain, this.defaultError, 'search')  
    }
    searchCategory = (e, category) => {
        this.handle(null, "/search/?category=" + category, "GET", null, this.updateMain, this.defaultError, 'search')  
    }
    searchSentiment = (e, sentiment) => {
        this.handle(null, "/search/?sentiment=" + sentiment, "GET", null, this.updateMain, this.defaultError, 'search')  
    }
    searchTopic = (e, topic) => {
        this.handle(null, "/search/?topic=" + topic, "GET", null, this.updateMain, this.defaultError, 'search')  
    }
    render() {
        const {news, metadata} = this.article;
        var news_item = news[0];

        var sentiment = metadata.filter(item => item['key'] == 'sentiment')[0];
        var topic = metadata.filter(item => item['key'] == 'topic');
        var tag = metadata.filter(item => item['key'] == 'tag');
        var topicItems = [];
        var tagItems = [];
        var sentimentItem = sentiment.length > 0 ? sentiment[0] : 'neu';
        var sentimentItemText = sentimentItem === 'pos' ? 'Positive' : sentimentItem === 'neg' ? 'Negative' : 'Neutral'

        for (var item of tag) {
            tagItems.push(<span><a href='#' onClick={(e) => this.searchTag(e, item['value'])}>{item['value']}</a> , </span>);
        }
     
        for (var item of topic) {
            topicItems.push(<span><a href='#' onClick={(e) => this.searchTopic(e, item['value'])}>{item['value']}</a> , </span>);
        } 
        return (
            <div className="container mt-5">
                <div className="row">
                    <div className="col-12">
                    <article className="blog-card">
                        <div className="blog-card__info">
                            <h5>{news_item['news_day']}, Category : <a href='#' onClick={(e) => this.searchCategory(e, news_item['category'])}>{news_item['category']}</a>, Sentiment : <a href='#' onClick={(e) => this.searchSentiment(e, sentimentItem)}>
                                {sentimentItemText}
                            </a></h5>
                            <h2>{news_item['news_title']}</h2>
                            <p>{news_item['news_context']}</p>
                            <p></p>
                            <p>Tags : {tagItems}</p>
                            <p>Topics : {topicItems}</p>
                        </div>
                    </article>
                    </div>
                </div>
            </div>

            
        );
    }
};


export default Article;