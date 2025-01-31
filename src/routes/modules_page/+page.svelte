<script>
    import { onMount } from "svelte";
    import { writable } from "svelte/store";
    import Banner from "../Banner.svelte";
    import picto_stockage_energie from "../../lib/images/picto_stockage_energie.svg";
    import picto_capteur from "../../lib/images/picto_capteur.svg";
    import picto_energie from "../../lib/images/picto_energie.svg";
    import picto_intelligence from "../../lib/images/picto_intelligence.svg";
    import picto_mobilite from "../../lib/images/picto_mobilite.svg";

    const pictos = {
        "Stockage d'énergie": picto_stockage_energie,
        "Capteur": picto_capteur,
        "Production d'énergie": picto_energie,
        "Réseau": picto_intelligence,
        "Processeur": picto_intelligence,
        "Mobilité": picto_mobilite,
    };

    const colors = {
        "Stockage d'énergie": "#e42618",
        "Capteur": "#239e99",
        "Production d'énergie": "#a04040",
        "Réseau": "#4B1338",
        "Processeur": "#4b1338",
        "Mobilité": "#656780",
    };

    import { modules } from "../data_store";
    import { fetchData } from "../data_store";
    
    // Store banner height to adjust the top margin of the content under it
    let bannerHeight = 0;

    // Function that runs when the component is mounted
    onMount(async () => {
        const banner = document.querySelector(".banner");
        if (banner) bannerHeight = banner.offsetHeight;

        // Fetch existant modules
        fetchData("modules");
    });

    let occupied_ids = [];

    let next_id = 0;
    modules.subscribe((value) => {
        if (value.length > 0) {
            let max = next_id;
            value.forEach(element => {
                if (element.module_id && !occupied_ids.includes(element.module_id)) {
                    occupied_ids.push(element.module_id);
                }
                if (element.module_id !== 32 && element.module_id > max) {
                    max = element.module_id;
                }
            });
            next_id = max + 1;
            console.log("Next ID:", next_id);
        }
    });




    let newModule = {
        name: "",
        id: null,
        positions: [],
        functionality: "",
        newFunctionality: { name: "", color: "#979797", picto: "" },
        characteristics: ["name", "power_flow", "energy"],
    };

    function togglePosition(position) {
        if (newModule.positions.includes(position)) {
            newModule.positions = newModule.positions.filter((p) => p !== position);
        } else {
            newModule.positions.push(position);
        }
    }

    function addCharacteristic(characteristic) {
        if (
            characteristic &&
            !newModule.characteristics.includes(characteristic)
        ) {
            newModule.characteristics = [...newModule.characteristics, characteristic];
        }
    }

    function removeCharacteristic(characteristic) {
        newModule.characteristics = newModule.characteristics.filter(
            (char) => char !== characteristic
        );
    }

    function handleFormSubmit(event) {
        event.preventDefault();
        // Vérification des champs
        if (
            newModule.name &&
            (newModule.id === null || !occupied_ids.includes(newModule.id)) &&
            newModule.positions.length > 0 &&
            (newModule.functionality === "Créer une nouvelle"
                ? newModule.newFunctionality.name &&
                  newModule.newFunctionality.color &&
                  newModule.newFunctionality.picto
                : newModule.functionality)
        ) {
            console.log("Module valide :", newModule);
            // Traitement à ajouter ici
            // Actualiser la liste des modules
        } else {
            alert("Vérifier que les champs requis sont remplis, ou que l'id choisi n'est pas déjà utilisé");
        }
    }
</script>




