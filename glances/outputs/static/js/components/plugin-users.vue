<template>
    <section class="plugin" id="users">
        <table class="table table-sm table-borderless">
            <thead>
                <tr>
                    <th scope="col" style="width: 30%">USERS</th>
                    <th scope="col" class="text-end" style="width: 20%">Processes</th>
                    <th scope="col" class="text-end" style="width: 50%">Total CPU Usage (%)</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in user_summary" :key=user.name>
                    <td scope="row">{{ user.name }}</td>
                    <td class="text-end w-25">{{ user.num_processes }}</td>
                    <td class="text-end w-25">{{ user.cpu_usage }} %</td>
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
        processes() {
            return this.data.stats['processlist'];
        },
        user_summary() {
            const allUsers = (this.processes || []).map((process) => process.username);
            const usernames = [...new Set(allUsers)]; // Convert Set to an array
            const num_cpu_cores = this.data.stats['core'].log;

            console.log(this.data.stats);
            

            let summary = [];

            for (let i = 0; i < usernames.length; i++) {
                let num_processes = 0;
                let cpu_usage = 0;

                for (let j = 0; j < this.processes.length; j++) {
                    if (this.processes[j].username === usernames[i]) {
                        num_processes += 1;
                        cpu_usage += this.processes[j].cpu_percent || 0; // Handle null/undefined
                    }
                }

                cpu_usage = cpu_usage/num_cpu_cores;
                if(cpu_usage > 0.009) {
                    summary.push({
                        name: usernames[i],
                        num_processes: num_processes,
                        cpu_usage: cpu_usage.toFixed(2),
                    });
                }
            }
            return summary;
        }
    }
};
</script>