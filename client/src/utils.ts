export function superSlice<T>(array: T[], start: number, end: number): T[] {
  if (end > start) {
    return array.slice(start, end);
  }

  return array.slice(start, array.length).concat(array.slice(0, end));
}

export function getWindow<T>(
  array: T[],
  elementsInSlide: number,
  slide: number
): T[] {
  let start = slide * elementsInSlide;
  let end = start + array.length;

  if (end > array.length) {
    end = end % array.length;
  }

  return superSlice(array, start, end);
}