<div class="homepage">
    <Banner />
    <div class="body" style="margin-top: {bannerHeight}px;">
        <div class="sidebar">
            <h2>Ajouter un module</h2>
            <form on:submit={handleFormSubmit}>
                <!-- Champ pour le nom -->
                <div class="form-group">
                    <label for="name">Nom du module *</label>
                    <input id="name" bind:value={newModule.name} required />
                </div>

                <!-- Champ pour l'ID -->
                <div class="form-group">
                    <label for="id">ID du module</label>
                    <input id="id" type="number" min={next_id} max={31} bind:value={newModule.id} />
                </div>

                <!-- Sélection multiple des positions -->
                <div class="form-group">
                    <label for="position">Position(s) *</label>
                    <div id="position" class="checkbox-group">
                        <label>
                            <input
                                type="checkbox"
                                value="Latérale"
                                on:change={() => togglePosition("Latérale")}
                            />
                            Latérale
                        </label>
                        <label>
                            <input
                                type="checkbox"
                                value="Supérieure"
                                on:change={() => togglePosition("Supérieure")}
                            />
                            Supérieure
                        </label>
                    </div>
                </div>

                <!-- Sélection de fonctionnalité -->
                <div class="form-group">
                    <label for="functionality">Fonctionnalité *</label>
                    <select
                        id="functionality"
                        bind:value={newModule.functionality}
                    >
                        <option value="">Aucune</option>
                        <option value="Créer une nouvelle">Créer une nouvelle</option>
                        {#each Object.entries(pictos) as [key, ]}
                            <option value={key}>{key}</option>
                        {/each}
                    </select>
                </div>

                <!-- Création d'une nouvelle fonctionnalité -->
                {#if newModule.functionality === "Créer une nouvelle"}
                    <h3>Nouvelle fonctionnalité</h3>
                    <div class="form-group">
                        <label for="name">Nom *</label>
                        <input
                            type="text"
                            id="name"
                            placeholder="Nom"
                            bind:value={newModule.newFunctionality.name}
                        />
                        <div class="color-picker">
                            <label for="color">Couleur *</label>
                            <input
                                id="color"
                                type="color"
                                bind:value={newModule.newFunctionality.color}
                                style:width="40%"
                            />
                            <div
                                class="color-preview"
                                style="background-color: {newModule.newFunctionality.color}"
                            ></div>
                        </div>
                        <label for="picto">Pictogramme (.svg ou .png, 540x540)</label>
                        <input
                            type="text"
                            placeholder="URL"
                            bind:value={newModule.newFunctionality.picto}
                        />
                        <input
                            type="file"
                            bind:value={newModule.newFunctionality.picto}
                        />
                    </div>
                {/if}

                <!-- Caractéristiques -->
                <div class="form-group">
                    <label for="characteristics">Caractéristiques</label>
                    <ul id="characteristics" class="characteristics-list">
                        {#each newModule.characteristics as char}
                            <li>
                                {char}
                                {#if !["name", "power_flow", "energy"].includes(char)}
                                    <button
                                        type="button"
                                        class="remove-btn"
                                        on:click={() => removeCharacteristic(char)}
                                    >
                                        🗑️
                                    </button>
                                {/if}
                            </li>
                        {/each}
                    </ul>
                    <input
                        type="text"
                        placeholder="Ajouter une caractéristique"
                        on:keydown={(e) => {
                            if (e.key === "Enter") {
                                e.preventDefault(); // Empêche le comportement par défaut (soumission du formulaire)
                                addCharacteristic(e.target.value);
                                e.target.value = "";
                            }
                        }}
                    />
                </div>

                <!-- Bouton pour soumettre -->
                <button type="submit">Ajouter le module</button>
            </form>
        </div>




        <div class="content">
            {#each $modules as module}
                <div
                    class="category"
                    style:background-color={colors[module.functionality]}
                >
                    <div class="header">
                        {#if module.functionality !== null}
                            <div class="image-container">
                                <img
                                    class="picto"
                                    alt="picto category"
                                    src={pictos[module.functionality]}
                                />
                            </div>
                        {/if}
                        <p><strong>Nom : {module.name}</strong></p>
                        <p><strong>Id :</strong> {module.module_id || ""}</p>
                    </div>
                    <div class="details">
                        <p><strong>Fonctionnalité :</strong> {module.functionality || "Aucune"}</p>
                        <p><strong>Positions :</strong> {#each module.position as pos}<span style:margin-left="3px">  + {pos}</span>{/each}</p>
                        <p><strong>Caractéristiques :</strong></p>
                        {#if module.characteristics.length !== 0}
                            <ul class="inline-enum">
                                {#each module.characteristics as char}
                                    <li>{char}</li>
                                {/each}
                            </ul>
                        {:else}
                            <p>Aucune caractéristique</p>
                        {/if}
                    </div>
                </div>
            {/each}
        </div>
    </div>
</div>




<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    .homepage {
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }

    .body {
        margin: 2%;
        display: flex;
        width: 96%;
        height: 100%;
    }

    .sidebar {
        width: 30%;
        padding: 20px;
        background-color: #ffd7c9;
        border-radius: 10px;
        /* border-right: 1px solid #ddd;
        box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1); */
        /* box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); */
        margin-right: 2%;
    }

    .sidebar h2 {
        margin-bottom: 20px;
        font-weight: bold;
   }

   .sidebar h3 {
        margin-bottom: 10px;
        font-weight: bold;
   }

    .form-group {
        margin-bottom: 15px;
    }

    .form-group label {
        font-weight: bold;
        display: block;
        margin-bottom: 5px;
    }

    .form-group input,
    .form-group select,
    .form-group button {
        width: 100%;
        padding: 8px;
        margin-bottom: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
    }

    .checkbox-group label {
        display: inline-flex;
        margin-bottom: 5px;
        width: 45%;
        font-weight: normal;
    }

    .color-picker {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .color-preview {
        width: 20px;
        height: 20px;
        margin-left: 10px;
        border: 1px solid white;
        border-radius: 50%;
    }

    .characteristics-list {
        list-style: none;
        padding: 0;
    }

    .characteristics-list li {
        display: flex;
        justify-content: space-between;
        margin-bottom: 5px;
    }

    .remove-btn {
        margin-left: 2%;
        max-height: 40px;
        max-width: 40px;
        /* background: none; */
        border: none;
        cursor: pointer;
    }

    button[type="submit"] {
        background-color: #ff662e;
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
    }

    button[type="submit"]:hover {
        background-color: #e65528;
    }


    .content {
        display: flex;
        flex-direction: column;
        flex-grow: 1;
        overflow: auto;
        height: 100%;
        width: 60%;
    }

    .category {
        /* display: flex;
        flex-direction: column;
        align-items: start; */
        border-radius: 15px;
        /* padding: 10px 10px;
        margin-bottom: 10px; */
        padding: 20px;
        margin-bottom: 15px;
        width: 90%;
        /* box-sizing: border-box; */
        background-color: #979797;
        color: white;
        font-family: "Roboto", sans-serif;
    }

    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .details {
        margin-top: 10px;
    }

    .inline-enum li {
        display: inline;
        margin-right: 10px;
        /* font-family: "Roboto", sans-serif;
        display: inline-block;
        margin-left: 5%;
        padding-left: 3%; */
    }

    .picto {
        /* height: 80%;
        width: 80%;
        position: relative; */
        height: 40px;
        width: 40px;
    }

    .image-container {
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: white;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        /* margin: 5px; */
    }
</style>
