<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';

import { generateImages, getGeneratedImages } from '../api.ts';

const generatedImages = ref([]);

const prompt = ref('');
const imagesCount = ref('1');

const isPending = ref(false);
const isGenerating = ref(false);

const isFormDisabled = computed(() => {
  return isPending.value || isGenerating.value;
});

onMounted(async () => {
  try {
    generatedImages.value = [];

    if (window.location.search) {
      const params = new URLSearchParams(window.location.search);

      if (params.has('generationId')) {
        isGenerating.value = true;
        const generationId = params.get('generationId');
        startPolling(generationId);
      }
    }
  } catch (e) {
    console.error(e);
  }
});

const startPolling = async (generationId: string) => {
  const interval = setInterval(async () => {
    try {
      const result = await getGeneratedImages(generationId);

      if (result.status !== 'PENDING') {
        clearInterval(interval);
        generatedImages.value = result.images;

        isGenerating.value = false;
      }

      prompt.value = result.prompt;
      imagesCount.value = result.images.length.toString();
    } catch (e) {
      console.error(e);
    }
  }, 3000);
};

const onSubmit = async () => {
  try {
    if (!prompt.value || Number(imagesCount.value) < 0) {
      return;
    }

    generatedImages.value = [];
    isPending.value = true;
    isGenerating.value = true;
    const result = await generateImages(
      prompt.value,
      Number(imagesCount.value)
    );

    const newURL = `${window.location.protocol}//${window.location.host}${window.location.pathname}?generationId=${result.id}`;
    window.history.pushState({ path: newURL }, '', newURL);

    startPolling(result.id);
  } catch (e) {
    console.error(e);
    isGenerating.value = false;
  } finally {
    isPending.value = false;
  }
};
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 pt-8">
    <div class="max-w-xl mx-auto grid grid-cols-2 gap-4 aspect-square">
      <div
        v-for="image in generatedImages"
        :class="`${
          generatedImages.length === 1 ? 'col-span-2' : 'col-span-1'
        } border rounded-lg overflow-hidden aspect-square`"
      >
        <img class="w-full object-cover" :src="image" alt="" />
      </div>
    </div>

    <p v-if="isGenerating" class="text-center text-slate-950">
      Generating images...
    </p>

    <form
      @submit.prevent="onSubmit"
      class="generation-form mt-4 max-w-xl mx-auto flex gap-1 items-stretch border rounded-lg overflow-hidden"
      :data-is-generating="isGenerating"
    >
      <input
        class="px-3 py-1 bg-white text-slate-950 flex-1"
        placeholder="Enter your prompt here"
        type="text"
        name="name"
        id="name"
        v-model="prompt"
        :disabled="isFormDisabled"
      />

      <input
        class="px-3 py-1 w-16 bg-white text-slate-950"
        type="number"
        step="1"
        min="1"
        max="4"
        name="imagesCount"
        id="imagesCount"
        v-model="imagesCount"
        :disabled="isFormDisabled"
      />

      <button
        type="submit"
        :disabled="isFormDisabled"
        class="px-3 py-1 text-slate-950 bg-white hover:bg-orange-400 transition-colors"
      >
        Generate!
      </button>
    </form>
  </div>
</template>

<style scoped>
.generation-form {
  --border-angle: 0turn;
  --main-bg: conic-gradient(
    from var(--border-angle),
    #213,
    #112 5%,
    #112 60%,
    #213 95%
  );

  border: solid 4px transparent;
  border-radius: 2em;
  --gradient-border: conic-gradient(
    from var(--border-angle),
    transparent 25%,
    #08f,
    #f03 99%,
    transparent
  );

  background: var(--main-bg) padding-box, var(--gradient-border) border-box,
    var(--main-bg) border-box;

  background-position: center center;
}

.generation-form[data-is-generating='true'] {
  animation: bg-spin 3s linear infinite forwards;
}

@keyframes bg-spin {
  to {
    --border-angle: 1turn;
  }
}

@property --border-angle {
  syntax: '<angle>';
  inherits: true;
  initial-value: 0turn;
}
</style>
