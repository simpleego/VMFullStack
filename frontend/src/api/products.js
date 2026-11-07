// 백엔드 주소. 나중에 환경에 따라 바꾸기 쉽도록 한 곳에 모아 둔다
const API_BASE = "http://localhost:8000";

export async function fetchProducts() {
  const response = await fetch(`${API_BASE}/api/v1/products`);

  if (!response.ok) {
    throw new Error(`서버 오류 (${response.status})`);
  }

  return response.json();
}
