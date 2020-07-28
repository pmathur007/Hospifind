var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

function TCList(props) {
    return React.createElement(
        "div",
        { id: "tc_results" },
        props.data.map(function (d, i) {
            return React.createElement(
                "div",
                { key: i, id: d.id, className: "tc_result" },
                React.createElement(
                    "p",
                    null,
                    React.createElement(
                        "strong",
                        null,
                        d.name
                    ),
                    React.createElement("br", null),
                    d.address,
                    React.createElement("br", null),
                    d.distance,
                    " - ",
                    d.time,
                    React.createElement("br", null),
                    React.createElement(
                        "strong",
                        null,
                        "Details:"
                    ),
                    React.createElement("br", null),
                    d.walkUp ? "Walk Up" : "Drive Thru",
                    React.createElement("br", null),
                    "Referral required: ",
                    d.referral ? "Yes" : "No",
                    React.createElement("br", null),
                    "Appointment required: ",
                    d.appointment ? "Yes" : "No",
                    React.createElement("br", null)
                )
            );
        })
    );
}

var FilterForm = function (_React$Component) {
    _inherits(FilterForm, _React$Component);

    function FilterForm(props) {
        _classCallCheck(this, FilterForm);

        var _this = _possibleConstructorReturn(this, (FilterForm.__proto__ || Object.getPrototypeOf(FilterForm)).call(this, props));

        _this.state = {
            walkUp: null,
            referral: null,
            appointment: null
        };
        _this.clearFilters = _this.clearFilters.bind(_this);
        return _this;
    }

    _createClass(FilterForm, [{
        key: "clearFilters",
        value: function clearFilters() {
            this.setState({
                walkUp: null,
                referral: null,
                appointment: null
            });
            this.props.clearFilters();
        }
    }, {
        key: "changeFilter",
        value: function changeFilter(name, value) {
            if (name === "walkUp") {
                this.setState({ walkUp: value });
            } else if (name === "referral") {
                this.setState({ referral: value });
            } else if (name === "appointment") {
                this.setState({ appointment: value });
            }
        }
    }, {
        key: "render",
        value: function render() {
            var _this2 = this;

            return React.createElement(
                "div",
                { id: "filterForm" },
                React.createElement(
                    "p",
                    null,
                    "Filter Centers"
                ),
                React.createElement(
                    "fieldset",
                    null,
                    React.createElement(
                        "legend",
                        null,
                        "Type"
                    ),
                    React.createElement("input", {
                        id: "typeWalk",
                        type: "radio",
                        name: "type",
                        checked: this.state.walkUp !== null && this.state.walkUp,
                        onChange: function onChange() {
                            return _this2.changeFilter("walkUp", true);
                        }
                    }),
                    React.createElement(
                        "label",
                        { htmlFor: "typeWalk" },
                        "Walk Up"
                    ),
                    React.createElement("input", {
                        id: "typeDrive",
                        type: "radio",
                        name: "type",
                        checked: this.state.walkUp !== null && !this.state.walkUp,
                        onChange: function onChange() {
                            return _this2.changeFilter("walkUp", false);
                        }
                    }),
                    React.createElement(
                        "label",
                        { htmlFor: "typeDrive" },
                        "Drive Thru"
                    )
                ),
                React.createElement(
                    "fieldset",
                    null,
                    React.createElement(
                        "legend",
                        null,
                        "Referral Required"
                    ),
                    React.createElement("input", {
                        id: "referralYes",
                        type: "radio",
                        name: "referral",
                        checked: this.state.referral !== null && this.state.referral,
                        onChange: function onChange() {
                            return _this2.changeFilter("referral", true);
                        }
                    }),
                    React.createElement(
                        "label",
                        { htmlFor: "referralYes" },
                        "Yes"
                    ),
                    React.createElement("input", {
                        id: "referralNo",
                        type: "radio",
                        name: "referral",
                        checked: this.state.referral !== null && !this.state.referral,
                        onChange: function onChange() {
                            return _this2.changeFilter("referral", false);
                        }
                    }),
                    React.createElement(
                        "label",
                        { htmlFor: "referralNo" },
                        "No"
                    )
                ),
                React.createElement(
                    "fieldset",
                    null,
                    React.createElement(
                        "legend",
                        null,
                        "Appointment Required"
                    ),
                    React.createElement("input", {
                        id: "appointmentYes",
                        type: "radio",
                        name: "appointment",
                        checked: this.state.appointment !== null && this.state.appointment,
                        onChange: function onChange() {
                            return _this2.changeFilter("appointment", true);
                        }
                    }),
                    React.createElement(
                        "label",
                        { htmlFor: "appointmentYes" },
                        "Yes"
                    ),
                    React.createElement("input", {
                        id: "appointmentNo",
                        type: "radio",
                        name: "appointment",
                        checked: this.state.appointment !== null && !this.state.appointment,
                        onChange: function onChange() {
                            return _this2.changeFilter("appointment", false);
                        }
                    }),
                    React.createElement(
                        "label",
                        { htmlFor: "appointmentNo" },
                        "No"
                    )
                ),
                React.createElement(
                    "div",
                    { id: "filter_buttons" },
                    React.createElement(
                        "button",
                        { className: "btn-light", onClick: function onClick() {
                                return _this2.props.applyFilters(_this2.state);
                            } },
                        "Apply Filters"
                    ),
                    React.createElement(
                        "button",
                        { className: "btn-light", onClick: this.clearFilters },
                        "Clear Filters"
                    )
                )
            );
        }
    }]);

    return FilterForm;
}(React.Component);

var FilteredTestCenters = function (_React$Component2) {
    _inherits(FilteredTestCenters, _React$Component2);

    function FilteredTestCenters(props) {
        _classCallCheck(this, FilteredTestCenters);

        var _this3 = _possibleConstructorReturn(this, (FilteredTestCenters.__proto__ || Object.getPrototypeOf(FilteredTestCenters)).call(this, props));

        _this3.state = {
            data: _this3.props.data,
            filteredData: _this3.props.data
        };
        _this3.clearFilters = _this3.clearFilters.bind(_this3);
        _this3.applyFilters = _this3.applyFilters.bind(_this3);
        return _this3;
    }

    _createClass(FilteredTestCenters, [{
        key: "clearFilters",
        value: function clearFilters() {
            this.setState({ filteredData: this.props.data });
        }
    }, {
        key: "applyFilters",
        value: function applyFilters(filters) {
            var filteredData = this.state.data;
            filteredData = filteredData.filter(function (d) {
                var keep = true;
                keep &= filters.walkUp === null || d.walkUp == filters.walkUp;
                keep &= filters.referral === null || d.referral == filters.referral;
                keep &= filters.appointment === null || d.appointment == filters.appointment;
                return keep;
            });

            this.setState({
                filteredData: filteredData
            });
        }
    }, {
        key: "render",
        value: function render() {
            return React.createElement(
                "div",
                { id: "tc_results_control" },
                React.createElement(FilterForm, { clearFilters: this.clearFilters, applyFilters: this.applyFilters }),
                React.createElement(TCList, { data: this.state.filteredData })
            );
        }
    }]);

    return FilteredTestCenters;
}(React.Component);

function loadTestingCenters(data) {
    ReactDOM.render(React.createElement(FilteredTestCenters, { data: data }), document.getElementById("tc_results_container"));
}