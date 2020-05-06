class MobileDataTable extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            data: props.data,
            showingData: Array(props.data.length).fill(false),
            deleteConfirmation: Array(props.data.length).fill(false)
        }
        this.toggleDetails = this.toggleDetails.bind(this);
    }

    toggleDetails(i) {
        const newShowing = this.state.showingData.slice();
        newShowing[i] = !newShowing[i];
        this.setState({showingData: newShowing});
    }
    
    deleteEntry(i) {
        const newDeleteConf = this.state.deleteConfirmation.slice();
        if (!newDeleteConf[i])
        {
            newDeleteConf[i] = true;
            this.setState({deleteConfirmation: newDeleteConf});
        }
        else
        {

        }
    }

    render() {
        return (
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>User</th>
                        <th>Details</th>
                        <th>Delete User</th>
                    </tr>
                </thead>
                {this.state.data.map((d, i) => {
                    return (
                        <tbody key={d.id}>
                            <tr>
                                <td>{ d.date.split(":", 2).join(":") }</td>
                                <td>{ d.user }</td>
                                <td><button onClick={ () => this.toggleDetails(i) }>Details</button></td>
                                <td><button onClick={ () => this.deleteEntry(i) }>{ this.state.deleteConfirmation[i] ? "Confirm Delete" : "Delete" }</button></td>
                            </tr>
                            {this.state.showingData[i] ? (
                                <tr>
                                    <td colSpan={3}>
                                        <p>Capacity: {d.bed_capacity}</p>
                                        <p>Beds: {d.beds_available}</p>
                                        <p>ICUs: {d.icus_available}</p>
                                        <p>Ventilators: {d.ventilators_available}</p>
                                        <p>COVID-19 Tests: {d.coronavirus_tests_available}</p>
                                        <p>COVID-19 Patients: {d.coronavirus_patients}</p>
                                        <p>COVID-19 Patient %: {d.coronavirus_patient_percent}</p>
                                    </td>
                                </tr>
                            ) : ''}
                        </tbody>
                    )
                })}    
            </table>
        );
    }
}

function FullDataTable(props) {
    return (
        <table>
            <thead>
                <tr>
                    <th>Date</th>
                    <th>User</th>
                    <th>Capacity</th>
                    <th>Beds</th>
                    <th>ICUs</th>
                    <th>Ventilators</th>
                    <th>COVID-19 Tests</th>
                    <th>COVID-19 Patients</th>
                    <th>COVID-19 Patient %</th>
                </tr>
            </thead>
            {props.data.map((d) => {
                return (
                    <tr key={d.id}>
                        <td>{ d.date }</td>
                        <td><a href="{{ url_for('view_user', user_id=d.user) }}">{ d.user }</a></td>
                        <td><p>{ d.bed_capacity }</p></td>
                        <td>{ d.beds_available }</td>
                        <td>{ d.icus_available }</td>
                        <td>{ d.ventilators_available }</td>
                        <td>{ d.coronavirus_tests_available }</td>
                        <td>{ d.coronavirus_patients }</td>
                        <td>{ d.coronavirus_patient_percent }</td>
                    </tr>
                );
            })}
        </table>
    )
}

$(document).ready(function() {
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
    }).done(function(json) {
        if (screen.width < 800) {
            ReactDOM.render(<MobileDataTable data={json}/>, document.getElementById("data_table"));
        }
        else {
            ReactDOM.render(<FullDataTable data={json}/>, document.getElementById("data_table"));
        }
        window.addEventListener("resize", function() {
            if (screen.width < 800) {
                ReactDOM.render(<MobileDataTable data={json}/>, document.getElementById("data_table"));
            }
            else {
                ReactDOM.render(<FullDataTable data={json}/>, document.getElementById("data_table"));
            }
        });
    });
});