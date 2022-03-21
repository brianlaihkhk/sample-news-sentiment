import React, {Component} from "react";

class News extends Component {
    constructor(props){
        super(props);
        this.news = props.news['news'];
        this.metadata = props.news['metadata'];        
        this.updateMain = props.updateMain;
    }

    searchTag = (e, tag) => {
        this.updateMain(null, "/search/?tag=" + tag, "GET", null, this.updateMain, this.defaultError, 'search')  
    }
    searchCategory = (e, category) => {
        this.updateMain(null, "/search/?category=" + category, "GET", null, this.updateMain, this.defaultError, 'search')  
    }
    searchSentiment = (e, sentiment) => {
        this.updateMain(null, "/search/?sentiment=" + sentiment, "GET", null, this.updateMain, this.defaultError, 'search')  
    }
    searchTopic = (e, topic) => {
        this.updateMain(null, "/search/?topic=" + topic, "GET", null, this.updateMain, this.defaultError, 'search')  
    }
    render() {
        var sentiment = this.metadata.filter(item => item['key'] == 'sentiment')[0];
        var topic = this.metadata.filter(item => item['key'] == 'topic');
        var tag = this.metadata.filter(item => item['key'] == 'tag');

        var topicItems = [];
        var tagItems = [];

        for (item in tag) {
            tagItems.push(<span><a onClick={(e) => this.searchTag(e, item['value'])}>item['value']</a> ,</span>);
        }
     
        for (item in topic) {
            topicItems.push(<span><a onClick={(e) => this.searchTopic(e, item['value'])}>item['value']</a> ,</span>);
        }   
        return (
            <div class="container mt-5">
                <div class="row">
                    <div class="col-12">
                    <article class="blog-card">
                        <div class="blog-card__info">
                            <h5>{this.news['news_day']}, Category : <a onClick={(e) => this.searchCategory(e, {this.news['category']})}>{this.news['category']}</a>, Sentiment : <a onClick={(e) => this.searchSentiment(e, {sentiment})}>{sentiment}</a></h5>
                            <h2>{this.news['news_title']}</h2>
                            <p>{this.news['news_context']}</p>
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


export default News;