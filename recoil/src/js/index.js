import React from 'react';
import { Router, Route, Link } from 'react-router';
import { Home } from './routes/home';

React.render((
    <Router>
        <Route path='/' component={Home} />
        <Route path='blog' component={Blog}>
            <Route path='/blog/:entry' component={Blog} />
        </Route>
    </Router>
), document.body);
