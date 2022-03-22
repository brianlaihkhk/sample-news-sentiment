import React, {Component} from "react";

class Search extends Component {
    constructor(props){
        super(props);
        this.handle = props.handle;
        this.updateMain = props.updateMain;
        this.defaultError = props.defaultError;
    }

    state = {
        criteria : new Map(),
        userSearchType : null,
        userSearchText : null
    }

    onSearchTypeChange = (e) => {
        this.setState({userSearchType : e.target.value.trim()});
    }

    onSearchTextChange = (e) => {
        this.setState({userSearchText : e.target.value.trim()});
    }

    validateForm = (e) => {
        if (this.state.userSearchType && !(this.state.userSearchType === 'select') && this.state.userSearchText){

            this.addCriteria(this.state.userSearchType, this.state.userSearchText);
            this.setState({userSearchType: null, userSearchText : null});
            document.getElementById("searchForm").reset();
        }
    }
    
    addCriteria = (key, value) => { 
        var new_criteria = this.state.criteria;
        
        if (new_criteria.get(key) == null){
            new_criteria.set(key, value.toLowerCase());
        } else {
            var new_value = new_criteria.get(key) + ',' + value.toLowerCase();
            new_criteria.set(key, new_value);
        }
        
        this.setState({criteria : new_criteria});
    }

    resetCriteria = (e) => {
        this.setState({criteria : new Map()});
        document.getElementById("searchForm").reset();
    }


    submitCriteria = (e) => {
        if (this.state.criteria.size > 0){
            const params = new URLSearchParams(this.state.criteria);
            this.handle(null, "/search?" + params.toString(), "GET", null, this.updateMain, this.defaultError, 'search');
            document.getElementById("searchForm").reset();
        }
    }

    printCurrentCriteria = (e) => {
        var output = []
        var enteries = [...this.state.criteria.entries()]

        enteries.forEach((item) => {
            var key = item[0];
            var value = item[1];
            output.push(<p>{key} : {value}</p>);
        });

        return output;
    }

    render() {
        var currentCriteria = this.printCurrentCriteria();
        return (
            <div>
                <p>Search</p>
                <form id="searchForm">
                    <select name="type" id="type"  onChange={this.onSearchTypeChange}>
                        <option value="select" default>-- Please select --</option>
                        <option value="category">Category</option>
                        <option value="topic">Topic</option>
                        <option value="tag">Tag</option>
                        <option value="sentiment">Sentiment</option>
                    </select>
                    <input type="text" name="query" onChange={this.onSearchTextChange} />
                    <input type="button" value="ADD" onClick={this.validateForm} />
                </form>
                <br />
                <button onClick={this.submitCriteria} >Search</button> <button onClick={this.resetCriteria} >Reset</button>
                <hr />
                <p>Current Search Criteria :</p>
                <p>{currentCriteria}</p>
            </div>
            
        );
    }
};


export default Search;