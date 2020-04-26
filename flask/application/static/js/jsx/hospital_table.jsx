import React from 'react';

'use strict'

function HospitalData(props) {
    return (
        <div>
            <p>Capacity: {props.capacity}</p>
            <p>Beds: {props.beds}</p>
            <p>ICUs: {props.icus}</p>
            <p>Ventilators: {props.ventilators}</p>
            <p>COVID Tests: {props.covidTests}</p>
            <p>COVID Patients: {props.covidPatients}</p>
            <p>COVID Patient Percentage {props.covidPercentage}%</p>
        </div>
    );
}

class MobileHospitalTable extends React.Component{
    constructor(props) {
        this.state = {
            expandedData: null,
        }
    }

    render() {
        <table className="sortable">
            <thead>
                <tr>
                    <th>Date</th>
                    <th>User</th>
                    <th>Show Data</th>
                </tr>
            </thead>
            {this.props.data.map(dataEntry => {
                return (
                    <tr>
                        <td>{ d.date.strftime('%m/%d/%y') }</td>
                        <td><a class="mr-2" href="{{ url_for('view_user', user_id=d.user) }}">{ d.user }</a></td>
                        <td>Show Data</td>
                    </tr>
                );
            })}
        </table>
    }
}

ReactDOM.render(<MobileHospitalTable data='hello'/>, document.getElementById('data_table'))
