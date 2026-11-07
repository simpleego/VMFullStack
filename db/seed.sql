USE vmShop;

-- 상품 샘플 데이터
-- image_url 은 백엔드 서버의 products/images 폴더에 있는 이미지 경로이다.
-- (백엔드가 /products/images 주소로 이 폴더를 제공한다)
INSERT INTO products (name, price, stock, image_url) VALUES
  ('콜라',       1500, 10, '/products/images/cola.svg'),
  ('사이다',     1400,  8, '/products/images/cider.svg'),
  ('오렌지주스', 2000,  0, '/products/images/orange.svg'),
  ('생수',       1000, 25, '/products/images/water.svg'),
  ('커피',       2500,  5, '/products/images/coffee.svg'),
  ('녹차',       1800, 12, '/products/images/greentea.svg');

-- 관리자 계정은 비밀번호 해시(bcrypt)가 필요하므로 회원가입을 배우는 Level 02 에서 추가한다
