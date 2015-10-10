import React from 'react';
import { Navbar, NavBrand, Nav } from 'react-bootstrap';

/** Bootstrap Navbar component. */
export class SiteNavbar extends React.Component {
    render() {
        return (
            <Navbar>
                <Nav>
                    <NavItem eventKey={1} href="#">Link</NavItem>
                    <NavItem eventKey={2} href="#">Link</NavItem>
                </Nav>
            </Navbar>
        );
    }
}
