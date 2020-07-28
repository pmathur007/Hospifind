function TCList(props) {
    return (
        <div id="tc_results">
            {props.data.map((d, i) => {
                return (
                    <div key={i} id={ d.id } className="tc_result">
                        <p>
                            <strong>{ d.name }</strong><br/>
                            { d.address }<br/>
                            { d.distance } - {d.time}<br/>
                            <strong>Details:</strong><br/>
                            { d.walkUp ? "Walk Up" : "Drive Thru" }<br/>
                            Referral required: { d.referral ? "Yes" : "No" }<br/>
                            Appointment required: { d.appointment ? "Yes": "No" }<br/>
                        </p>
                    </div>
                );
            })}
        </div>
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
                <p>Filter Centers</p>
                <fieldset>
                    <legend>Type</legend>
                    <input 
                        id="typeWalk"
                        type="radio"
                        name="type"
                        checked={this.state.walkUp !== null && this.state.walkUp}
                        onChange={() => this.changeFilter("walkUp", true)}
                    />
                    <label htmlFor="typeWalk">Walk Up</label>
                    <input
                        id="typeDrive"
                        type="radio"
                        name="type"
                        checked={this.state.walkUp !== null && !this.state.walkUp}
                        onChange={() => this.changeFilter("walkUp", false)}
                    /> 
                    <label htmlFor="typeDrive">Drive Thru</label>
                </fieldset>
                <fieldset>
                    <legend>Referral Required</legend>
                    <input
                        id="referralYes"
                        type="radio"
                        name="referral"
                        checked={this.state.referral !== null && this.state.referral}
                        onChange={() => this.changeFilter("referral", true)}
                    />
                    <label htmlFor="referralYes">Yes</label>
                    <input
                        id="referralNo"
                        type="radio"
                        name="referral"
                        checked={this.state.referral !== null && !this.state.referral}
                        onChange={() => this.changeFilter("referral", false)}
                    />
                    <label htmlFor="referralNo">No</label>
                </fieldset>
                <fieldset>
                    <legend>Appointment Required</legend>
                    <input
                        id="appointmentYes"
                        type="radio"
                        name="appointment"
                        checked={this.state.appointment !== null && this.state.appointment}
                        onChange={() => this.changeFilter("appointment", true)}
                    />
                    <label htmlFor="appointmentYes">Yes</label>
                    <input
                        id="appointmentNo"
                        type="radio"
                        name="appointment"
                        checked={this.state.appointment !== null && !this.state.appointment}
                        onChange={() => this.changeFilter("appointment", false)}
                    />
                    <label htmlFor="appointmentNo">No</label>
                </fieldset>
                <div id="filter_buttons">
                    <button className="btn-light" onClick={() => this.props.applyFilters(this.state)}>Apply Filters</button>
                    <button className="btn-light" onClick={this.clearFilters}>Clear Filters</button>
                </div>
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
            <div id="tc_results_control">
                <FilterForm clearFilters={this.clearFilters} applyFilters={this.applyFilters}/>
                <TCList data={this.state.filteredData}/>
            </div>
        );
    }
}

function loadTestingCenters(data) {
    ReactDOM.render(<FilteredTestCenters data={data}/>, document.getElementById("tc_results_container"));
}