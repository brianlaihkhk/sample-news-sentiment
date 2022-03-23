import React, {Component} from "react";


class MainTable extends Component {
    constructor(props){
        super(props);
        this.handle = props.handle;
        this.updateMain = props.updateMain;
        this.defaultError = props.defaultError;
    }

 
    dataClick = (e, type, year, month, day, weekDay, spec) => {
        var date_query = (weekDay ? weekDay : "" ) + "-" + (year ? year : "" ) + "-" + (month ? month : "" ) + "-" + (day ? day : "" )

        if (spec){
            this.handle(null, "/" + type + "/" + date_query + "/" + spec, "GET", null, this.updateMain, this.defaultError, type);
        } else {
            this.handle(null, "/" + type + "/" + date_query, "GET", null, this.updateMain, this.defaultError, type);
        }
    }

    searchClick = (e, type, year, month, day, weekDay, spec) => {
        var query = (weekDay != null ? weekDay : "" ) + "-" + (year != null ? year : "" ) + "-" + (month != null ? month : "" ) + "-" + (day != null ? day : "" );

        if (spec) {
            this.handle(null, "/search?" + type + "=" + spec + '&date=' + query, "GET", null, this.updateMain, this.defaultError, 'search')
        } else {
            this.handle(null, "/search?" + 'date=' + query, "GET", null, this.updateMain, this.defaultError, 'search') 
        }
    }

    getTableHeader = (content) => {
        var output = []
        if (content.length > 0){
            for (var key of Object.keys(this.props.content[0])){
                output.push(<th className="main_table">{key}</th>);
            }
        }
        return output;
    }

    convertDayString = (dateString) => {
        var spec = dateString.split('-');
        return {'year' : spec[1], 'month' : spec[2], 'day' : spec[3] , 'week_day' : spec[0]}
    }

    getTableBody = (content, type, url, selectWeekDay) => {

        var output = [];
        var urlSplit = url.substring(0, url.indexOf('?')).split('/');
        var dayString = urlSplit.length === 3 ? urlSplit[2] : null;
        var dateSpec = dayString ? this.convertDayString(dayString) : {};

        content.forEach((row) => {
            var outputRow = []

            Object.entries(row).forEach((item) => {
                var key = item[0];
                var value = item[1];

                if (type === 'news' && key === 'year'){
                    outputRow.push(<td className="main_table"><span><a href='#' onClick={(e) => this.dataClick(e, 'category', row['year'], null, null, selectWeekDay, null)}>{value}</a></span></td>);
                } else if (type === 'news'){
                    outputRow.push(<td className="main_table"><span><a href='#' onClick={(e) => this.searchClick(e, 'date', row['year'], null, null, selectWeekDay, null)}>{value}</a></span></td>);
                } else if (key === 'year'){
                    outputRow.push(<td className="main_table"><span><a href='#' onClick={(e) => this.dataClick(e, type, row['year'], null, null, selectWeekDay, null )}>{value}</a></span></td>);
                } else if (key === 'month'){
                    outputRow.push(<td className="main_table"><span><a href='#' onClick={(e) => this.dataClick(e, type, row['year'], row['month'], null, selectWeekDay, null )}>{value}</a></span></td>);
                } else if (key === 'day'){
                    outputRow.push(<td className="main_table"><span><a href='#' onClick={(e) => this.dataClick(e, type, row['year'], row['month'], row['day'], selectWeekDay, null )}>{value}</a></span></td>);
                } else if (key === 'week_day'){
                    outputRow.push(<td className="main_table"><span><a href='#' onClick={(e) => this.dataClick(e, type, row['year'], row['month'], row['day'], selectWeekDay, null )}>{value}</a></span></td>);
                } else if (key === 'category' || key === 'topic' || key === 'tag' || key === 'sentiment' ){
                    outputRow.push(<td className="main_table"><span><a href='#' onClick={(e) => this.dataClick(e, type, row['year'], row['month'], row['day'], selectWeekDay, value )}>{value}</a></span></td>);
                } else if (key === 'news_count' ){
                    outputRow.push(<td className="main_table"><span><a href='#' onClick={(e) => this.searchClick(e, type, row['year'], row['month'], row['day'], selectWeekDay, row[type])}>{value}</a></span></td>);
                } else{
                    outputRow.push(<td className="main_table"><span>{value}</span></td>);
                }


            });
            output.push(<tr>{outputRow}</tr>);
        });
        return output;
        
    };

    render() {
        const {content, type, url, selectWeekDay} = this.props; 

        var header = this.getTableHeader(content);
        var body = this.getTableBody(content, type, url, selectWeekDay);
        return (
            <div className="wrapper">
                <table className="main_table">
                    <thead>
                        <tr className="main_table">
                            {header}
                        </tr>
                    </thead>
                    <tbody className="main_table">
                        {body}
                    </tbody>
                </table>
            </div>
            
        );
    }
};


export default MainTable;