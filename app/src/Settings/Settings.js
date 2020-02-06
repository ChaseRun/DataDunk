import React from "react"
import './Settings.css'

import Button from 'react-bootstrap/Button'

class Settings extends React.Component {
    render() {
       return (
        <div id="Settings-Border">
            <h5 id="Settings-Header"> <b> Settings </b> </h5>
        
            <div id="Settings-Section">
                <div id="Websites">
                    <div>
                        <Button variant="primary">FanDuel</Button>
                    </div>
                    <div>
                        <Button variant="outline-success">Draft Kings</Button>
                    </div>
                </div>

                <div id="Optimize">
                    <Button variant="outline-danger" size="lg" block>Optimize</Button>
                </div>
            </div>
        </div>
       )
    }
 }

export default Settings