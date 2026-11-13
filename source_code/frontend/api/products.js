// 백엔드 상품 API 기본주소

const API_BASE = '/products'

// 공통함수
// fetch 요청
async function request(url, signal) {
    const res = await fetch(url, { signal })

    if (!res.ok) {
        const body = await res.json().catch(() => ({}))
        throw new Error(body.detail || `서버 오류 (${res.status})`)
    }

    return res.json()
}

// [1단계] 상품 목록 : GET /products
export function fetchProducts(signal) {
    return request(API_BASE, signal)
}