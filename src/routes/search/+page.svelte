<script lang="ts">
    import type { PageData } from './$types';
    
    export let data: PageData;
</script>

<h1 class="title large">
    Train Search
</h1>

<div class="exterior">
    <div class="interior">
        <div class="row">
            <div class="col-2">
                <p>There are currently {data.train-count}</p>
            </div>
        </div>
        <div class="row">
            <div class="col-2">
                <select>
                    <!--Data array is called 'stations'-->
                    {#each data.stations as station}
                        <option value={station}>{station}</option>
                    {/each}
                </select>
            </div>
        </div>
    </div>
</div>