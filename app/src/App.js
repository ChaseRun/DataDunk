import React from "react"
import './App.css';


import Header from "./Header/Header"
import Settings from "./Settings/Settings"
import Legend from "./Legend/Legend"
import PlayerSelection from "./PlayerSelection/PlayerSelection"
import PlayerTable from "./PlayerTable/PlayerTable"

import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'




class App extends React.Component {
  render() {
    
    return (
      <Container fluid>
      <Row>
        <Col sm={3} style={{padding: "0px"}}>
            <Header />
            <Settings />
            <Legend />
        </Col>
        <Col sm={9} style={{padding: "0px"}}>
            <PlayerSelection />
            <PlayerTable />
        </Col>
      </Row>
  </Container>
     
     
     )
  }
}

export default App
