<script lang="ts">
  import { onMount } from "svelte";

  export let value: string | null;
  export let type: "gallery" | "table";
  export let selected = false;

  let size: number;
  let el: HTMLDivElement;

  function set_styles(element: HTMLElement, el_width: number): void {
    if (!element || !el_width) return;
    el.style.setProperty(
      "--local-text-width",
      `${el_width < 150 ? el_width : 200}px`
    );
    el.style.whiteSpace = "unset";
  }

  onMount(() => {
    set_styles(el, size);
  });
</script>

<div
  bind:clientWidth={size}
  bind:this={el}
  class:table={type === "table"}
  class:gallery={type === "gallery"}
  class:selected
>
  <!-- {value ? value : ""} -->
  <!-- {JSON.stringify(value)} -->
  {#if value}
    {#if value["chains"].length > 1}
      <b>Input composed of {value["chains"].length} chains </b> <br />
    {:else}
      <b>Input composed of {value["chains"].length} chain </b><br />
    {/if}
    <ul>
      {#each value["chains"] as val}
        {#if ["protein", "DNA", "RNA"].includes(val["class"])}
          <li><div>{val["class"]} {val["sequence"].length} residues</div></li>
        {/if}
        {#if val["class"] == "ligand"}
          {#if val["name"] != undefined}
            <li><div>Ligand {val["name"]}</div></li>
          {:else if val["smiles"] != undefined}
            <li><div>Ligand SMILES with {val["smiles"].length} atoms</div></li>
          {:else}
            <li><div>Ligand</div></li>
          {/if}
        {/if}
      {/each}
    </ul>

    <ul>
      <li>{value["covMods"].length} covalent modifications</li>
    </ul>
  {/if}
</div>

<style>
  .gallery {
    padding: var(--size-1) var(--size-2);
  }

  div {
    overflow: hidden;
    min-width: var(--local-text-width);

    white-space: nowrap;
  }
</style>
