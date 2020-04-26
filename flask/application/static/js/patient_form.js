'use_strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

function RadioInput(props) {
    return React.createElement(
        'label',
        null,
        React.createElement('input', {
            type: 'radio',
            value: props.value,
            checked: props.checked,
            onChange: props.onChange
        }),
        props.value
    );
}

var RadioField = function (_React$Component) {
    _inherits(RadioField, _React$Component);

    function RadioField(props) {
        _classCallCheck(this, RadioField);

        var _this = _possibleConstructorReturn(this, (RadioField.__proto__ || Object.getPrototypeOf(RadioField)).call(this, props));

        _this.handleOptionChange = function (e) {
            _this.setState({
                selectedOption: e.target.value
            });
        };

        _this.state = {
            selectedOption: _this.props.options[0]
        };
        return _this;
    }

    _createClass(RadioField, [{
        key: 'render',
        value: function render() {
            var _this2 = this;

            return React.createElement(
                'fieldset',
                null,
                React.createElement(
                    'legend',
                    null,
                    this.props.title
                ),
                this.props.options.map(function (option) {
                    return React.createElement(RadioInput, {
                        key: option,
                        value: option,
                        checked: _this2.state.selectedOption === option,
                        onChange: _this2.handleOptionChange
                    });
                })
            );
        }
    }]);

    return RadioField;
}(React.Component);

var PatientForm = function (_React$Component2) {
    _inherits(PatientForm, _React$Component2);

    function PatientForm() {
        _classCallCheck(this, PatientForm);

        return _possibleConstructorReturn(this, (PatientForm.__proto__ || Object.getPrototypeOf(PatientForm)).apply(this, arguments));
    }

    _createClass(PatientForm, [{
        key: 'render',
        value: function render() {
            return React.createElement('form', null);
        }
    }]);

    return PatientForm;
}(React.Component);

ReactDOM.render(React.createElement(PatientForm, null), document.getElementById('patient_form'));