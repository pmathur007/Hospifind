var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var MobileDataTable = function (_React$Component) {
    _inherits(MobileDataTable, _React$Component);

    function MobileDataTable(props) {
        _classCallCheck(this, MobileDataTable);

        var _this = _possibleConstructorReturn(this, (MobileDataTable.__proto__ || Object.getPrototypeOf(MobileDataTable)).call(this, props));

        _this.state = {
            data: props.data,
            showingData: Array(props.data.length).fill(false),
            deleteConfirmation: Array(props.data.length).fill(false)
        };
        _this.toggleDetails = _this.toggleDetails.bind(_this);
        return _this;
    }

    _createClass(MobileDataTable, [{
        key: "toggleDetails",
        value: function toggleDetails(i) {
            var newShowing = this.state.showingData.slice();
            newShowing[i] = !newShowing[i];
            this.setState({ showingData: newShowing });
        }
    }, {
        key: "deleteEntry",
        value: function deleteEntry(i) {
            var newDeleteConf = this.state.deleteConfirmation.slice();
            if (!newDeleteConf[i]) {
                newDeleteConf[i] = true;
                this.setState({ deleteConfirmation: newDeleteConf });
            } else {}
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
                        "tr",
                        null,
                        React.createElement(
                            "th",
                            null,
                            "Date"
                        ),
                        React.createElement(
                            "th",
                            null,
                            "User"
                        ),
                        React.createElement(
                            "th",
                            null,
                            "Details"
                        ),
                        React.createElement(
                            "th",
                            null,
                            "Delete User"
                        )
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
                                d.date.split(":", 2).join(":")
                            ),
                            React.createElement(
                                "td",
                                null,
                                d.user
                            ),
                            React.createElement(
                                "td",
                                null,
                                React.createElement(
                                    "button",
                                    { onClick: function onClick() {
                                            return _this2.toggleDetails(i);
                                        } },
                                    "Details"
                                )
                            ),
                            React.createElement(
                                "td",
                                null,
                                React.createElement(
                                    "button",
                                    { onClick: function onClick() {
                                            return _this2.deleteEntry(i);
                                        } },
                                    _this2.state.deleteConfirmation[i] ? "Confirm Delete" : "Delete"
                                )
                            )
                        ),
                        _this2.state.showingData[i] ? React.createElement(
                            "tr",
                            null,
                            React.createElement(
                                "td",
                                { colSpan: 3 },
                                React.createElement(
                                    "p",
                                    null,
                                    "Capacity: ",
                                    d.bed_capacity
                                ),
                                React.createElement(
                                    "p",
                                    null,
                                    "Beds: ",
                                    d.beds_available
                                ),
                                React.createElement(
                                    "p",
                                    null,
                                    "ICUs: ",
                                    d.icus_available
                                ),
                                React.createElement(
                                    "p",
                                    null,
                                    "Ventilators: ",
                                    d.ventilators_available
                                ),
                                React.createElement(
                                    "p",
                                    null,
                                    "COVID-19 Tests: ",
                                    d.coronavirus_tests_available
                                ),
                                React.createElement(
                                    "p",
                                    null,
                                    "COVID-19 Patients: ",
                                    d.coronavirus_patients
                                ),
                                React.createElement(
                                    "p",
                                    null,
                                    "COVID-19 Patient %: ",
                                    d.coronavirus_patient_percent
                                )
                            )
                        ) : ''
                    );
                })
            );
        }
    }]);

    return MobileDataTable;
}(React.Component);

function FullDataTable(props) {
    return React.createElement(
        "table",
        null,
        React.createElement(
            "thead",
            null,
            React.createElement(
                "tr",
                null,
                React.createElement(
                    "th",
                    null,
                    "Date"
                ),
                React.createElement(
                    "th",
                    null,
                    "User"
                ),
                React.createElement(
                    "th",
                    null,
                    "Capacity"
                ),
                React.createElement(
                    "th",
                    null,
                    "Beds"
                ),
                React.createElement(
                    "th",
                    null,
                    "ICUs"
                ),
                React.createElement(
                    "th",
                    null,
                    "Ventilators"
                ),
                React.createElement(
                    "th",
                    null,
                    "COVID-19 Tests"
                ),
                React.createElement(
                    "th",
                    null,
                    "COVID-19 Patients"
                ),
                React.createElement(
                    "th",
                    null,
                    "COVID-19 Patient %"
                )
            )
        ),
        props.data.map(function (d) {
            return React.createElement(
                "tr",
                { key: d.id },
                React.createElement(
                    "td",
                    null,
                    d.date
                ),
                React.createElement(
                    "td",
                    null,
                    React.createElement(
                        "a",
                        { href: "{{ url_for('view_user', user_id=d.user) }}" },
                        d.user
                    )
                ),
                React.createElement(
                    "td",
                    null,
                    React.createElement(
                        "p",
                        null,
                        d.bed_capacity
                    )
                ),
                React.createElement(
                    "td",
                    null,
                    d.beds_available
                ),
                React.createElement(
                    "td",
                    null,
                    d.icus_available
                ),
                React.createElement(
                    "td",
                    null,
                    d.ventilators_available
                ),
                React.createElement(
                    "td",
                    null,
                    d.coronavirus_tests_available
                ),
                React.createElement(
                    "td",
                    null,
                    d.coronavirus_patients
                ),
                React.createElement(
                    "td",
                    null,
                    d.coronavirus_patient_percent
                )
            );
        })
    );
}

$(document).ready(function () {
    query = {
        "table_name": "Data",
        "filter_by": [{
            "field_name": "Data.hospital",
            "operator": "equals",
            "field_value": 1
        }]
    };

    $.ajax({
        type: "POST",
        url: "/db",
        data: JSON.stringify(query),
        contentType: "application/json",
        dataType: "json"
    }).done(function (json) {
        if (screen.width < 800) {
            ReactDOM.render(React.createElement(MobileDataTable, { data: json }), document.getElementById("data_table"));
        } else {
            ReactDOM.render(React.createElement(FullDataTable, { data: json }), document.getElementById("data_table"));
        }
        window.addEventListener("resize", function () {
            if (screen.width < 800) {
                ReactDOM.render(React.createElement(MobileDataTable, { data: json }), document.getElementById("data_table"));
            } else {
                ReactDOM.render(React.createElement(FullDataTable, { data: json }), document.getElementById("data_table"));
            }
        });
    });
});