function TCTable(props) {
    return (
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Address</th>
                    <th>Type</th>
                    <th>Referal Required</th>
                    <th>Appointement Required</th>
                </tr>
            </thead>
            <tbody>
            {props.data.map((d, i) => {
                return (
                    <tr key={i}>
                        <td>{ d.name }</td>
                        <td>{ d.address }</td>
                        <td>{ d.walkUp ? "Walk Up" : "Drive Thru" }</td>
                        <td>{ d.referral ? "Yes" : "No" }</td>
                        <td>{ d.appointment ? "Yes": "No" }</td>
                    </tr>
                );
            })}
            </tbody>
        </table>
    );
}

class FilterForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            walkUp: null,
            referral: null,
            appointment: null
        }
        this.clearFilters = this.clearFilters.bind(this);
    }

    clearFilters() {
        this.setState({
            walkUp: null,
            referral: null,
            appointment: null
        });
        this.props.clearFilters();
    }

    changeFilter(name, value) {
        if (name === "walkUp") {
            this.setState({walkUp: value});
        } else if (name === "referral") {
            this.setState({referral: value});
        } else if (name === "appointment") {
            this.setState({appointment: value});
        }
    }

    render() {
        return (
            <div id="filterForm">
                <fieldset>
                    <legend>Type</legend>
                    <label htmlFor="typeWalk">
                        <input 
                            id="typeWalk"
                            type="radio"
                            name="type"
                            checked={this.state.walkUp !== null && this.state.walkUp}
                            onChange={() => this.changeFilter("walkUp", true)}
                        />
                    Walk Up</label>
                    <label htmlFor="typeDrive">
                        <input
                            id="typeDrive"
                            type="radio"
                            name="type"
                            checked={this.state.walkUp !== null && !this.state.walkUp}
                            onChange={() => this.changeFilter("walkUp", false)}
                        /> 
                    Drive Thru</label>
                </fieldset>
                <fieldset>
                    <legend>Referral Required</legend>
                    <label htmlFor="referralYes">
                        <input
                            id="referralYes"
                            type="radio"
                            name="referral"
                            checked={this.state.referral !== null && this.state.referral}
                            onChange={() => this.changeFilter("referral", true)}
                        />
                    Yes</label>
                    <label htmlFor="referralNo">
                        <input
                            id="referralNo"
                            type="radio"
                            name="referral"
                            checked={this.state.referral !== null && !this.state.referral}
                            onChange={() => this.changeFilter("referral", false)}
                        />
                    No</label>
                </fieldset>
                <fieldset>
                    <legend>Appointment Required</legend>
                    <label htmlFor="appointmentYes">
                        <input
                            id="appointmentYes"
                            type="radio"
                            name="appointment"
                            checked={this.state.appointment !== null && this.state.appointment}
                            onChange={() => this.changeFilter("appointment", true)}
                        />
                    Yes</label>
                    <label htmlFor="appointmentNo">
                        <input
                            id="appointmentNo"
                            type="radio"
                            name="appointment"
                            checked={this.state.appointment !== null && !this.state.appointment}
                            onChange={() => this.changeFilter("appointment", false)}
                        />
                    No</label>
                </fieldset>
                <button onClick={() => this.props.applyFilters(this.state)}>Apply Filters</button>
                <button onClick={this.clearFilters}>Clear Filters</button>
            </div>
        );
    }
}

class FilteredTestCenters extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            data: this.props.data,
            filteredData: this.props.data
        };
        this.clearFilters = this.clearFilters.bind(this);
        this.applyFilters = this.applyFilters.bind(this);
    }

    clearFilters() {
        this.setState({filteredData: this.props.data});
    }

    applyFilters(filters) {
        let filteredData = this.state.data;
        filteredData = filteredData.filter((d) => {
            console.log(d);
            let keep = true;
            keep &= (filters.walkUp === null || d.walkUp == filters.walkUp);
            keep &= (filters.referral === null || d.referral == filters.referral);
            keep &= (filters.appointment === null || d.appointment == filters.appointment);
            return keep;
        });

        this.setState({
            filteredData: filteredData
        });
    }

    render() {
        return (
            <div>
                <FilterForm clearFilters={this.clearFilters} applyFilters={this.applyFilters}/>
                <TCTable data={this.state.filteredData}/>
            </div>
        );
    }
}

function loadTestingCenters(data) {
    ReactDOM.render(<FilteredTestCenters data={data}/>, document.getElementById("results"));
}