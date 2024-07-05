<script setup lang="ts">
import { onMounted, ref } from 'vue';

import { loadRecentImages } from '../api.ts';
import { getWindow } from '../utils.ts';

interface Props {
  class?: string;
}

const props = defineProps<Props>();

const imageWidth = 15;

const gap = 2;
const elementsInLine = Math.ceil(100 / (imageWidth + gap));
const elementsCount = elementsInLine * 3;
const lineWidth = elementsInLine * imageWidth + (elementsInLine - 1) * gap;

const allImages = ref([]);

const firstLine = ref([]);
const secondLine = ref([]);

const translateX = ref(0);

onMounted(async () => {
  try {
    allImages.value = await loadRecentImages(elementsCount).catch((e) => {});
  } catch (e) {
    console.error(e);

    allImages.value = new Array(elementsCount)
      .fill(0)
      .map((_, i) => `https://fakeimg.pl/200x200/?text=${i}`);
  }

  let slide = 0;
  firstLine.value = getWindow(allImages.value, elementsInLine, slide);
  secondLine.value = getWindow(allImages.value, elementsInLine, slide + 1);

  let before = Date.now();

  const interval = setInterval(() => {
    let now = Date.now();
    const delta = now - before;
    translateX.value -= delta * 0.01;
    before = now;

    if (translateX.value < -lineWidth) {
      slide = (slide + 1) % 3;

      firstLine.value = getWindow(allImages.value, elementsInLine, slide);
      secondLine.value = getWindow(
        allImages.value,
        elementsInLine,
        (slide + 1) % 3
      );

      translateX.value = 0 + gap;
    }
  });

  return () => clearInterval(interval);
});
</script>

<template>
  <div :class="[props.class, 'py-8 overflow-hidden']">
    <ul
      class="flex gap-x-[2vw] first-line"
      :style="`--translate-x: ${translateX}vw`"
    >
      <li
        v-for="image in firstLine"
        :key="image"
        class="flex-shrink-0 flex-grow-0 aspect-square border rounded-lg overflow-hidden"
        :style="`width: ${imageWidth}vw`"
      >
        <img class="w-full object-cover" :src="image" alt="" />
      </li>
    </ul>

    <ul
      class="flex gap-x-[2vw] mt-4 second-line"
      :style="`--translate-x: ${translateX}vw`"
    >
      <li
        v-for="image in secondLine"
        :key="image"
        class="flex-shrink-0 flex-grow-0 aspect-square border rounded-lg overflow-hidden"
        :style="`width: ${imageWidth}vw`"
      >
        <img class="w-full object-cover" :src="image" alt="" />
      </li>
    </ul>
  </div>
</template>

<style scoped>
.first-line {
  transform: translateX(var(--translate-x));
}

.second-line {
  --translate-x2: calc(var(--translate-x) - 0vw);
  transform: translateX(var(--translate-x2));
}

.first-line,
.second-line {
  will-change: transform;
}
</style>
