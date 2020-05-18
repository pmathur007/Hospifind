class MobileUserTable extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            data: props.data,
            showingData: Array(props.data.length).fill(false)
        }
        this.toggleDetails = this.toggleDetails.bind(this);
    }

    toggleDetails(i) {
        const newShowing = this.state.showingData.slice();
        newShowing[i] = !newShowing[i];
        this.setState({ showingData: newShowing });
    }

    render() {
        return (
            <table>
                <thead>
                    <th>Username</th>
                    <th>Role</th>
                    <th>User Info</th>
                    <th>Data Details</th>
                </thead>
                {this.state.data.map((d, i) => {
                    return (
                        <tbody key={d.id}>
                            <tr>
                                <td>{d.username}</td>
                                <td>{d.is_admin ? "Admin" : "Data Input"}</td>
                                <td><button onClick={() => this.toggleDetails(i)}>User Info</button></td>
                                <td><button>Data Details</button></td>
                            </tr>
                            {this.state.showingData[i] ? (
                                <tr>
                                    <td colSpan={4}>
                                        <p>Name: {d.name}</p>
                                        <p>Email: {d.email}</p>
                                    </td>
                                </tr>
                            ) : ""}
                        </tbody>
                    );
                })}
            </table>
        );
    }
}

class FullUserTable extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            data: props.data
        }
    }

    render() {
        return (
            <table>
                <thead>
                    <th>Username</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Role</th>
                    <th>Data Details</th>
                </thead>
                {this.state.data.map((d) => {
                    return (
                        <tr key={d.id}>
                            <td>{d.username}</td>
                            <td>{d.name}</td>
                            <td>{d.email}</td>
                            <td>{d.is_admin ? "Admin" : "Data Input"}</td>
                            <td><button>Data Details</button></td>
                        </tr>
                    );
                })}
            </table>
        );
    }
}

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
        data: JSON.stringify(query),
    }).done(function (json) {
        if ($(window).width() < 800) {
            ReactDOM.render(<MobileUserTable data={json} />, document.getElementById("user_table"));
        }
        else {
            ReactDOM.render(<FullUserTable data={json} />, document.getElementById("user_table"));
        }
        window.addEventListener("resize", function () {
            if ($(window).width() < 800) {
                ReactDOM.render(<MobileUserTable data={json} />, document.getElementById("user_table"));
            }
            else {
                ReactDOM.render(<FullUserTable data={json} />, document.getElementById("user_table"));
            }
        });
    });
}