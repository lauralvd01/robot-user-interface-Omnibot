import { writable } from 'svelte/store';
//import des images
import pictoIntelligence from '$lib/images/picto_intelligence.svg';
import picto_energie from '$lib/images/picto_energie.svg'
import picto_mobilite from '$lib/images/picto_mobilite.svg'
import picto_stockage from '$lib/images/picto_stockage_energie.svg'
import picto_capteur from '$lib/images/picto_capteur.svg'

export const selectedTriangle = writable({ id: null, color: '#494949' }); //définition d'un emplacement par son id et sa couleur

export const triangleTitle = writable({
    1:"Module Roue",
    2:"Module Camera",
    3:"Module Roue",
    4:"Module Batterie",
    5:"Module Roue",
    6:"Module Camera",
    7:"Unité centrale",
    8:"Module 5G",
    9:"Supercondensateur",
    10:"Pile à hydrogène",
    11:"Pile à hydrogène",
    12:"Panneau solaire",
});

export const triangleData = writable({
    1: "Information sur le module roue (id:1)",
    2: "Information sur le module camera (id:2)",
    3: "Information sur le module roue (id:3)",
    4: "Information sur le module batterie (id:4)",
    5: "Information sur le module roue (id:5)",
    6: "Information sur le module Camera (id:6)",
    7: "Information sur l'unité centrale (id:7)",
    8: "Information sur le module 5G (id:8)",
    9: "Information sur le Supercondensateur (id:9)",
    10: "Information sur la pile à hydrogène (id:10)",
    11: "Information sur la pile à hydrogène (id:11)",
    12: "Information sur le panneau solaire (id:12)",
});
export const triangleImages = writable({
    1:picto_mobilite,
    2:picto_capteur,
    3:picto_mobilite,
    4:picto_stockage,
    5:picto_mobilite,
    6:picto_capteur,
    7:pictoIntelligence,
    8:pictoIntelligence,
    9:picto_stockage,
    10:picto_energie,
    11:picto_energie,
    12:picto_energie,
});