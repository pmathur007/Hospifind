class MobileDataTable extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            data: props.data,
            showingData: Array(props.data.length).fill(false),
        }
        this.toggleDetails = this.toggleDetails.bind(this);
    }

    toggleDetails(i) {
        const newShowing = this.state.showingData.slice();
        newShowing[i] = !newShowing[i];
        this.setState({showingData: newShowing});
    }
    
    deleteEntry(i) {
        if (window.confirm("Do you want to delete this entry?")) {
            query = {
                "table_name": "Data",
                "filter_by": [{
                    "field_name": "Data.id",
                    "operator": "equals",
                    "field_value": this.state.data[i].id
                }]
            };

            $.ajax({
                type: "DELETE",
                url: "/db",
                data: JSON.stringify(query),
                contentType: "application/json",
                dataType: "json"
            });

            const newData = this.state.data.slice();
            const newShowingData = this.state.showingData.slice();
            newData.splice(i, 1); newShowingData.splice(i, 1);
            
            this.setState({
                data: newData,
                showingData: newShowingData
            });
        }
    }

    render() {
        return (
            <table className="sortable">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>User</th>
                        <th>Details</th>
                        <th>Delete</th>
                    </tr>
                </thead>
                {this.state.data.map((d, i) => {
                    return (
                        <tbody key={d.id}>
                            <tr>
                                <td>{ d.date.split(":", 2).join(":") }</td>
                                <td>{ d.user }</td>
                                <td onClick={ () => this.toggleDetails(i) } className="td-clickable">Details</td>
                                <td onClick={ () => this.deleteEntry(i) } className="td-clickable">Delete</td>
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
                    );
                })}    
            </table>
        );
    }
}

class FullDataTable extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            data: props.data
        }
    }

    deleteEntry(i) {
        if (window.confirm("Do you want to delete this entry?")) {
            query = {
                "table_name": "Data",
                "filter_by": [{
                    "field_name": "Data.id",
                    "operator": "equals",
                    "field_value": this.state.data[i].id
                }]
            };

            $.ajax({
                type: "DELETE",
                url: "/db",
                data: JSON.stringify(query),
                contentType: "application/json",
                dataType: "json"
            });

            const newData = this.state.data.slice();
            const newShowingData = this.state.showingData.slice();
            newData.splice(i, 1); newShowingData.splice(i, 1);
            
            this.setState({
                data: newData,
                showingData: newShowingData
            });
        }
    }

    render() {
        return (
            <table className="sortable">
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
                        <th>Delete User</th>
                    </tr>
                </thead>
                {this.state.data.map((d, i) => {
                    return (
                        <tr key={d.id}>
                            <td>{ d.date.split(":", 2).join(":") }</td>
                            <td><a href="{{ url_for('view_user', user_id=d.user) }}">{ d.user }</a></td>
                            <td><p>{ d.bed_capacity }</p></td>
                            <td>{ d.beds_available }</td>
                            <td>{ d.icus_available }</td>
                            <td>{ d.ventilators_available }</td>
                            <td>{ d.coronavirus_tests_available }</td>
                            <td>{ d.coronavirus_patients }</td>
                            <td>{ d.coronavirus_patient_percent }</td>
                            <td onClick={ () => this.deleteEntry(i) } className="td-clickable">Delete</td>
                        </tr>
                    );
                })}
            </table>
        );
    }
}


function reloadDataTable(hospital_id) {
    query = {
        "table_name": "Data",
        "filter_by": [{
            "field_name": "Data.hospital",
            "operator": "equals",
            "field_value": hospital_id
        }]
    };
    
    $.ajax({
        type: "POST",
        url: "/db",
        data: JSON.stringify(query),
        contentType: "application/json",
        dataType: "json"
    }).done(function(json) {
        if ($(window).width() < 800) {
            ReactDOM.render(<MobileDataTable data={json}/>, document.getElementById("data_table"));
        }
        else {
            ReactDOM.render(<FullDataTable data={json}/>, document.getElementById("data_table"));
        }
        window.addEventListener("resize", function() {
            if ($(window).width() < 800) {
                ReactDOM.render(<MobileDataTable data={json}/>, document.getElementById("data_table"));
            }
            else {
                ReactDOM.render(<FullDataTable data={json}/>, document.getElementById("data_table"));
            }
        });
    });
}