<template>
    <section class="plugin" id="users">
        <table class="table table-sm table-borderless">
            <thead>
                <tr>
                    <th scope="col" style="width: 25%">ACTIVE USERS</th>
                    <th scope="col" class="text-end" style="width: 25%">Sesion Start</th>
                    <th scope="col" class="text-end" style="width: 25%">CPU usg</th>
                    <th scope="col" class="text-end" style="width: 25%">Mem usg</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in usermonitor" :key=user.name>
                    <td scope="row">{{ user.name }}</td>
                    <td class="text-end w-25">{{ user.started }}</td>
                    <td class="text-end w-25">{{ parseFloat(user.cpu).toFixed(2) }} %</td>
                    <td class="text-end w-25">{{ parseFloat(user.memory).toFixed(2) }} %</td>
                </tr>
            </tbody>
        </table>
    </section>
</template>

<script>

import { store } from '../store.js';

export default {
    props: {
        data: {
            type: Object
        },
        sorter: {
            type: Object
        },
        usernameFilterStr: {
            type: String,
            required: false
        }
    },
    data() {
        return store;
    },
    computed: {
        usermonitor() {
            const userstats = this.data.stats['usermonitor'];
            return userstats;
        }
    }
};
</script>