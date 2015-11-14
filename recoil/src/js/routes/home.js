/** Top-level route. */

import React from 'react';
import { Page } from '../components/page';
import { MarkerUpper } from '../markup';

export class Home extends React.Component {
    render() {
        var markerUpper = new MarkerUpper(this.props.src);
        var content = markerUpper.render();
        return <Page content={content} />
    }
}

Home.propTypes = {
    src: React.PropTypes.string.isRequired;
}
