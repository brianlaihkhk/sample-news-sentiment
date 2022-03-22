import React, {Component} from "react";


class MainTable extends Component {
    constructor(props){
        super(props);
        this.type = props.type;
        this.content = props.content;
        this.handle = props.handle;
        this.updateMain = props.updateMain;
        this.defaultError = props.defaultError;
        this.url = props.url;
    }


    dataClick = (e, type, year, month, day, weekDay, spec) => {
        date_query = (weekDay ? weekDay : "" ) + "-" + (year ? year : "" ) + "-" + (month ? month : "" ) + "-" + (day ? day : "" )

        if (spec){
            this.handle(null, "/" + type + "/" + date_query + "/" + spec, "GET", null, this.updateMain, this.defaultError, e.target.name)  
        } else {
            this.handle(null, "/" + type + "/" + date_query, "GET", null, this.updateMain, this.defaultError, e.target.name) 
        }
    }

    searchClick = (e, type, year, month, day, weekDay, spec) => {
        query = (weekDay != null ? weekDay : "" ) + "-" + (year != null ? year : "" ) + "-" + (month != null ? month : "" ) + "-" + (day != null ? day : "" )

        this.handle(null, "/search?" + type + "=" + spec + '&date=' + query, "GET", null, this.updateMain, this.defaultError, 'search')  
    }

    getTableHeader = () => {
        output = []
        if (this.content.length > 0){
            for (key in Object.keys(this.content[0])){
                output.push(<th>{key}</th>);
            }
        }
        return output;
    }

    convertDayString = (dateString) => {
        spec = dateString.split('-');
        return {'year' : spec[1], 'month' : spec[2], 'day' : spec[3] : 'week_day' : spec[0]}
    }

    getTableBody = () => {
        output = [];
        urlSplit = this.url.substring(0, this.url.indexOf('?')).split('/');
        dayString = urlSplit.length == 3 ? urlSplit[2] : null;
        dateSpec = dayString ? this.convertDayString(dayString) : {};

        for (row in this.content) {
            outputRow = []
            for (item in row) {
                if (this.type == 'news' && item == row['category']){
                    outputRow.push(<td><span><a onClick={(e) => this.dataClick(e, 'category', row['year'], null, null, null, item)}>{item}</a></span></td>);
                } else if (this.type == 'news'){
                    outputRow.push(<td><span><a onClick={(e) => this.searchClick(e, 'date', row['year'], null, null, null, item)}>{item}</a></span></td>);
                } else if (item == row['year']){
                    outputRow.push(<td><span><a onClick={(e) => this.dataClick(e, this.type, row['year'], null, null, null, null )}>{item}</a></span></td>);
                } else if (item == row['month']){
                    outputRow.push(<td><span><a onClick={(e) => this.dataClick(e, this.type, row['year'], row['month'], null, null, null )}>{item}</a></span></td>);
                } else if (item == row['day']){
                    outputRow.push(<td><span><a onClick={(e) => this.dataClick(e, this.type, row['year'], row['month'], row['day'], null, null )}>{item}</a></span></td>);
                } else if (item == 'week_day'){
                    outputRow.push(<td><span><a onClick={(e) => this.dataClick(e, this.type, row['year'], row['month'], row['day'], row['week_day'], null )}>{item}</a></span></td>);
                } else if (item == 'category' || item == 'topic' || item == 'tag' || item == 'sentiment' ){
                    outputRow.push(<td><span><a onClick={(e) => this.dataClick(e, this.type, dateSpec['year'], dateSpec['month'], dateSpec['day'], dateSpec['week_day'], item )}>{item}</a></span></td>);
                } else if (item == 'news_count' ){
                    outputRow.push(<td><span><a onClick={(e) => this.searchClick(e, this.type, dateSpec['year'], dateSpec['month'], dateSpec['day'], dateSpec['week_day'], row[this.type])}>{item}</a></span></td>);
                } else{
                    outputRow.push(<td><span>{item}</span></td>);
                }


            }
            output.push(<tr>{outputRow}</tr>);
        }
    };

    render() {

        return (
            <div class="wrapper">
                <table>
                    <thead>
                        <tr>
                            {this.getTableHeader()}
                        </tr>
                    </thead>
                    <tbody>
                        {this.getTableBody()}
                    </tbody>
                </table>
            </div>
            
        );
    }
};


export default MainTable;