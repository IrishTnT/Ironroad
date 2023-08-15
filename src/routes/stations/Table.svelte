<script lang="ts">

    export let tableData = [
        {
            "test1": "test1",
            "test2": "test2",
            "test3": "test3",
        },
        {
            "test1": "test1",
            "test2": "test2",
            "test3": "test3"
        }
    ];
</script>

<body>
    <table>
        <tr>
            {#each Object.keys(tableData[0]) as key}
                <th>{key}</th>
            {/each}
        </tr>
        {#each tableData as row}
            <tr>
                {#each Object.values(row) as value}
                    <td>{value}</td>
                {/each}
            </tr>
        {/each}
    </table>
</body>