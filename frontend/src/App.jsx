import { useState } from "react";
import "./App.css";
import ProductCard from "./components/ProductCard";

// 가짜 데이터: 나중에 백엔드/DB에서 받아올 데이터와 같은 모양으로 만든다
const fakeProducts = [
  { id: 1, name: "콜라", price: 1500, stock: 10, image_url: "🥤" },
  { id: 2, name: "사이다", price: 1400, stock: 8, image_url: "🧃" },
  { id: 3, name: "오렌지주스", price: 2000, stock: 0, image_url: "🍊" },
  { id: 4, name: "생수", price: 1000, stock: 25, image_url: "💧" },
  { id: 5, name: "커피", price: 2500, stock: 5, image_url: "☕" },
  { id: 6, name: "녹차", price: 1800, stock: 12, image_url: "🍵" },
];

function App() {
  // products: 현재 값, setProducts: 값을 바꾸는 함수
  const [products, setProducts] = useState(fakeProducts);

  return (
    <div className="container">
      <h1 className="title">🥤 음료수 자판기</h1>

      {/* useState 체험용 버튼: 상태가 바뀌면 화면이 다시 그려진다 */}
      <div className="toolbar">
        <button onClick={() => setProducts([])}>목록 비우기</button>{" "}
        <button onClick={() => setProducts(fakeProducts)}>목록 채우기</button>
      </div>

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
