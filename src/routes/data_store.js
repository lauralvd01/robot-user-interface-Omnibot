import { writable } from 'svelte/store';

/////////////////////////////////////  Frontend data store ///////////////////////////////////

export const is_gamepad_connected = writable(false);

export const moving = writable({x_linear_vel: 0, y_linear_vel: 0, angular_vel: 0});

export const step = 0.1;
export const speed_data = writable({linear_speed: 1 / step, angular_speed: 2 / step,});
export const d_speed = writable({ du: false, dd: false, dl: false, dr: false });

export const batteries = writable({});


/////////////////////////////////////  Backend data store ///////////////////////////////////

import { backend_host, backend_port } from '../config.js';
const endpoint = `http://${backend_host}:${backend_port}/`;

export const modules = writable([]);
export const connected_modules = writable([]);
export const batteries_data = writable([]);
export const power_infos = writable([]);
export const settings = writable(1);
export const simulating = writable(true);

// Associate a request string with its store and default value
const request_store = {
    modules: [modules, []],
    connected_modules: [connected_modules, []],
    batteries_data: [batteries_data, []],
    power_infos: [power_infos, []],
    settings: [settings, 1],
    simulating: [simulating, true]
}

// Send a request to the backend to get the data
export async function fetchData(request) {
    // request = name of the data to fetch = name of the writable where to store the data
    if (!(request_store[request])) {
        console.error("Error: request not found");
        return;
    }
    const [store, default_value] = request_store[request];
    try {
        console.log(`Fetching ${request} ...`);
        const response = await fetch(endpoint + "fetch_" + request); // Send the request to the backend
        const data = await response.json(endpoint + "fetch_" + request); // Parse response and get data as a JSON object
        if (data.ok === true) {
            store.set(data.data); // Set the store with the data received
        } else {
            console.error("Error:", data.error);
            store.set(default_value); // Set the store with the default value
        }
    } catch (error) {
        console.error("Error:", error);
        store.set(default_value); // Set the store with an empty array
    }
}


// Send a request to the backend to move the robot
export function sendMoveData(moves) {
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
