import "./ProductCard.css";

// props: 부모(App)가 넘겨준 상품 정보 객체
function ProductCard({ product }) {
  const soldOut = product.stock === 0;

  return (
    <div className={soldOut ? "card sold-out" : "card"}>
      <div className="card-image">{product.image_url}</div>
      <h3 className="card-name">{product.name}</h3>
      <p className="card-price">{product.price.toLocaleString()}원</p>
      <p className="card-stock">
        {soldOut ? "품절" : `재고 ${product.stock}개`}
      </p>
    </div>
  );
}

export default ProductCard;
