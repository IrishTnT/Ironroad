<script lang="ts">
    import type { PageData } from './$types';
    
    export let data: PageData;
</script>

    <div class="container">
        <img src="./ironroad.png">
        <h1 class="title large nomargin">Test for all CSS elements</h1>
        <h1 class="medium nomargin">MEDIUM TEXT</h1>
        <h1 class="small nomargin">SMALL TEXT</h1>

        <p>Plain text</p>

        <div class="exterior">
            <h1 class="title large">The Form</h1>
            <div class="interior">
                <form>
                    <!--Dropdown-->
                    <div class="form-element dropdown">
                        <select>
                            <option value="1">Option 1</option>
                            <option value="2">Option 2</option>
                        </select>
                    </div>

                    <!--Input-->
                    <div class="form-element input">
                        <input type="text" placeholder="Input">
                    </div>

                    <!--Button-->
                    <div class="form-element button">
                        <button>Button</button>
                    </div>

                    <!--Checkbox-->
                    <div class="form-element checkbox">
                        <input type="checkbox" id="checkbox">
                        <label for="checkbox">Checkbox</label>
                    </div>

                    <!--Switch-->
                    <div class="form-element switchbox">
                        <label class="switch">
                            <input type="checkbox" class="switchbox">
                            <span class="switchslider"></span>
                        </label>
                    </div>

                    <!--Slider-->
                    <div class="form-element slider">
                        <input type="range" id="slider">
                        <label for="slider">Slider</label>
                    </div>

                    <!--Textarea-->
                    <div class="form-element textarea">
                        <textarea placeholder="Textarea"></textarea>
                    </div>
                    
                </form>
            </div>
        </div>
    </div>