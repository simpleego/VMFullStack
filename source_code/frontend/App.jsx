import { useState } from 'react'
import heroImg from './assets/hero.png'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import './App.css'

import ProductCard from "./components/ProductCard";
import ProductList from './pages/ProductList'
// 이미지 기본 경로 (public/images 폴더 = 사이트 주소의 /images)
const IMAGE_PATH = '/images'


function App() {  

  return (
    <div className="container">
      <header className="header">
        <h1 className="title">🥤 음료수 자판기</h1>
      </header>

      <ProductList />
    </div>
  )
}

export default App
