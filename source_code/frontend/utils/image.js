// DB 의 image_url("/products/images/cola.svg") 을
// 프론트 public 폴더 경로("/images/cola.svg") 로 바꾼다.
//   백엔드가 아직 이미지 파일을 내려주지 않기 때문에 public/images 의 같은 파일을 쓴다.
//   image_url 이 NULL 이면 기본 이미지를 보여준다.
export function toImagePath(imageUrl) {
  if (!imageUrl) return '/favicon.svg'
  const fileName = imageUrl.split('/').pop()   // "cola.svg"
  return `/images/${fileName}`
}