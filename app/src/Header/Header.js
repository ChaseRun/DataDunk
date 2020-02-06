import React from "react"
import './Header.css'

class Header extends React.Component {
    render() {
       return (
        <div id="Header-Section">
            <div>
                <h1 id="Title"> <b> Data Dunk </b> </h1>
                <h3 id="Title"> Fantasy Optimizer </h3>
            </div>

            <div id="Links">
                <div>
                    <a id="About" href="/"> About </a>
                </div>
                <div>
                    <a id="About" href="/"> Source Code </a>
                </div>
            </div>

            <div id="Twitter">
                <a id="About" href="https://twitter.com/DataDunk"> Twitter </a>
            </div>

            <div id="Description">
                <p id="Description-Text">A Machine Learning NBA Fanduel/Draft Kings Optimizer</p>
            </div>
        </div>
       )
    }
 }

export default Header