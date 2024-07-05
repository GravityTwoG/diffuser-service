export const loadRecentImages = async (imagesCount: number) => {
  return new Array(imagesCount)
    .fill(0)
    .map((_, i) => `https://fakeimg.pl/200x200/?text=${i}`);
};
