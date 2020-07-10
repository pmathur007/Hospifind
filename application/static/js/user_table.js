var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var MobileUserTable = function (_React$Component) {
    _inherits(MobileUserTable, _React$Component);

    function MobileUserTable(props) {
        _classCallCheck(this, MobileUserTable);

        var _this = _possibleConstructorReturn(this, (MobileUserTable.__proto__ || Object.getPrototypeOf(MobileUserTable)).call(this, props));

        _this.state = {
            data: props.data,
            showingData: Array(props.data.length).fill(false)
        };
        _this.toggleDetails = _this.toggleDetails.bind(_this);
        return _this;
    }

    _createClass(MobileUserTable, [{
        key: "toggleDetails",
        value: function toggleDetails(i) {
            var newShowing = this.state.showingData.slice();
            newShowing[i] = !newShowing[i];
            this.setState({ showingData: newShowing });
        }
    }, {
        key: "render",
        value: function render() {
            var _this2 = this;

            return React.createElement(
                "table",
                null,
                React.createElement(
                    "thead",
                    null,
                    React.createElement(
                        "th",
                        null,
                        "Username"
                    ),
                    React.createElement(
                        "th",
                        null,
                        "Role"
                    ),
                    React.createElement(
                        "th",
                        null,
                        "User Info"
                    ),
                    React.createElement(
                        "th",
                        null,
                        "Data Details"
                    )
                ),
                this.state.data.map(function (d, i) {
                    return React.createElement(
                        "tbody",
                        { key: d.id },
                        React.createElement(
                            "tr",
                            null,
                            React.createElement(
                                "td",
                                null,
                                d.username
                            ),
                            React.createElement(
                                "td",
                                null,
                                d.is_admin ? "Admin" : "Data Input"
                            ),
                            React.createElement(
                                "td",
                                null,
                                React.createElement(
                                    "button",
                                    { onClick: function onClick() {
                                            return _this2.toggleDetails(i);
                                        } },
                                    "User Info"
                                )
                            ),
                            React.createElement(
                                "td",
                                null,
                                React.createElement(
                                    "button",
                                    null,
                                    "Data Details"
                                )
                            )
                        ),
                        _this2.state.showingData[i] ? React.createElement(
                            "tr",
                            null,
                            React.createElement(
                                "td",
                                { colSpan: 4 },
                                React.createElement(
                                    "p",
                                    null,
                                    "Name: ",
                                    d.name
                                ),
                                React.createElement(
                                    "p",
                                    null,
                                    "Email: ",
                                    d.email
                                )
                            )
                        ) : ""
                    );
                })
            );
        }
    }]);

    return MobileUserTable;
}(React.Component);

var FullUserTable = function (_React$Component2) {
    _inherits(FullUserTable, _React$Component2);

    function FullUserTable(props) {
        _classCallCheck(this, FullUserTable);

        var _this3 = _possibleConstructorReturn(this, (FullUserTable.__proto__ || Object.getPrototypeOf(FullUserTable)).call(this, props));

        _this3.state = {
            data: props.data
        };
        return _this3;
    }

    _createClass(FullUserTable, [{
        key: "render",
        value: function render() {
            return React.createElement(
                "table",
                null,
                React.createElement(
                    "thead",
                    null,
                    React.createElement(
                        "th",
                        null,
                        "Username"
                    ),
                    React.createElement(
                        "th",
                        null,
                        "Name"
                    ),
                    React.createElement(
                        "th",
                        null,
                        "Email"
                    ),
                    React.createElement(
                        "th",
                        null,
                        "Role"
                    ),
                    React.createElement(
                        "th",
                        null,
                        "Data Details"
                    )
                ),
                this.state.data.map(function (d) {
                    return React.createElement(
                        "tr",
                        { key: d.id },
                        React.createElement(
                            "td",
                            null,
                            d.username
                        ),
                        React.createElement(
                            "td",
                            null,
                            d.name
                        ),
                        React.createElement(
                            "td",
                            null,
                            d.email
                        ),
                        React.createElement(
                            "td",
                            null,
                            d.is_admin ? "Admin" : "Data Input"
                        ),
                        React.createElement(
                            "td",
                            null,
                            React.createElement(
                                "button",
                                null,
                                "Data Details"
                            )
                        )
                    );
                })
            );
        }
    }]);

    return FullUserTable;
}(React.Component);

function reloadUserTable(hospital_id) {
    query = {
        "table_name": "User",
        "filter_by": [{
            "field_name": "User.association",
            "operator": "equals",
            "field_value": hospital_id
        }]
    };

    $.ajax({
        type: "POST",
        url: "/db",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify(query)
    }).done(function (json) {
        if ($(window).width() < 800) {
            ReactDOM.render(React.createElement(MobileUserTable, { data: json }), document.getElementById("user_table"));
        } else {
            ReactDOM.render(React.createElement(FullUserTable, { data: json }), document.getElementById("user_table"));
        }
        window.addEventListener("resize", function () {
            if ($(window).width() < 800) {
                ReactDOM.render(React.createElement(MobileUserTable, { data: json }), document.getElementById("user_table"));
            } else {
                ReactDOM.render(React.createElement(FullUserTable, { data: json }), document.getElementById("user_table"));
            }
        });
    });
}