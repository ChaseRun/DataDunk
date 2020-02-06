import React from "react"
import './PlayerSelection.css';

import Nav from 'react-bootstrap/Nav'
import Form from 'react-bootstrap/Form'
import FormControl from 'react-bootstrap/FormControl'
import Button from 'react-bootstrap/Button'

class PlayerSelection extends React.Component {
    render() {
       return (
            <div id="PlayerSelection-Border">
                <h5 id="PlayerSelection-Header"> <b> Players </b> </h5>
                
                <div id="PlayerSelection-Section">
                    <Nav fill justify variant="tabs" defaultActiveKey="/home">

                    <Form inline>
                        <FormControl type="text" placeholder="Search Player" className="mr-sm-2" />
                        <Button variant="outline-primary" >Search</Button>
                    </Form>

                    <Nav.Item>
                        <Nav.Link eventKey="link-8">All</Nav.Link>
                    </Nav.Item>
                    <Nav.Item>
                        <Nav.Link eventKey="link-1">PG</Nav.Link>
                    </Nav.Item>
                    <Nav.Item>
                        <Nav.Link eventKey="link-2">SG</Nav.Link>
                    </Nav.Item>
                    <Nav.Item>
                        <Nav.Link eventKey="link-3">SF</Nav.Link>
                    </Nav.Item>
                    <Nav.Item>
                        <Nav.Link eventKey="link-4">PF</Nav.Link>
                    </Nav.Item>
                    <Nav.Item>
                        <Nav.Link eventKey="link-5">C</Nav.Link>
                    </Nav.Item>
                    <Nav.Item>
                        <Nav.Link eventKey="link-6">G</Nav.Link>
                    </Nav.Item>
                    <Nav.Item>
                        <Nav.Link eventKey="link-7">F</Nav.Link>
                    </Nav.Item>
                </Nav>
            </div>
        </div>
       )
    }
 }

 export default PlayerSelection