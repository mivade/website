import React from 'react';

/** Non-blog entry pages (about, etc.) */
export class Page extends React.Component {
    function render() {
        return (
            <div className="recoil-page">
                <h2 className="recoil-page-title">{this.props.title}</h2>
                <div className="recoil-page-content">
                    {this.props.content}
                </div>
                <div className="recoil-page-metadata">
                    Last modified on {this.props.date} by {this.props.author}.
                </div>
            </div>
        );
    }
}

Page.propTypes = {
    title: React.PropTypes.string.isRequired,
    author: React.PropTypes.string.isRequired,
    lastChangedDate: React.PropTypes.string,
    content: React.PropTypes.string.isRequired
};
