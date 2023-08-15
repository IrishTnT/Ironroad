<script lang="ts">
    import type { PageData, ActionData } from './$types';
    import Table from './Table.svelte';
    
    export let data: PageData;
    export let form: ActionData;
</script>

<h1 class="title large text">
    Train Search
</h1>

<div class="exterior">
    <div class="interior">
        <div class="row">
            <div class="col">
                <p>Search for trains at a station!</p>
            </div>
        </div>
        <form method="POST">
            <div class="row">
                <div class="col">
                    <select name="stationCode" id="stationCode">
                        {#each data.stations as station}
                            <option value={station.code}>{station.name}</option>
                        {/each}
                    </select>
                </div>

                <div class="col">
                    <input type=number name="time" id="time" min=5 max=90 placeholder="5 - 90 mins">
                </div>
            </div>
            <div class="row">
                <button>
                    Search
                </button>
            </div>
        </form>

        {#if form?.success}
            <Table tableData={form.trains}/>
        {/if}
    </div>
</div>