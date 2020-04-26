import React from 'react';
import { Formik } form 'formik';

'use_strict';

function RadioInput(props) {
    return (
        <label>
            <input
                type="radio"
                value={props.value}
                checked={props.checked}
                onChange={props.onChange}
            />
            {props.value}
        </label>
    );
}

class RadioField extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            selectedOption: this.props.options[0],
        };
    }

    handleOptionChange = e => {
        this.setState({
            selectedOption: e.target.value,
        });
    };

    render() {
        return (
            <fieldset>
                <legend>{this.props.title}</legend>
                {this.props.options.map((option) => {
                    return <RadioInput
                                key={option}
                                value={option}
                                checked={this.state.selectedOption === option}
                                onChange={this.handleOptionChange}
                            />
                })}
            </fieldset>
        );
    }
}

class CheckboxField extends React.Component {

}

class PatientForm extends React.Component {
    render() {
        return (
            <form>
            </form>
        );
    }
}

ReactDOM.render(<PatientForm/>, document.getElementById('patient_form'));
