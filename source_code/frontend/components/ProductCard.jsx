import "./ProductCard.css";
// import { API_BASE } from "../api/products";

const API_BASE = '/'

// props: 부모(App)가 넘겨준 상품 정보 객체
function ProductCard({ product }) {
  const soldOut = product.stock === 0;

  return (
    <div className={soldOut ? "card sold-out" : "card"}>
      {/* image_url 은 "/products/images/cola.svg" 같은 경로이므로 서버 주소를 앞에 붙인다 */}
      <img
        className="card-image"
        src={`${product.image_url}`}
        alt={product.name}
      />
      <h3 className="card-name">{product.name}</h3>
      <p className="card-price">{product.price.toLocaleString()}원</p>
      <p className="card-stock">
        {soldOut ? "품절" : `재고 ${product.stock}개`}
      </p>
    </div>
  );
}

export default ProductCard;
