import React, { Component } from "react";
import SelectMenu from "./components/select_menu";
import MainView from "./components/main_view";
import Search from "./components/search";
import Category from "./components/category";

const HOST = 'http://localhost:8000';

class App extends Component {

  state = {
    content : 'main',
    type : 'main',
    url : null
  };

  handleCall = (e, url, method, request_header, successHandler, notSuccessHandler, successType) => {
    if (e != null) {
      e.preventDefault();
    }

    var headers = {}
    Object.assign(headers, request_header)

    fetch(HOST + url, {
      method: method,
      headers: headers,
      mode: 'cors', // no-cors, *cors, same-origin
      cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
      credentials: 'same-origin', // include, *same-origin, omit,
      redirect: 'follow', // manual, *follow, error
      referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    })
    .then(response => response.json())
    .then(response => response.success ? successHandler(response.payload, url, successType) : notSuccessHandler(response.payload))
    .catch(err => this.exceptionHandler(err));
  }

  updateMain = (payload, url, type) => {
    this.setState({ content : payload , url: url, type : type });
  }

  exceptionHandler = (err) => {
    console.log("exceptionHandler");
    console.log(err);
    this.setState({ content : "Internal Server Error.  Please retry again.", type : 'error' });
  }

  notSucessDisplayError = (payload) => {
    console.log("notSucessDisplayError");
    console.log(payload);
    this.setState({ content : payload != null ? "Connection Error. " + payload : "Connection Error. Please retry again.", type : 'error' });
  }

  render() {
    return (
      <div className="main__wrap">
        <main className="container">
          <div className="header">
              <SelectMenu handle={this.handleCall} updateMain={this.updateMain} defaultError={this.notSucessDisplayError} />
          </div>
          <div className="wrapper clearfix">
            <div className="section">
              <MainView state={this.state} handle={this.handleCall} updateMain={this.updateMain} defaultError={this.notSucessDisplayError} />
            </div>
            <div className="nav">
              <Search handle={this.handleCall} updateMain={this.updateMain} defaultError={this.notSucessDisplayError} />
              <Category handle={this.handleCall} updateMain={this.updateMain} defaultError={this.notSucessDisplayError} />
            </div>
          </div>
        </main>
      </div>
    );
  }
}

export default App;
