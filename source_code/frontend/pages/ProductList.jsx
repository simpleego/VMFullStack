import { useEffect, useState } from "react";
import ProductCard from "../components/ProductCard";
import { fetchProducts } from "../api/products";
import { toImagePath } from "../utils/image";

// 상품 목록 화면
function ProductList(){
    // 화면 상태 3가지 : 데이터, 로딩 중인지, 에러 메시지
    const [products, setProducts] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    // 화면이 처음 나타날때 한 번만 상품 목록을 표시
    useEffect(()=>{

        // 화면이 사라지면 진행 중인 요청을 취소하기 위한 컨트롤러
        const controller = new AbortController()

        fetchProducts(controller.signal)
            .then((data)=> {
                setProducts(data.map((p)=>(
                    {...p, image_url: toImagePath(p.image_url) })))
                })
            .catch((err)=>{
                if (err.name === 'AbortError') return // 취소된 요청은 에러가 아님
                setError(err.message)
            })
            .finally(()=>{
                if (!controller.signal.aborted) setLoading(false)
            })

        // 정리 함수 : 화면이 사라질 때 요청 취소
        return ()=> controller.abort()
    }, [])

    if (loading) return <p className="message">상품을 불러오는 중...</p>
    if (error) return <p className="message error">⚠️ {error}</p>
    if (products.length === 0) return <p className="message">판매 중인 상품이 없습니다.</p>

    return (
        <div className="product-grid">
            {products.map((product)=>(
                <ProductCard  key={product.id} product={product} />
            ))}
        </div>
    )
}

export default ProductList
