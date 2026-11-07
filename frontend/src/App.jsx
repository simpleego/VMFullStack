import { useEffect, useState } from "react";
import "./App.css";
import ProductCard from "./components/ProductCard";
import { fetchProducts } from "./api/products";

function App() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // 화면이 처음 나타날 때 한 번만 실행된다 ([] 의 의미)
  useEffect(() => {
    fetchProducts()
      .then((data) => setProducts(data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p className="message">불러오는 중...</p>;
  if (error) return <p className="message error">오류: {error}</p>;

  return (
    <div className="container">
      <h1 className="title">🥤 음료수 자판기</h1>

      {products.length === 0 ? (
        <p className="message">상품이 없습니다.</p>
      ) : (
        <div className="product-grid">
          {products.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
