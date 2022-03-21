import React, {Component} from "react";


class MainTable extends Component {
    constructor(props){
        super(props);
        this.type = props.type;
        this.content = props.content;
        this.handle = props.handle;
        this.updateMain = props.updateMain;
        this.defaultError = props.defaultError;
    }


    dataClick = (e, type, year, month, day, weekDay) => {
        query = (weekDay != null ? weekDay : "" ) + "-" + (year != null ? year : "" ) + "-" + (month != null ? month : "" ) + "-" + (day != null ? day : "" )

        this.handle(null, "/" + this.type + "/" + query, "GET", null, this.processSelection, this.fail, e.target.name)  
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
    getTableBody = () => {
        output = [];

        for (row in this.content) {
            output.push(<tr>
                {Object.keys(row).map(function(key){ 
                        return (<td><span><a onClick={(e) => this.dataClick(e, {this.type}, {row['year']}, {row['month']}, {row['day']}, {row['week_day']} )}>{row[key]}</a></span></td>);

                        })}
                </tr>);
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