import { writable } from "svelte/store";

    //import des images
    import pictoIntelligence from "$lib/images/picto_intelligence.svg";
    import picto_energie from "$lib/images/picto_energie.svg";
    import picto_mobilite from "$lib/images/picto_mobilite.svg";
    import picto_stockage from "$lib/images/picto_stockage_energie.svg";
    import picto_capteur from "$lib/images/picto_capteur.svg";

    export const selectedTriangle = writable({ id: null, color: "#494949" }); //définition d'un emplacement par son id et sa couleur

    // Définition des listes de triangles et de trapèzes
    export const triangles = [
        {
            id: 7,
            x1: 250,
            y1: 113.4,
            x2: 200,
            y2: 200,
            x3: 150,
            y3: 113.4,
            hoverColor: "#696761",
            clickColor: "#FF662E",
        },
        {
            id: 8,
            x1: 300,
            y1: 200,
            x2: 200,
            y2: 200,
            x3: 250,
            y3: 113.4,
            hoverColor: "#696761",
            clickColor: "#FF662E",
        },
        {
            id: 9,
            x1: 250,
            y1: 286.61,
            x2: 200,
            y2: 200,
            x3: 300,
            y3: 200,
            hoverColor: "#696761",
            clickColor: "#FF662E",
        },
        {
            id: 10,
            x1: 150,
            y1: 286.61,
            x2: 200,
            y2: 200,
            x3: 250,
            y3: 286.61,
            hoverColor: "#696761",
            clickColor: "#FF662E",
        },
        {
            id: 11,
            x1: 100,
            y1: 200,
            x2: 200,
            y2: 200,
            x3: 150,
            y3: 286.61,
            hoverColor: "#696761",
            clickColor: "#FF662E",
        },
        {
            id: 12,
            x1: 150,
            y1: 113.4,
            x2: 200,
            y2: 200,
            x3: 100,
            y3: 200,
            hoverColor: "#696761",
            clickColor: "#FF662E",
        },
    ];

    export const trapezes = [
        {
            id: 1,
            x1: 275,
            y1: 70.1,
            x2: 125,
            y2: 70.1,
            x3: 150,
            y3: 113.4,
            x4: 250,
            y4: 113.4,
            hoverColor: "#696761",
            clickColor: "#FF662E",
        },
        {
            id: 2,
            x1: 350,
            y1: 200,
            x2: 275,
            y2: 70.1,
            x3: 250,
            y3: 113.4,
            x4: 300,
            y4: 200,
            hoverColor: "#696761",
            clickColor: "#FF662E",
        },
        {
            id: 3,
            x1: 275,
            y1: 329.91,
            x2: 350,
            y2: 200,
            x3: 300,
            y3: 200,
            x4: 250,
            y4: 286.61,
            hoverColor: "#696761",
            clickColor: "#FF662E",
        },
        {
            id: 4,
            x1: 125,
            y1: 329.91,
            x2: 275,
            y2: 329.91,
            x3: 250,
            y3: 286.61,
            x4: 150,
            y4: 286.61,
            hoverColor: "#696761",
            clickColor: "#FF662E",
        },
        {
            id: 5,
            x1: 50,
            y1: 200,
            x2: 125,
            y2: 329.91,
            x3: 150,
            y3: 286.61,
            x4: 100,
            y4: 200,
            hoverColor: "#696761",
            clickColor: "#FF662E",
        },
        {
            id: 6,
            x1: 125,
            y1: 70.1,
            x2: 50,
            y2: 200,
            x3: 100,
            y3: 200,
            x4: 150,
            y4: 113.4,
            hoverColor: "#696761",
            clickColor: "#FF662E",
        },
    ];

    // Fonction permettant de dessiner des triangles équilatéraux
    export function drawEquilateralTriangle(ctx, x1, y1, x2, y2, x3, y3) {
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        ctx.lineTo(x3, y3);
        ctx.closePath();
        ctx.stroke();
        ctx.fill();
    }

    // Fonction pour dessiner un trapèze
    export function drawTrapeze(ctx, x1, y1, x2, y2, x3, y3, x4, y4) {
        ctx.beginPath();
        ctx.moveTo(x1, y1); // Coin supérieur gauche
        ctx.lineTo(x2, y2); // Coin supérieur droit
        ctx.lineTo(x3, y3); // Coin inférieur droit
        ctx.lineTo(x4, y4); // Coin inférieur gauche
        ctx.closePath();
        ctx.stroke();
        ctx.fill();
    }

    // Fonction pour vérifier si un point est dans un triangle
    export function isPointInTriangle(px, py, { x1, y1, x2, y2, x3, y3 }) {
        const area =
            0.5 * (-y2 * x3 + y1 * (-x2 + x3) + x1 * (y2 - y3) + x2 * y3);
        const s =
            (1 / (2 * area)) *
            (y1 * x3 - x1 * y3 + (y3 - y1) * px + (x1 - x3) * py);
        const t =
            (1 / (2 * area)) *
            (x1 * y2 - y1 * x2 + (y1 - y2) * px + (x2 - x1) * py);
        const u = 1 - s - t;
        return s >= 0 && t >= 0 && u >= 0;
    }

    // Fonction pour vérifier si un point est dans un trapèze
    export function isPointInTrapeze(
        px,
        py,
        { x1, y1, x2, y2, x3, y3, x4, y4 },
    ) {
        function sign(x1, y1, x2, y2, x, y) {
            return (x1 - x) * (y2 - y) - (x2 - x) * (y1 - y);
        }

        let d1, d2, d3, d4;
        d1 = sign(px, py, x1, y1, x2, y2);
        d2 = sign(px, py, x2, y2, x3, y3);
        d3 = sign(px, py, x3, y3, x4, y4);
        d4 = sign(px, py, x4, y4, x1, y1);

        const has_neg = d1 < 0 || d2 < 0 || d3 < 0 || d4 < 0;
        const has_pos = d1 > 0 || d2 > 0 || d3 > 0 || d4 > 0;

        return !(has_neg && has_pos);
    }

    export const triangleTitle = writable({
        1: "Module Roue",
        2: "Module Camera",
        3: "Module Roue",
        4: "Module Batterie",
        5: "Module Roue",
        6: "Module Camera",
        7: "Unité centrale",
        8: "Module 5G",
        9: "Supercondensateur",
        10: "Pile à hydrogène",
        11: "Pile à hydrogène",
        12: "Panneau solaire",
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

    export const functionalityImages = {
        "Stockage d'énergie": picto_stockage,
        "Production d'énergie": picto_energie,
        "Mobilité": picto_mobilite,
        "Capteur": picto_capteur,
        "Processeur": pictoIntelligence,
        "Réseau": pictoIntelligence
    };

    export const triangleImages = writable({
        1: picto_mobilite,
        2: picto_capteur,
        3: picto_mobilite,
        4: picto_stockage,
        5: picto_mobilite,
        6: picto_capteur,
        7: pictoIntelligence,
        8: pictoIntelligence,
        9: picto_stockage,
        10: picto_energie,
        11: picto_energie,
        12: picto_energie,
    });