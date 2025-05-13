// 画像データ
const images = [
  {
    src: "images/monogatari_inrou_mitokoumon.png",
    caption: 'from <a href="https://www.irasutoya.com/2017/05/blog-post_807.html">いらすとや</a>',
    alt: "水戸黄門"
  },
  {
    src: "images/goddess_leading_the_people.jpg",
    caption: 'ドラクロア「民衆を導く自由の女神」',
    alt: "民衆を導く自由の女神"
  }
];

let currentIndex = 0;

// 画像を切り替える関数
function switchImage() {
  const imageElement = document.getElementById("displayed-image");
  const captionElement = document.getElementById("image-caption");

  // 次の画像に切り替え
  currentIndex = (currentIndex + 1) % images.length;
  const nextImage = images[currentIndex];

  // 画像とキャプションを更新
  imageElement.src = nextImage.src;
  imageElement.alt = nextImage.alt;
  captionElement.innerHTML = nextImage.caption;
}

// 一定時間ごとに画像を切り替え
setInterval(switchImage, 5000); // 5秒ごとに切り替え