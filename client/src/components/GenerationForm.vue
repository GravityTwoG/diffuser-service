<template>
  <div class="max-w-4xl mx-auto pt-8">
    <div class="max-w-xl mx-auto grid grid-cols-2 gap-4">
      <div
        class="col-span-1 border rounded-lg overflow-hidden aspect-square"
      ></div>
      <div
        class="col-span-1 border rounded-lg overflow-hidden aspect-square"
      ></div>
      <div
        class="col-span-1 border rounded-lg overflow-hidden aspect-square"
      ></div>
      <div
        class="col-span-1 border rounded-lg overflow-hidden aspect-square"
      ></div>
    </div>

    <form class="mt-4 max-w-xl mx-auto flex gap-1 items-stretch" action="">
      <input
        class="px-3 py-1 border rounded-md bg-white flex-1"
        placeholder="Enter your prompt here"
        type="text"
        name="name"
        id="name"
      />
      <button type="submit" class="px-3 py-1 text-slate-950 border rounded-md">
        Generate!
      </button>
    </form>
  </div>
</template>
