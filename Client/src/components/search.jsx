import React, {Component} from "react";

class Search extends Component {
    constructor(props){
        super(props);
        this.handle = props.handle;
        this.updateMain = props.updateMain;
        this.defaultError = props.defaultError;
    }

    state = {
        criteria : new Map()
    }

    addCriteria = (e) => {
        new_criteria = this.state.criteria;
        if (new_criteria.get(e.taget.type.value) == null){
            new_criteria.set(e.taget.type.value, e.target.query.value);
        } else {
            var new_value = new_criteria.get(e.taget.type.value) + ',' + e.target.query.value
            new_criteria.set(e.taget.type.value, new_value);
        }
        
        setState({criteria : new_criteria})
    }

    resetCriteria = (e) => {
        setState({criteria : new Map()})
    }


    submitCriteria = (e) => {
        const params = new URLSearchParams(this.state.criteria)
        this.handle(null, "/search?" + params.toString(), "GET", null, this.updateMain, this.defaultError, 'search')  
    }

    render() {
        return (
            <div>
                <p>Search</p>
                <p>
                    <form onSubmit={this.addCriteria}>
                        <select name="type" id="type">
                            <option value="category">Category</option>
                            <option value="topic">Topic</option>
                            <option value="tag">Tag</option>
                            <option value="sentiment">Sentiment</option>
                        </select>
                        <input type="text" name="query" />
                        <input type="submit" value="ADD" />
                    </form>
                </p>

                <button onClick={this.submitCriteria} >Search</button> <button onClick={this.resetCriteria} >Reset</button>
                <hr />
                <p>Current Search Criteria :</p>
                <p>{this.state.criteria}</p>
            </div>
            
        );
    }
};


export default Search;