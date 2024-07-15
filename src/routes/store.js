import { writable } from 'svelte/store';

export const selectedTriangle = writable({ id: null, color: '#494949' });
export const triangleData = writable({
    1: "Information sur le triangle 1",
    2: "Information sur le triangle 2",
    3: "Information sur le triangle 3",
    4: "Information sur le triangle 4",
    5: "Information sur le triangle 5",
    6: "Information sur le triangle 6",
    7: "Information sur le triangle 7",
    8: "Information sur le triangle 8",
    9: "Information sur le triangle 9",
    10: "Information sur le triangle 10",
    11: "Information sur le triangle 11",
    12: "Information sur le triangle 12",
});
