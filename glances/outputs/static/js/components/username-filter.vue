<template>
    <div id="username-filter-container">
        <button id="open-filter-menu" @click="openFilterMenu()">Filter</button>
        <div id="filter-menu" v-show="filterMenuOpen">
            <div>Username pattern:</div>
            <input type="text">
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

    #filter-form {
        width: 27%;
    }

    #open-filter-menu {
        height: 100%;
        width: 80px;
        font-family: "Lucida Sans Typewriter", "Lucida Console", Monaco, "Bitstream Vera Sans Mono", monospace;
    }

    #filter-menu {
        background-color: #000000;
        border-radius: 2px;
        border-color: #FFFFFF;
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        height: 200px;
        width: 400px;
        font-family: "Lucida Sans Typewriter", "Lucida Console", Monaco, "Bitstream Vera Sans Mono", monospace;
    }

</style>