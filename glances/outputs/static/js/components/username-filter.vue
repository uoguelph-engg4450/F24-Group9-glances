<template>
    <div id="username-filter-container">
        <button id="open-filter-menu" @click="openFilterMenu()">Filter by Username</button>
        <div id="filter-menu-container" v-show="filterMenuOpen">
            <div style="display: inline-flex;" id="filter-input-container">
                <div class="filter-menu" id="filter-label">Username pattern:</div>
                <input class="filter-menu" id="filter-form" type="text" @input="$emit('filterApplied', $event.target.value)">
            </div>
            <button id="close-filter-menu" @click="openFilterMenu()">Exit</button>
        </div>
        <!-- <input id="filter-form" type="text" placeholder="Enter a username to filter by ..." @input="$emit('filterApplied', $event.target.value)"> -->
    </div>
</template>

<script>

    export default {
        emits: ["filterApplied"],

        data() {
            return {
                filterMenuOpen: false
            }
        },

        methods: {
            openFilterMenu() {
                if(this.filterMenuOpen == false) {
                    this.filterMenuOpen = true;
                } else {
                    this.filterMenuOpen = false;
                }
                console.log(this.filterMenuOpen);
            }
        }
    };
    
</script>

<style>

    #username-filter-container {
        background-color: transparent;
    }

    #open-filter-menu {
        height: 100%;
        width: 120px;
        background-color: black;
        border-style: solid;
        border-width: 1px;
        border-color: white;
        font-family: "Lucida Sans Typewriter", "Lucida Console", Monaco, "Bitstream Vera Sans Mono", monospace;
    }

    #close-filter-menu {
        height: 100%;
        background-color: black;
        border: none;
        font-family: "Lucida Sans Typewriter", "Lucida Console", Monaco, "Bitstream Vera Sans Mono", monospace;
        grid-row: 3;
        margin: 0 auto;
    }

    #filter-menu-container {
        background-color: #000000;
        border-style: solid;
        border-width: 2px;
        border-color: #FFFFFF;
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        height: 200px;
        width: 400px;
        font-family: "Lucida Sans Typewriter", "Lucida Console", Monaco, "Bitstream Vera Sans Mono", monospace;
        display: grid;
        grid-template-columns: 400px;
        grid-template-rows: 20px 100px 50px;
    }

    .filter-menu {
        background-color: transparent;
        font-family: "Lucida Sans Typewriter", "Lucida Console", Monaco, "Bitstream Vera Sans Mono", monospace;
    }

    #filter-input-container {
        height: 100%;
        width: 100%;
        grid-row: 1;
    }

    #filter-label {
        height: 100%;
        width: 40%;
        border: none;
        background-color: transparent;
    }

    #filter-form {
        width: 60%;
        background-color: transparent;
        border-style: solid;
        border-color: white;
        border-width: 1px;
    }



</style>