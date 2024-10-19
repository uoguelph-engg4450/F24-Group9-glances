<template>
    <div id="username-filter-container">
        <input id="filter-form" type="text" placeholder="Enter a username to filter by ..." @input="$emit('filterApplied', $event.target.value)">
    </div>
</template>

<script>

    export default {
        emits: ["filterApplied"]
    }
    
</script>

<style>

    #username-filter-container {
        background-color: transparent;
    }

    #filter-form {
        width: 27%;
    }

</style>