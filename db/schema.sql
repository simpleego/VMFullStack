USE vmShop;

-- 여러 번 실행해도 되도록 기존 테이블을 먼저 지운다 (외래키 때문에 자식 테이블부터 삭제)
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;

-- 회원 (Level 02 이후 사용)
CREATE TABLE users (
  id            INT          NOT NULL AUTO_INCREMENT PRIMARY KEY,
  email         VARCHAR(100) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  name          VARCHAR(50)  NOT NULL,
  role          VARCHAR(10)  NOT NULL DEFAULT 'USER',    -- USER / ADMIN
  status        VARCHAR(10)  NOT NULL DEFAULT 'ACTIVE',  -- ACTIVE / BLOCKED
  created_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT uq_users_email UNIQUE (email),
  CONSTRAINT chk_users_role CHECK (role IN ('USER', 'ADMIN')),
  CONSTRAINT chk_users_status CHECK (status IN ('ACTIVE', 'BLOCKED'))
);

-- 상품 (Level 01 에서 사용)
CREATE TABLE products (
  id          INT          NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name        VARCHAR(50)  NOT NULL,
  price       INT          NOT NULL,
  stock       INT          NOT NULL DEFAULT 0,
  image_url   VARCHAR(255) NULL,
  description VARCHAR(255) NULL,
  is_active   TINYINT(1)   NOT NULL DEFAULT 1,
  created_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT chk_products_price CHECK (price >= 0),
  CONSTRAINT chk_products_stock CHECK (stock >= 0)
);

-- 주문 (Level 이후 사용)
CREATE TABLE orders (
  id          INT         NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id     INT         NOT NULL,
  total_price INT         NOT NULL,
  status      VARCHAR(10) NOT NULL DEFAULT 'PAID',  -- 가상 결제이므로 바로 PAID
  created_at  DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_orders_user FOREIGN KEY (user_id) REFERENCES users (id),
  INDEX idx_orders_user_id (user_id),
  INDEX idx_orders_created_at (created_at)
);

-- 주문 상세 (주문 1건에 상품 여러 개)
CREATE TABLE order_items (
  id         INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  order_id   INT NOT NULL,
  product_id INT NOT NULL,
  quantity   INT NOT NULL,
  unit_price INT NOT NULL,  -- 주문 당시 가격을 따로 저장 (이후 상품 가격이 바뀌어도 유지)
  CONSTRAINT fk_items_order FOREIGN KEY (order_id) REFERENCES orders (id),
  CONSTRAINT fk_items_product FOREIGN KEY (product_id) REFERENCES products (id),
  CONSTRAINT chk_items_quantity CHECK (quantity > 0)
);
