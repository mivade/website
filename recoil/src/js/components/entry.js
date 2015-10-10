import React from 'react';

/** Blog entries */
export class BlogEntry extends React.Component {
    static propTypes = {
        title: React.PropTypes.string.isRequired,
        author: React.PropTypes.string.isRequired,
        date: React.PropTypes.string.isRequired,
        lastChangedDate: React.PropTypes.string,  // TODO: use this
        content: React.PropTypes.string.isRequired
    };

    function render() {
        return (
            <div className="recoil-entry">
                <h2 className="recoil-entry-title">{this.props.title}</h2>
                <div className="recoil-entry-metadata">
                    Posted on {this.props.date} by {this.props.author}.
                </div>
                <div className="recoil-entry-content">
                    {this.props.content}
                </div>
            </div>
        );
    }
}
