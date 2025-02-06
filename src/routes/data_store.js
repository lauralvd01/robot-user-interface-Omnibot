import { writable } from 'svelte/store';

/////////////////////////////////////  Frontend data store ///////////////////////////////////

export const is_gamepad_connected = writable(false);
is_gamepad_connected.subscribe(value => {console.log("Gamepad connected ?", value);});

export const moving = writable({x_linear_vel: 0, y_linear_vel: 0, angular_vel: 0});

export const step = 0.1;
export const speed_data = writable({linear_speed: 1 / step, angular_speed: 2 / step,});
export const d_speed = writable({ du: false, dd: false, dl: false, dr: false });

export const batteries = writable({});

function updateBatteryLevel(batteries_data) {
    let batt = {};
    if (batteries_data.length > 0) {
        for (const battery_data of batteries_data) {
            batt[battery_data.slot_id] = {
                name: battery_data.name.toUpperCase(),
                state_of_charge: Math.round(
                    battery_data.state_of_charge * 100,
                ),
            };
        }
    }
    batteries.set(batt);
}

export const graphic_saved_data = writable({});

/////////////////////////////////////  Backend data store ///////////////////////////////////

import { backend_host, backend_port } from '../config.js';
const endpoint = `http://${backend_host}:${backend_port}/`;

export const modules = writable([]);
const current_data = writable({});
export const connected_modules = writable([]);
export const batteries_data = writable([]);
export const power_infos = writable([]);
export const settings = writable(1);
export const simulating = writable(true);

current_data.subscribe(value => {
    if (value["connected_modules"]) {
        connected_modules.set(value["connected_modules"]);
    } else { connected_modules.set([]); }

    if (value["batteries_data"]) {
        batteries_data.set(value["batteries_data"]);
    } else { batteries_data.set([]); }

    if (value["power_infos"]) {
        power_infos.set(value["power_infos"]);
    } else { power_infos.set([]); }
})
batteries_data.subscribe(value => updateBatteryLevel(value));

// Associate a request string with its store and default value
const request_store = {
    modules: { need_connection: false, store: modules, default_value: [] },
    current_data: { need_connection: true, store: current_data, default_value: {} },
    connected_modules: { need_connection: true, store: connected_modules, default_value: [] },
    batteries_data: { need_connection: true, store: batteries_data, default_value: [] },
    power_infos: { need_connection: true, store: power_infos, default_value: [] },
    settings: { need_connection: false, store: settings, default_value: 1 },
    simulating: { need_connection: false, store: simulating, default_value: true },
}

// Don't send a new request when it is impossible to connect to the robot
let no_connection = false;

async function test_connection() {
    try {
        console.log("Testing connection ...");
        const response = await fetch(endpoint + "test_connection");
        const data = await response.json();
        if (data.ok === true) {
            console.log("Connection successful");
            no_connection = false;
        }
    }
    catch (error) {
        console.error("Error:", error);
        no_connection = true;
        let sleep = new Promise(resolve => setTimeout(resolve, 500));
        sleep.then(() => test_connection());
    }
}


// Send a request to the backend to get the data
export async function fetchData(request) {
    // request = name of the data to fetch = name of the writable where to store the data
    if (!(request_store[request])) {
            console.error("Error: request not found");
        return;
    }
    const need_connection = request_store[request]["need_connection"];
    const store = request_store[request]["store"];
    const default_value = request_store[request]["default_value"];

    // Fetch data only if the request does not need a connection or if the connection is established
    if (!need_connection || (need_connection && !no_connection)) {
        try {
            console.log(`Fetching ${request} ...`);
            const response = await fetch(endpoint + "fetch_" + request); // Send the request to the backend
            const data = await response.json(endpoint + "fetch_" + request); // Parse response and get data as a JSON object
            if (data.ok === true) {
                store.set(data.data); // Set the store with the data received
                no_connection = false;
            } else {
                console.error("Error:", data.error);
                store.set(default_value); // Set the store with the default value
                if (data.error === "[Errno 111] Connect call failed ('192.168.50.153', 6550)") {
                    console.error("Error: Connection to the robot failed");
                    no_connection = true;
                    test_connection();
                }
            }
        } catch (error) {
            console.error("Error:", error);
            store.set(default_value); // Set the store with an empty array
        }
    }
    // If the request is to get the current data, wait 1 second before sending a new request
    if (request === "current_data") {
        let sleep = new Promise(resolve => setTimeout(resolve, 1000));
        sleep.then(() => fetchData(request));
    }
}


// Send a request to the backend to move the robot
export function sendMoveData(moves) {
    if (no_connection) return;

    moving.set({...moves});
    console.log("Sending move data: ", moves);
    fetch(endpoint + "post_move", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(moves),
    });
}

// Send a request to the backend to change robot speed settigs
export function sendSpeedData(speed_data) {
    if (no_connection) return;
    
    console.log("Sending speed data: ", speed_data);
    fetch(endpoint + "set_speed", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            linear_speed: Math.round(speed_data.linear_speed * step * 10) / 10,
            angular_speed: Math.round(speed_data.angular_speed * step * 10) / 10,
        }),
    });
}

